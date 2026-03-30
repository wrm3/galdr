"""
memory_ingest_session — Tier 1 (passive): ingest session from IDE file.
Called automatically by Cursor / Claude Code hooks.
"""
import json
import logging
import os
from typing import Optional

from ._agent_memory_shared import (
    init, upsert_project, ensure_session, insert_turn
)

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_ingest_session"
TOOL_DESCRIPTION = (
    "Ingest a completed IDE session into the agent memory store. "
    "Called automatically by Cursor/Claude Code hooks after a session ends. "
    "Provide either raw_turns (list of {user, agent} dicts) or a raw_jsonl string. "
    "The session is deduplicated by content hash — safe to call multiple times."
)
TOOL_PARAMS = {
    "conversation_id": "Unique session ID from the IDE hook payload",
    "project_id":      "Stable project UUID from .galdr/.project_id (e.g. 'proj_a1b2c3d4')",
    "platform":        "IDE platform: 'cursor' | 'claude_code' | 'antigravity' | 'vscode'",
    "raw_turns":       "List of {user: str, agent: str} exchange dicts (optional)",
    "raw_jsonl":       "Raw JSONL string of conversation turns (optional)",
    "user_id":         "User ID from ~/.galdr/user_config.json (optional)",
    "machine_id":      "Machine GUID or Antigravity installation_id (optional)",
    "project_path":    "Absolute path to project root (informational, optional)",
    "status":          "Session status string from hook payload (optional)",
    "loop_count":      "Number of agent loops from Cursor hook (optional)",
}


def setup(context: dict):
    init(context)


def execute(
    conversation_id: str,
    project_id: str,
    platform: str,
    raw_turns: Optional[list] = None,
    raw_jsonl: Optional[str] = None,
    user_id: Optional[str] = None,
    machine_id: Optional[str] = None,
    project_path: Optional[str] = None,
    status: Optional[str] = None,
    loop_count: Optional[int] = None,
) -> dict:
    from ._agent_memory_shared import _db
    if not _db:
        return {"success": False, "error": "Database not available"}

    project_path = project_path or ""
    display_name = os.path.basename(project_path.rstrip("/\\")) if project_path else ""
    proj_row_id = upsert_project(
        project_id, user_id or "", machine_id or "", project_path, display_name
    )
    session_id = ensure_session(
        conversation_id, proj_row_id, platform, "passive", status, loop_count,
        user_id=user_id,
    )

    turns: list = raw_turns or []
    if raw_jsonl and not turns:
        for line in raw_jsonl.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    u = obj.get("user") or obj.get("human") or obj.get("input") or ""
                    a = obj.get("agent") or obj.get("assistant") or obj.get("output") or ""
                    if u or a:
                        turns.append({"user": str(u), "agent": str(a)})
            except json.JSONDecodeError:
                pass

    inserted = skipped = 0
    for i, turn in enumerate(turns):
        u = str(turn.get("user") or "")
        a = str(turn.get("agent") or "")
        if not u and not a:
            continue
        if insert_turn(session_id, i, u, a, platform, "passive", user_id=user_id):
            inserted += 1
        else:
            skipped += 1

    return {
        "success": True,
        "session_id": session_id,
        "conversation_id": conversation_id,
        "project_id": project_id,
        "platform": platform,
        "turns_inserted": inserted,
        "turns_skipped_duplicate": skipped,
    }
