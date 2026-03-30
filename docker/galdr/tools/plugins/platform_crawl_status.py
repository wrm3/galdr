"""
platform_crawl_status — Check status of server-side crawl4ai crawls.
"""
import logging
from typing import Optional

TOOL_NAME = "platform_crawl_status"
TOOL_DESCRIPTION = (
    "Check the status of server-side documentation crawls. "
    "Returns active, completed, and failed crawls with page counts and timing."
)
TOOL_PARAMS = {
    "crawl_id": "Specific crawl ID to check (optional — returns all if omitted)",
    "target":   "Filter by target name (optional)",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(
    crawl_id: Optional[str] = None,
    target: Optional[str] = None,
) -> dict:
    from .platform_crawl_trigger import _active_crawls

    results = []
    for cid, state in _active_crawls.items():
        if crawl_id and cid != crawl_id:
            continue
        if target and state.get("target") != target:
            continue
        results.append(state.copy())

    # Also check DB for last crawl times
    db_targets = []
    if _db:
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT name, last_crawled_at, max_pages, max_depth, visibility
                    FROM crawl_targets
                    ORDER BY name
                    """
                )
                for row in cur.fetchall():
                    db_targets.append({
                        "name": row["name"],
                        "last_crawled_at": str(row["last_crawled_at"]) if row["last_crawled_at"] else None,
                        "max_pages": row["max_pages"],
                        "max_depth": row["max_depth"],
                        "visibility": row["visibility"],
                    })
        except Exception as e:
            _logger.debug("Failed to read crawl_targets: %s", e)

    return {
        "success": True,
        "active_crawls": results,
        "total_active": len(results),
        "configured_targets": db_targets,
    }
