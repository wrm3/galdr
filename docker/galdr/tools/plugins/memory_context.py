"""
memory_context — build a token-budgeted context block for session-start injection.
"""
import logging
from typing import Optional

from ._agent_memory_shared import init, MAX_CONTEXT_TOKENS

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_context"
TOOL_DESCRIPTION = (
    "Retrieve a token-budgeted context block for injecting into session-start. "
    "Returns recent session summaries and key past decisions, formatted for AI context. "
    "Call this from session-start.ps1 (Cursor) or session start hooks to pre-brief the agent."
)
TOOL_PARAMS = {
    "project_id":  "Project UUID from .galdr/.project_id",
    "user_id":     "User ID to scope sessions to (optional — returns all users if omitted)",
    "max_tokens":  f"Token budget for output (default: {MAX_CONTEXT_TOKENS})",
    "recent_n":    "Number of recent sessions to include (default: 3)",
}


def setup(context: dict):
    init(context)


def execute(
    project_id: str,
    user_id: Optional[str] = None,
    max_tokens: int = MAX_CONTEXT_TOKENS,
    recent_n: int = 3,
) -> dict:
    from ._agent_memory_shared import _db
    if not _db:
        return {"success": False, "error": "Database not available"}

    recent_n = max(1, min(recent_n, 10))
    max_tokens = max(500, min(max_tokens, 8000))
    approx_chars = max_tokens * 4

    # Fetch recent sessions
    sql = """
        SELECT s.conversation_id, s.platform, s.session_summary, s.ended_at,
               COUNT(t.id) AS turn_count
        FROM agent_sessions s
        JOIN agent_projects p ON p.id = s.project_id
        LEFT JOIN agent_turns t ON t.session_id = s.id
        WHERE p.project_id = %s
    """
    params: list = [project_id]
    if user_id:
        sql += " AND s.user_id = %s"
        params.append(user_id)
    sql += """
        GROUP BY s.id
        ORDER BY s.ended_at DESC NULLS LAST
        LIMIT %s
    """
    params.append(recent_n)
    sessions = []
    with _db.get_cursor() as cur:
            cur.execute(sql, params)
            for row in cur.fetchall():
                sessions.append({
                    "conversation_id": row["conversation_id"],
                    "platform":  row["platform"],
                    "summary":   row["session_summary"],
                    "ended_at":  str(row["ended_at"])[:16] if row["ended_at"] else "unknown",
                    "turn_count": row["turn_count"],
                })

    # Fetch recent key decisions from active captures
    cap_sql = """
        SELECT c.key_decisions, c.files_changed, c.created_at
        FROM agent_memory_captures c
        JOIN agent_sessions s ON s.id = c.session_id
        JOIN agent_projects p ON p.id = c.project_id
        WHERE p.project_id = %s
          AND c.key_decisions IS NOT NULL AND c.key_decisions != ''
    """
    cap_params: list = [project_id]
    if user_id:
        cap_sql += " AND c.user_id = %s"
        cap_params.append(user_id)
    cap_sql += " ORDER BY c.created_at DESC LIMIT 5"
    caps = []
    with _db.get_cursor() as cur:
            cur.execute(cap_sql, cap_params)
            caps = cur.fetchall()

    lines: list[str] = [
        f"## Agent Memory — {project_id}",
        "",
    ]

    if not sessions:
        lines.append("No previous sessions recorded for this project.")
    else:
        lines.append(f"### Recent Sessions (last {len(sessions)})")
        for s in sessions:
            ts = s["ended_at"]
            plat = s["platform"] or "?"
            turns = s["turn_count"]
            summ = s["summary"] or "(no summary)"
            lines.append(f"\n**{ts} [{plat}]** — {turns} turns")
            lines.append(summ)

    if caps:
        lines.append("\n### Key Decisions (Recent)")
        for cap in caps:
            ts = str(cap["created_at"])[:16]
            lines.append(f"\n**{ts}:** {cap['key_decisions']}")
            if cap["files_changed"]:
                lines.append(f"Files: {cap['files_changed']}")

    context_text = "\n".join(lines)
    if len(context_text) > approx_chars:
        context_text = (
            context_text[:approx_chars]
            + "\n\n[...memory truncated to fit token budget]"
        )

    return {
        "success": True,
        "project_id": project_id,
        "context": context_text,
        "approx_tokens": len(context_text) // 4,
        "sessions_included": len(sessions),
    }
