"""
monitor_add — Add a content monitor for scheduled checking.

Supports playlist (daily), docs (weekly), github_repo (weekly), and url (monthly)
monitoring. The web UI and heartbeat scheduler use monitor_check_due to find
overdue monitors and trigger re-ingestion.
"""
import json
import logging
from typing import Optional

TOOL_NAME = "monitor_add"

TOOL_DESCRIPTION = (
    "Add a content monitor for scheduled checking. Supports YouTube playlists "
    "(daily new video detection), docs sites (weekly re-crawl), GitHub repos "
    "(weekly commit check), and URLs (monthly change detection). "
    "Example: monitor_add(name='ai-playlist', monitor_type='playlist', "
    "url='https://youtube.com/playlist?list=PLxxx', schedule='daily')"
)

TOOL_PARAMS = {
    "name": "Unique name for this monitor (e.g. 'cursor-docs', 'ai-playlist')",
    "monitor_type": "Type: 'playlist' | 'docs' | 'github_repo' | 'url'",
    "url": "URL to monitor",
    "schedule": "Check frequency: 'hourly' | 'daily' | 'weekly' | 'monthly' (default varies by type)",
    "config": "Type-specific config as JSON object (optional). E.g. {max_pages: 100} for docs",
    "user_id": "User creating the monitor (optional)",
}

_db = None
_logger = logging.getLogger(__name__)

DEFAULT_SCHEDULES = {
    "playlist": "daily",
    "docs": "weekly",
    "github_repo": "weekly",
    "url": "monthly",
}


def setup(context: dict):
    global _db
    _db = context.get("db")


def execute(
    name: str,
    monitor_type: str,
    url: str,
    schedule: Optional[str] = None,
    config: Optional[dict] = None,
    user_id: Optional[str] = None,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not name or not name.strip():
        return {"success": False, "error": "name is required"}
    if monitor_type not in ("playlist", "docs", "github_repo", "url"):
        return {"success": False, "error": f"Invalid monitor_type: {monitor_type}. Must be playlist|docs|github_repo|url"}
    if not url or not url.strip():
        return {"success": False, "error": "url is required"}

    name = name.strip().lower().replace(" ", "-")
    schedule = schedule or DEFAULT_SCHEDULES.get(monitor_type, "weekly")
    config = config or {}

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO content_monitors (name, monitor_type, url, schedule, config, created_by)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s)
                    ON CONFLICT (name) DO UPDATE
                        SET monitor_type = EXCLUDED.monitor_type,
                            url          = EXCLUDED.url,
                            schedule     = EXCLUDED.schedule,
                            config       = EXCLUDED.config,
                            created_by   = EXCLUDED.created_by,
                            enabled      = true
                    RETURNING id
                    """,
                    (name, monitor_type, url.strip(), schedule, json.dumps(config), user_id),
                )
                monitor_id = cur.fetchone()[0]
                conn.commit()

        return {
            "success": True,
            "monitor_id": monitor_id,
            "name": name,
            "monitor_type": monitor_type,
            "url": url.strip(),
            "schedule": schedule,
            "message": f"Monitor '{name}' created. It will be checked {schedule}.",
        }
    except Exception as e:
        _logger.error("Failed to add monitor: %s", e)
        return {"success": False, "error": str(e)}
