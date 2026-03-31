"""
monitor_remove — Remove a content monitor by name.
"""
import logging

TOOL_NAME = "monitor_remove"

TOOL_DESCRIPTION = "Remove a content monitor by name. This stops all scheduled checks for the monitor."

TOOL_PARAMS = {
    "name": "Name of the monitor to remove",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(name: str) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not name:
        return {"success": False, "error": "name is required"}

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM content_monitors WHERE name = %s", (name.strip().lower(),))
                deleted = cur.rowcount
                conn.commit()

        if deleted:
            return {"success": True, "name": name, "message": f"Monitor '{name}' removed."}
        return {"success": False, "error": f"Monitor '{name}' not found."}
    except Exception as e:
        _logger.error("Failed to remove monitor: %s", e)
        return {"success": False, "error": str(e)}
