"""
Vault Export Sessions — Export agent memory captures as vault-ready .md content.

Reads recent session summaries from agent_memory_captures and returns them
formatted as vault notes. The agent then writes them to the vault filesystem
and calls vault_sync to index them.

Use after memory_capture_session to bridge memory → vault.
"""
import json
import logging
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "vault_export_sessions"

TOOL_DESCRIPTION = (
    "Export recent agent session summaries from the memory database as vault-ready .md content. "
    "Returns formatted notes that the agent should write to the vault's sessions/ folder. "
    "Use after memory_capture_session to ensure session summaries land in the vault."
)

TOOL_PARAMS = {
    "project_id": "Project UUID to export sessions for (from .galdr/.project_id)",
    "since_hours": "Export sessions from the last N hours (default 24)",
    "limit": "Max sessions to export (default 10)",
    "include_already_exported": "Include sessions that were already exported (default false)",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


def _format_session_md(capture: dict, project: dict, session: dict) -> str:
    """Format a memory capture as a vault .md note."""
    ts = capture.get("created_at") or datetime.now(timezone.utc)
    date_str = ts.strftime("%Y-%m-%d")
    time_str = ts.strftime("%H%M%S")
    conv_id = session.get("conversation_id", "unknown")
    id_short = conv_id[:8] if conv_id else "noid"
    platform = session.get("platform", "unknown")
    project_name = project.get("display_name", "unknown")
    project_id = project.get("project_id", "")

    summary = capture.get("summary", "")
    key_decisions = capture.get("key_decisions") or []
    if isinstance(key_decisions, str):
        try:
            key_decisions = json.loads(key_decisions)
        except Exception:
            key_decisions = [key_decisions]

    files_changed = capture.get("files_changed") or []
    if isinstance(files_changed, str):
        try:
            files_changed = json.loads(files_changed)
        except Exception:
            files_changed = [files_changed]

    category = capture.get("category", "")
    topic = capture.get("topic", "")

    tags = ["session", platform]
    if category:
        tags.append(category)
    if topic:
        tags.append(topic)

    md = f"""---
date: {date_str}
project: {project_name}
project_id: {project_id}
type: session
ingestion_type: session
source: {platform}/memory
conversation_id: {conv_id}
platform: {platform}
topics: [{', '.join(tags)}]
---

# Session: {project_name} ({date_str})

{summary}
"""

    if key_decisions:
        md += "\n## Key Decisions\n\n"
        for d in key_decisions:
            md += f"- {d}\n"

    if files_changed:
        md += "\n## Files Changed\n\n"
        for f in files_changed:
            md += f"- `{f}`\n"

    filename = f"{date_str}_{time_str}_{id_short}.md"
    rel_path = f"projects/{project_name}/sessions/{filename}"

    return {"filename": filename, "rel_path": rel_path, "content": md}


async def execute(
    project_id: str,
    since_hours: int = 24,
    limit: int = 10,
    include_already_exported: bool = False,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not project_id:
        return {"success": False, "error": "project_id is required"}

    limit = min(max(1, int(limit)), 50)

    try:
        hours = max(1, int(since_hours))
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT c.id AS capture_id, c.summary, c.key_decisions, c.files_changed,
                       c.category, c.topic, c.created_at,
                       s.conversation_id, s.platform, s.loop_count,
                       p.project_id, p.display_name
                FROM agent_memory_captures c
                JOIN agent_sessions s ON c.session_id = s.id
                JOIN agent_projects p ON c.project_id = p.id
                WHERE p.project_id = %s
                  AND c.created_at >= NOW() - make_interval(hours => %s)
                ORDER BY c.created_at DESC
                LIMIT %s
            """, (project_id, hours, limit))
            rows = cur.fetchall()
    except Exception as e:
        _logger.error(f"Failed to query sessions: {e}")
        return {"success": False, "error": str(e)}

    if not rows:
        return {"success": True, "count": 0, "notes": [], "message": "No new sessions to export"}

    notes = []
    for row in rows:
        capture = {
            "summary": row.get("summary", ""),
            "key_decisions": row.get("key_decisions"),
            "files_changed": row.get("files_changed"),
            "category": row.get("category", ""),
            "topic": row.get("topic", ""),
            "created_at": row.get("created_at", datetime.now(timezone.utc)),
        }
        project = {
            "project_id": row.get("project_id", ""),
            "display_name": row.get("display_name", ""),
        }
        session = {
            "conversation_id": row.get("conversation_id", ""),
            "platform": row.get("platform", ""),
        }
        note = _format_session_md(capture, project, session)
        note["capture_id"] = row.get("capture_id")
        notes.append(note)

    return {
        "success": True,
        "count": len(notes),
        "notes": notes,
        "instructions": "Write each note to the vault at the rel_path shown, then call vault_sync for each.",
    }
