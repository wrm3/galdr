"""
crawl_add_target — Add a custom crawl target for internal docs.

Allows teams to crawl internal wikis, Confluence, company docs, etc.
Results are tagged with source_visibility for access control.
"""
import json
import logging
from typing import Optional

TOOL_NAME = "crawl_add_target"
TOOL_DESCRIPTION = (
    "Add a custom documentation crawl target (internal wiki, Confluence, company docs). "
    "The target can then be crawled with platform_crawl_trigger. "
    "Results are tagged with visibility: 'internal' (company docs) or 'public' (platform docs)."
)
TOOL_PARAMS = {
    "name":       "Unique name for the target (e.g. 'company-wiki', 'confluence-api')",
    "urls":       "List of starting URLs to crawl",
    "max_pages":  "Maximum pages to crawl (default: 50)",
    "max_depth":  "Maximum link depth (default: 3)",
    "visibility": "Access scope: 'public' (platform docs) or 'internal' (company docs). Default: 'internal'",
    "user_id":    "User ID creating the target (optional, for audit trail)",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(
    name: str,
    urls: list,
    max_pages: int = 50,
    max_depth: int = 3,
    visibility: str = "internal",
    user_id: Optional[str] = None,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not name or not name.strip():
        return {"success": False, "error": "name is required"}
    if not urls:
        return {"success": False, "error": "urls list is required (at least one URL)"}
    if visibility not in ("public", "internal"):
        visibility = "internal"

    name = name.strip().lower().replace(" ", "-")

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO crawl_targets (name, urls, max_pages, max_depth, visibility, created_by)
                    VALUES (%s, %s::jsonb, %s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE
                        SET urls       = EXCLUDED.urls,
                            max_pages  = EXCLUDED.max_pages,
                            max_depth  = EXCLUDED.max_depth,
                            visibility = EXCLUDED.visibility,
                            created_by = EXCLUDED.created_by
                    RETURNING id
                    """,
                    (name, json.dumps(urls), max_pages, max_depth, visibility, user_id),
                )
                target_id = cur.fetchone()[0]
                conn.commit()

        return {
            "success": True,
            "target_id": target_id,
            "name": name,
            "urls": urls,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "visibility": visibility,
            "message": f"Target '{name}' created. Use platform_crawl_trigger(target='{name}') to crawl.",
        }
    except Exception as e:
        _logger.error("Failed to add crawl target: %s", e)
        return {"success": False, "error": str(e)}
