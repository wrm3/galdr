"""
memory_capture_insight — Tier 2 (active): explicit structured insight capture.

Call this tool when you learn something worth remembering across sessions:
  - A user preference (code style, naming conventions, formatting)
  - A procedure you should follow (how to deploy, test pattern, git flow)
  - A correction (something you did wrong, should avoid in future)
  - An architectural decision and its rationale
  - Project context that took effort to establish

Inspired by letta-code's structured memory categories.
"""
import difflib
import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional

from ._agent_memory_shared import init, upsert_project, ensure_session, embed, embed_str

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_capture_insight"
TOOL_DESCRIPTION = (
    "Capture a specific insight, preference, procedure, or decision for long-term memory. "
    "Call this when you learn something worth preserving across sessions: user preferences, "
    "how-to procedures, corrections to avoid, architectural decisions. "
    "Each insight is stored under a topic tag and updated if that topic already has a capture — "
    "so the memory stays current rather than accumulating duplicates. "
    "BEST PRACTICE: Call at session end after memory_capture_session, or mid-session when you "
    "learn something important."
)
TOOL_PARAMS = {
    "insight": (
        "The insight to capture (1-4 sentences). Be specific and actionable. "
        "Example: 'Use `uv run` instead of `python` in this project. The venv is managed by UV.'"
    ),
    "category": (
        "Type of insight: "
        "'procedure' (how to do something), "
        "'preference' (user likes/dislikes), "
        "'correction' (mistake to avoid), "
        "'decision' (architectural choice + rationale), "
        "'context' (project background), "
        "'general' (anything else)"
    ),
    "topic": (
        "Short label for grouping related insights (e.g. 'git workflow', 'code style', "
        "'deploy process', 'test patterns'). Reusing the same topic UPDATES the insight "
        "instead of creating a duplicate."
    ),
    "project_id": "Stable project UUID from .galdr/.project_id. Use 'unknown' if unavailable.",
    "project_path": "Absolute path to the project root",
    "scope": (
        "Who this applies to: 'project' (this codebase only), "
        "'user' (this user across all projects), "
        "'session' (just this session), "
        "'global' (always applies)"
    ),
    "platform": "IDE platform: 'cursor' | 'claude_code' | 'antigravity' | 'vscode'",
    "user_id": "User ID from ~/.galdr/user_config.json (optional)",
    "machine_id": "Machine GUID (optional)",
}


def setup(context: dict):
    init(context)


def execute(
    insight: str,
    category: str = "general",
    topic: Optional[str] = None,
    project_id: Optional[str] = None,
    project_path: str = "",
    scope: str = "project",
    platform: str = "unknown",
    user_id: Optional[str] = None,
    machine_id: Optional[str] = None,
) -> dict:
    from ._agent_memory_shared import _db
    if not _db:
        return {"success": False, "error": "Database not available"}

    # Validate category / scope
    valid_categories = {"procedure", "preference", "context", "correction", "decision", "general"}
    valid_scopes = {"project", "user", "session", "global"}
    if category not in valid_categories:
        category = "general"
    if scope not in valid_scopes:
        scope = "project"

    project_id = project_id or "unknown"
    display_name = os.path.basename(project_path.rstrip("/\\")) if project_path else project_id

    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    conversation_id = f"insight_{project_id}_{ts}"

    proj_row_id = upsert_project(
        project_id, user_id or "", machine_id or "", project_path, display_name
    )
    session_id = ensure_session(
        conversation_id, proj_row_id, platform, "active", "completed", None,
        user_id=user_id,
    )

    emb_vec = embed(f"{category} {topic or ''} {insight}")

    # ── Diff tracking: look for existing capture with same topic ────────────
    prev_content = None
    diff_text = None
    action = "created"

    if topic:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, summary FROM agent_memory_captures
                    WHERE project_id = %s AND topic = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (proj_row_id, topic),
                )
                row = cur.fetchone()

        if row:
            prev_content = row[1] if isinstance(row, dict) else row[1]
            if prev_content and prev_content.strip() != insight.strip():
                diff_lines = list(difflib.unified_diff(
                    prev_content.splitlines(keepends=True),
                    insight.splitlines(keepends=True),
                    fromfile=f"{topic} (before)",
                    tofile=f"{topic} (after)",
                    lineterm="",
                ))
                diff_text = "".join(diff_lines) if diff_lines else None
                action = "updated"
            else:
                # Content identical — skip duplicate
                return {
                    "success": True,
                    "action": "skipped_duplicate",
                    "topic": topic,
                    "message": f"Insight for topic '{topic}' already up to date — no changes stored.",
                }

    # ── Insert new capture ────────────────────────────────────────────────────
    with _db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO agent_memory_captures
                    (session_id, project_id, summary, key_decisions,
                     files_changed, embedding,
                     category, scope, topic, prev_content, diff_text, user_id)
                VALUES (%s, %s, %s, %s, %s, %s::vector, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    session_id, proj_row_id,
                    insight,             # summary = the insight text
                    None,                # key_decisions (N/A for insight captures)
                    None,                # files_changed
                    embed_str(emb_vec),
                    category, scope,
                    topic,
                    prev_content,
                    diff_text,
                    user_id,
                ),
            )
            capture_id = cur.fetchone()[0]
            conn.commit()

    logger.info(
        "memory_capture_insight: %s category=%s topic=%s project=%s",
        action, category, topic, project_id,
    )

    result = {
        "success": True,
        "capture_id": capture_id,
        "action": action,
        "category": category,
        "scope": scope,
        "topic": topic,
        "project_id": project_id,
    }

    if action == "updated" and diff_text:
        result["diff_summary"] = f"Updated existing '{topic}' insight ({len(diff_text)} chars changed)"

    result["message"] = (
        f"Insight {action} under category '{category}'"
        + (f" / topic '{topic}'" if topic else "")
        + ". Will be included in future session context."
    )

    return result
