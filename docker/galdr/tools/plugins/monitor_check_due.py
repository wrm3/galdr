"""
monitor_check_due — Return monitors that are overdue for a check.

Used by the heartbeat scheduler and web UI to find monitors that need checking.
"""
import logging
from datetime import datetime, timezone

TOOL_NAME = "monitor_check_due"

TOOL_DESCRIPTION = (
    "Return content monitors that are overdue for a check based on their schedule. "
    "Used by the heartbeat scheduler to trigger periodic re-ingestion."
)

TOOL_PARAMS = {
    "limit": "Max monitors to return (default: 50)",
}

_db = None
_logger = logging.getLogger(__name__)

SCHEDULE_INTERVALS = {
    "hourly": "1 hour",
    "daily": "1 day",
    "weekly": "7 days",
    "monthly": "30 days",
}


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(limit: int = 50) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    try:
        with _db.get_cursor() as cur:
            cur.execute(
                """
                SELECT id, name, monitor_type, url, schedule, last_checked_at, config
                FROM content_monitors
                WHERE enabled = true
                  AND (
                    last_checked_at IS NULL
                    OR (schedule = 'hourly'  AND last_checked_at < NOW() - INTERVAL '1 hour')
                    OR (schedule = 'daily'   AND last_checked_at < NOW() - INTERVAL '1 day')
                    OR (schedule = 'weekly'  AND last_checked_at < NOW() - INTERVAL '7 days')
                    OR (schedule = 'monthly' AND last_checked_at < NOW() - INTERVAL '30 days')
                  )
                ORDER BY last_checked_at ASC NULLS FIRST
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()

        due = []
        for row in rows:
            if isinstance(row, dict):
                r = row
            else:
                r = {
                    "id": row[0], "name": row[1], "monitor_type": row[2],
                    "url": row[3], "schedule": row[4], "last_checked_at": row[5],
                    "config": row[6],
                }
            if r.get("last_checked_at") and hasattr(r["last_checked_at"], "isoformat"):
                r["last_checked_at"] = r["last_checked_at"].isoformat()
            due.append(r)

        return {"success": True, "count": len(due), "due_monitors": due}
    except Exception as e:
        _logger.error("Failed to check due monitors: %s", e)
        return {"success": False, "error": str(e)}
