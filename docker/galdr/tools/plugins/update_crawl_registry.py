"""
update_crawl_registry — record a completed crawl in the shared registry.

Called by the crawl4ai host-side script after each successful platform crawl.
Updates last_crawled_at and pages_count so other projects know docs are fresh.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "update_crawl_registry"
TOOL_DESCRIPTION = (
    "Update the platform docs crawl registry after a successful crawl. "
    "Call this after running crawl4ai (scripts/platform_crawl.py) for a platform. "
    "Marks the platform as freshly crawled so other projects skip redundant crawls. "
    "Platforms: 'cursor' | 'claude_code' | 'gemini'."
)
TOOL_PARAMS = {
    "platform":    "Platform that was crawled: 'cursor' | 'claude_code' | 'gemini'",
    "pages_count": "Number of pages ingested in this crawl",
    "status":      "Crawl outcome: 'success' | 'partial' | 'failed' (default: 'success')",
    "notes":       "Optional notes (e.g., 'manual backfill', 'partial — 3 targets dead-lettered')",
}

KNOWN_PLATFORMS = {"cursor", "claude_code", "gemini"}

_db = None


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(
    platform: str,
    pages_count: int,
    status: str = "success",
    notes: Optional[str] = None,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not available"}

    platform = platform.lower().strip()
    if platform not in KNOWN_PLATFORMS:
        return {
            "success": False,
            "error": f"Unknown platform '{platform}'. Valid: {sorted(KNOWN_PLATFORMS)}",
        }

    valid_statuses = {"success", "partial", "failed"}
    if status not in valid_statuses:
        return {
            "success": False,
            "error": f"Invalid status '{status}'. Valid: {sorted(valid_statuses)}",
        }

    pages_count = max(0, pages_count)

    try:
        with _db.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO platform_docs_crawl_registry
                    (platform, last_crawled_at, pages_count, crawl_status, notes)
                VALUES
                    (%s, NOW(), %s, %s, %s)
                ON CONFLICT (platform) DO UPDATE SET
                    last_crawled_at = NOW(),
                    pages_count     = EXCLUDED.pages_count,
                    crawl_status    = EXCLUDED.crawl_status,
                    notes           = EXCLUDED.notes,
                    updated_at      = NOW()
                RETURNING last_crawled_at, pages_count, crawl_status
                """,
                (platform, pages_count, status, notes),
            )
            row = cur.fetchone()
            _db.conn.commit()

        return {
            "success": True,
            "platform": platform,
            "last_crawled_at": row["last_crawled_at"].isoformat() if row else None,
            "pages_count": row["pages_count"] if row else pages_count,
            "status": row["crawl_status"] if row else status,
            "message": f"Registry updated for '{platform}': {pages_count} pages, status={status}",
        }

    except Exception as e:
        logger.exception("update_crawl_registry failed")
        return {"success": False, "error": str(e)}
