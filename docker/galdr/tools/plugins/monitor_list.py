"""
monitor_list — List all content monitors with status.
"""
import logging

TOOL_NAME = "monitor_list"

TOOL_DESCRIPTION = (
    "List all content monitors with their status, schedule, and last check time. "
    "Optionally filter by type or enabled status."
)

TOOL_PARAMS = {
    "monitor_type": "Filter by type: 'playlist' | 'docs' | 'github_repo' | 'url' (optional)",
    "enabled_only": "Only show enabled monitors (default: true)",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(
    monitor_type: str = None,
    enabled_only: bool = True,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    conditions = []
    params = []

    if enabled_only:
        conditions.append("enabled = true")
    if monitor_type:
        conditions.append("monitor_type = %s")
        params.append(monitor_type)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    try:
        with _db.get_cursor() as cur:
            cur.execute(
                f"""
                SELECT id, name, monitor_type, url, schedule, enabled,
                       last_checked_at, last_change_at, check_state, config, created_at
                FROM content_monitors
                {where}
                ORDER BY name
                """,
                params,
            )
            rows = cur.fetchall()

        monitors = []
        for row in rows:
            if isinstance(row, dict):
                r = row
            else:
                r = {
                    "id": row[0], "name": row[1], "monitor_type": row[2],
                    "url": row[3], "schedule": row[4], "enabled": row[5],
                    "last_checked_at": row[6], "last_change_at": row[7],
                    "check_state": row[8], "config": row[9], "created_at": row[10],
                }
            for k in ("last_checked_at", "last_change_at", "created_at"):
                if r.get(k) and hasattr(r[k], "isoformat"):
                    r[k] = r[k].isoformat()
            monitors.append(r)

        return {"success": True, "count": len(monitors), "monitors": monitors}
    except Exception as e:
        _logger.error("Failed to list monitors: %s", e)
        return {"success": False, "error": str(e)}
