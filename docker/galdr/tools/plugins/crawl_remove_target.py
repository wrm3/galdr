"""
crawl_remove_target — Remove a custom crawl target.
"""
import logging

TOOL_NAME = "crawl_remove_target"
TOOL_DESCRIPTION = (
    "Remove a custom crawl target by name. "
    "Built-in targets (cursor, claude, gemini) can also be removed if desired."
)
TOOL_PARAMS = {
    "name": "Name of the target to remove",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(name: str) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not name or not name.strip():
        return {"success": False, "error": "name is required"}

    name = name.strip().lower()

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM crawl_targets WHERE name = %s RETURNING id",
                    (name,),
                )
                row = cur.fetchone()
                conn.commit()

        if row:
            return {
                "success": True,
                "name": name,
                "message": f"Target '{name}' removed.",
            }
        else:
            return {
                "success": False,
                "error": f"Target '{name}' not found.",
            }
    except Exception as e:
        _logger.error("Failed to remove crawl target: %s", e)
        return {"success": False, "error": str(e)}
