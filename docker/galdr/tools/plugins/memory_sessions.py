"""
memory_sessions — list recent agent sessions for a project.
"""
import logging
from typing import Optional

from ._agent_memory_shared import init

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_sessions"
TOOL_DESCRIPTION = (
    "List recent agent sessions for a project. "
    "Use to review what was worked on recently across all IDE platforms."
)
TOOL_PARAMS = {
    "project_id": "Project UUID from .galdr/.project_id (required)",
    "user_id":    "Filter to a specific user (optional — returns all users if omitted)",
    "limit":      "Max sessions to return (1-50, default: 20)",
    "platform":   "Filter by platform: 'cursor' | 'claude_code' | 'antigravity' | 'vscode' (optional)",
}


def setup(context: dict):
    init(context)


def execute(
    project_id: str,
    user_id: Optional[str] = None,
    limit: int = 20,
    platform: Optional[str] = None,
) -> dict:
    from ._agent_memory_shared import _db
    if not _db:
        return {"success": False, "error": "Database not available"}

    limit = max(1, min(limit, 50))
    sql = """
        SELECT
            s.id, s.conversation_id, s.platform, s.capture_tier,
            s.status, s.loop_count, s.session_summary,
            s.ended_at, s.created_at,
            COUNT(t.id) AS turn_count,
            COUNT(c.id) AS capture_count
        FROM agent_sessions s
        JOIN agent_projects p ON p.id = s.project_id
        LEFT JOIN agent_turns t ON t.session_id = s.id
        LEFT JOIN agent_memory_captures c ON c.session_id = s.id
        WHERE p.project_id = %s
    """
    params: list = [project_id]
    if user_id:
        sql += " AND s.user_id = %s"; params.append(user_id)
    if platform:
        sql += " AND s.platform = %s"; params.append(platform)
    sql += " GROUP BY s.id ORDER BY s.ended_at DESC NULLS LAST LIMIT %s"
    params.append(limit)

    sessions = []
    with _db.get_cursor() as cur:
            cur.execute(sql, params)
            for row in cur.fetchall():
                sessions.append({
                    "session_id":    row["id"],
                    "conversation_id": row["conversation_id"],
                    "platform":      row["platform"],
                    "capture_tier":  row["capture_tier"],
                    "status":        row["status"],
                    "loop_count":    row["loop_count"],
                    "summary":       row["session_summary"],
                    "ended_at":      str(row["ended_at"]),
                    "created_at":    str(row["created_at"]),
                    "turn_count":    row["turn_count"],
                    "capture_count": row["capture_count"],
                })

    return {
        "success": True,
        "project_id": project_id,
        "sessions": sessions,
        "total": len(sessions),
    }
