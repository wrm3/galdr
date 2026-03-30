"""
crawl_list_targets — List all configured crawl targets.
"""
import logging
from typing import Optional

TOOL_NAME = "crawl_list_targets"
TOOL_DESCRIPTION = (
    "List all configured documentation crawl targets — both built-in platform targets "
    "and custom targets added via crawl_add_target. Shows URLs, crawl limits, "
    "visibility, and last crawl time."
)
TOOL_PARAMS = {
    "visibility": "Filter by visibility: 'public' | 'internal' | 'all' (default: 'all')",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(
    visibility: str = "all",
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    sql = """
        SELECT name, urls, max_pages, max_depth, visibility,
               created_by, last_crawled_at, created_at
        FROM crawl_targets
    """
    params: list = []
    if visibility in ("public", "internal"):
        sql += " WHERE visibility = %s"
        params.append(visibility)
    sql += " ORDER BY name"

    targets = []
    try:
        with _db.get_cursor() as cur:
            cur.execute(sql, params)
            for row in cur.fetchall():
                targets.append({
                    "name": row["name"],
                    "urls": row["urls"],
                    "max_pages": row["max_pages"],
                    "max_depth": row["max_depth"],
                    "visibility": row["visibility"],
                    "created_by": row["created_by"],
                    "last_crawled_at": str(row["last_crawled_at"]) if row["last_crawled_at"] else None,
                    "created_at": str(row["created_at"]) if row["created_at"] else None,
                })
    except Exception as e:
        _logger.error("Failed to list crawl targets: %s", e)
        return {"success": False, "error": str(e)}

    return {
        "success": True,
        "targets": targets,
        "total": len(targets),
    }
