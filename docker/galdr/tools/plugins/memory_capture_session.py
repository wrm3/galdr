"""
memory_capture_session — Tier 2 (active): agent self-reports session summary.
Use at end of every Antigravity / VS Code session.
"""
import logging
import os
from datetime import datetime, timezone
from typing import Optional

from ._agent_memory_shared import (
    init, upsert_project, ensure_session, embed, embed_str
)

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_capture_session"
TOOL_DESCRIPTION = (
    "CALL THIS AT THE END OF EVERY SESSION to preserve context for future sessions. "
    "Directly captures an agent-written session summary. "
    "Use for Antigravity/Gemini, VS Code, or any platform without automatic hooks. "
    "No file reading required — you provide the summary directly."
)
TOOL_PARAMS = {
    "summary":         "What was accomplished this session (2-6 sentences)",
    "project_path":    "Absolute path to the project root",
    "project_id":      "Stable project UUID from .galdr/.project_id. Use 'unknown' if unavailable.",
    "platform":        "IDE platform: 'cursor' | 'claude_code' | 'antigravity' | 'vscode'",
    "key_decisions":   "Architectural or design decisions made (optional)",
    "files_changed":   "Comma-separated list of files modified (optional)",
    "user_id":         "User ID from ~/.galdr/user_config.json (optional)",
    "machine_id":      "Machine GUID or Antigravity installation_id (optional)",
    "conversation_id": "Session ID if known (optional — auto-generated if omitted)",
}


def setup(context: dict):
    init(context)


def execute(
    summary: str,
    project_path: str,
    project_id: Optional[str] = None,
    platform: str = "unknown",
    key_decisions: Optional[str] = None,
    files_changed: Optional[str] = None,
    user_id: Optional[str] = None,
    machine_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> dict:
    from ._agent_memory_shared import _db
    if not _db:
        return {"success": False, "error": "Database not available"}

    project_id = project_id or "unknown"
    display_name = os.path.basename(project_path.rstrip("/\\")) if project_path else ""

    if not conversation_id:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        conversation_id = f"active_{project_id}_{ts}"

    proj_row_id = upsert_project(
        project_id, user_id or "", machine_id or "", project_path, display_name
    )
    session_id = ensure_session(
        conversation_id, proj_row_id, platform, "active", "completed", None,
        user_id=user_id,
    )

    emb = embed(f"{summary} {key_decisions or ''}")

    with _db.get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_memory_captures
                (session_id, project_id, summary, key_decisions,
                 files_changed, embedding, user_id)
            VALUES (%s, %s, %s, %s, %s, %s::vector, %s)
            """,
            (session_id, proj_row_id, summary, key_decisions,
             files_changed, embed_str(emb), user_id),
        )
        cur.execute(
            "UPDATE agent_sessions SET session_summary=%s WHERE id=%s",
            (summary, session_id),
        )

    return {
        "success": True,
        "session_id": session_id,
        "conversation_id": conversation_id,
        "project_id": project_id,
        "platform": platform,
        "capture_tier": "active",
        "message": "Session captured. Context preserved for future sessions.",
    }
