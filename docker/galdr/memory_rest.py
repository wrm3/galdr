"""
memory_rest.py — Lightweight REST bridge for agent memory operations.

Provides simple HTTP endpoints alongside the MCP SSE server so that
non-MCP clients (Cursor hooks, Claude Code hooks, shell scripts) can
call memory functions without implementing the full MCP SSE protocol.

Endpoints:
  POST /memory/ingest    — Tier-1 passive capture (raw turns from file adapters)
  POST /memory/capture   — Tier-2 active capture (agent self-reports session summary)
  POST /memory/insight   — Tier-2 active capture (structured insight with category/topic)
  GET  /memory/context   — Return token-budgeted context for session-start hook
  GET  /memory/health    — Quick health check

All endpoints accept/return JSON.
"""

import difflib
import logging
from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

logger = logging.getLogger(__name__)

_shared: dict = {
    "db": None,
    "embedding_gen": None,
    "config": None,
}


def init_memory_rest(db, embedding_generator, config) -> None:
    """Called from server.py after components are initialized."""
    _shared["db"] = db
    _shared["embedding_gen"] = embedding_generator
    _shared["config"] = config
    logger.info("memory_rest: REST bridge initialized (db=%s)", "connected" if db else "None")


def _get_shared():
    """Return (db, embedding_gen) or raise RuntimeError if not ready."""
    db = _shared["db"]
    eg = _shared["embedding_gen"]
    if db is None:
        raise RuntimeError("PostgreSQL not configured — memory REST bridge unavailable")
    return db, eg


def _init_shared_module(db, eg):
    """Initialize the _agent_memory_shared helper with the current DB/embedding objects."""
    from galdr.tools.plugins._agent_memory_shared import init as mem_init
    mem_init({"db": db, "embedding_generator": eg})


# ---------------------------------------------------------------------------
# /memory/ingest  — Tier-1 passive capture
# ---------------------------------------------------------------------------

async def handle_memory_ingest(request: Request) -> JSONResponse:
    """
    POST /memory/ingest

    Body (JSON):
      project_id      str  — stable project UUID (.galdr/.project_id)
      conversation_id str  — unique session ID from the IDE
      platform        str  — 'cursor' | 'claude_code' | 'vscode' | 'gemini'
      project_path    str  — absolute path to the project root
      display_name    str  — human-readable project name (optional)
      user_id         str  — from ~/.galdr/user_config.json (optional)
      machine_id      str  — from ~/.galdr/user_config.json (optional)
      loop_count      int  — number of agent loops in the session (optional)
      status          str  — 'completed' | 'partial' (optional)
      turns           list — [{user, agent}] raw turn objects

    Returns: {success, ingested_turns, session_id}
    """
    try:
        db, eg = _get_shared()
    except RuntimeError as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=503)

    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Invalid JSON: {e}"}, status_code=400)

    project_id = body.get("project_id")
    conversation_id = body.get("conversation_id")
    platform = body.get("platform", "cursor")
    turns = body.get("turns", [])

    if not project_id or not conversation_id:
        return JSONResponse(
            {"success": False, "error": "project_id and conversation_id are required"},
            status_code=400,
        )

    project_path = body.get("project_path", "")
    display_name = body.get("display_name") or (project_path.split("\\")[-1] or project_path.split("/")[-1] or project_id)
    user_id = body.get("user_id", "")
    machine_id = body.get("machine_id", "")
    loop_count = body.get("loop_count", len(turns))
    status = body.get("status", "completed")

    try:
        from galdr.tools.plugins._agent_memory_shared import (
            init as mem_init,
            upsert_project,
            ensure_session,
            content_hash,
            summarise_turn,
            embed,
        )

        mem_init({"db": db, "embedding_generator": eg})

        # Upsert project and session (each uses get_cursor() internally → safe)
        project_db_id = upsert_project(
            project_id=project_id,
            user_id=user_id,
            machine_id=machine_id,
            project_path=project_path,
            display_name=display_name,
        )

        session_db_id = ensure_session(
            conversation_id=conversation_id,
            project_row_id=project_db_id,
            platform=platform,
            capture_tier="passive",
            status=status,
            loop_count=loop_count,
        )

        # Pre-compute hashes + embeddings for all turns BEFORE acquiring the DB
        # connection (avoids holding it during potentially slow API calls).
        #
        # We deliberately skip per-turn LLM summarisation here: the bulk ingest
        # path embeds the raw text (user + agent combined) which is sufficient for
        # semantic search. Summaries can be generated lazily on demand.
        import json as _json

        records = []
        for idx, turn in enumerate(turns):
            user_msg_text  = turn.get("user", "")
            agent_msg_text = turn.get("agent", "")
            if not user_msg_text and not agent_msg_text:
                continue
            chash = content_hash(user_msg_text, agent_msg_text)

            # Enrich embedding text with tool names and file refs when available
            tool_names = turn.get("tool_names") or []
            file_refs  = turn.get("file_refs")  or []
            session_meta = turn.get("session_metadata") or {}

            combined_raw = " ".join(filter(None, [
                user_msg_text,
                agent_msg_text,
                " ".join(tool_names),
                " ".join(file_refs),
            ]))
            emb_vec = embed(combined_raw[:2000])

            records.append({
                "session_id":       session_db_id,
                "turn_index":       idx,
                "chash":            chash,
                "user_msg":         user_msg_text,
                "agent_resp":       agent_msg_text,
                "emb_vec":          emb_vec,
                "platform":         platform,
                "tool_names":       tool_names,
                "file_refs":        file_refs,
                "session_metadata": session_meta,
            })

        ingested = 0
        if records:
            with db.get_cursor() as cur:
                cur.execute(
                    "SELECT content_hash FROM agent_turns WHERE session_id=%s",
                    (session_db_id,),
                )
                existing = {row["content_hash"] for row in cur.fetchall()}

                for r in records:
                    if r["chash"] in existing:
                        continue

                    # Serialise arrays / JSONB for psycopg2
                    meta_json  = _json.dumps(r["session_metadata"]) if r["session_metadata"] else "{}"
                    tools_arr  = r["tool_names"] or []
                    files_arr  = r["file_refs"]  or []

                    cur.execute(
                        """
                        INSERT INTO agent_turns
                            (session_id, turn_index, content_hash,
                             user_message, agent_response,
                             llm_title, llm_description, embedding,
                             platform, capture_tier,
                             tool_names, file_refs, session_metadata)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            r["session_id"], r["turn_index"], r["chash"],
                            r["user_msg"], r["agent_resp"],
                            None, None, r["emb_vec"],   # title/desc filled lazily
                            r["platform"], "passive",
                            tools_arr, files_arr, meta_json,
                        ),
                    )
                    ingested += 1

        logger.info(
            "memory/ingest: project=%s conv=%s platform=%s turns_ingested=%d",
            project_id, conversation_id, platform, ingested,
        )

        return JSONResponse(
            {
                "success": True,
                "project_db_id": project_db_id,
                "session_db_id": session_db_id,
                "ingested_turns": ingested,
                "total_turns": len(turns),
            }
        )

    except Exception as e:
        logger.error("memory/ingest error: %s", e, exc_info=True)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ---------------------------------------------------------------------------
# /memory/capture  — Tier-2 active capture (agent self-reports session summary)
# ---------------------------------------------------------------------------

async def handle_memory_capture(request: Request) -> JSONResponse:
    """
    POST /memory/capture

    Body (JSON):
      project_id      str  — stable project UUID
      project_path    str  — absolute path to the project root
      summary         str  — agent-generated session summary (REQUIRED)
      key_decisions   str  — bullet-list of key decisions (optional)
      files_changed   str  — comma-separated list of changed files (optional)
      conversation_id str  — session ID (auto-generated if omitted)
      platform        str  — 'cursor' | 'claude_code' | 'vscode' | 'gemini'
      user_id         str  — from ~/.galdr/user_config.json (optional)
      machine_id      str  — from ~/.galdr/user_config.json (optional)

    Returns: {success, project_db_id, session_db_id, capture_id}
    """
    try:
        db, eg = _get_shared()
    except RuntimeError as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=503)

    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Invalid JSON: {e}"}, status_code=400)

    project_id = body.get("project_id")
    summary = body.get("summary")

    if not project_id or not summary:
        return JSONResponse(
            {"success": False, "error": "project_id and summary are required"},
            status_code=400,
        )

    project_path = body.get("project_path", "")
    key_decisions = body.get("key_decisions", "")
    files_changed = body.get("files_changed", "")
    conversation_id = body.get("conversation_id") or f"active-{project_id}"
    platform = body.get("platform", "cursor")
    user_id = body.get("user_id", "")
    machine_id = body.get("machine_id", "")
    display_name = body.get("display_name") or (project_path.split("\\")[-1] or project_path.split("/")[-1] or project_id)

    try:
        from galdr.tools.plugins._agent_memory_shared import (
            init as mem_init,
            upsert_project,
            ensure_session,
            embed as embed_fn,
            embed_str,
        )

        mem_init({"db": db, "embedding_generator": eg})

        project_db_id = upsert_project(
            project_id=project_id,
            user_id=user_id,
            machine_id=machine_id,
            project_path=project_path,
            display_name=display_name,
        )

        session_db_id = ensure_session(
            conversation_id=conversation_id,
            project_row_id=project_db_id,
            platform=platform,
            capture_tier="active",
            status="completed",
            loop_count=0,
        )

        # Compute embedding outside the DB transaction (avoids holding connection during API call)
        combined_text = summary
        if key_decisions:
            combined_text += f"\n\nKey Decisions:\n{key_decisions}"
        embedding_vec = embed_str(embed_fn(combined_text))

        # Update summary + insert capture record in a single cursor context
        capture_id = None
        with db.get_cursor() as cur:
            cur.execute(
                "UPDATE agent_sessions SET session_summary=%s WHERE id=%s",
                (summary, session_db_id),
            )
            cur.execute(
                """
                INSERT INTO agent_memory_captures
                    (session_id, project_id, summary, key_decisions, files_changed, embedding,
                     category, scope)
                VALUES (%s, %s, %s, %s, %s, %s, 'context', 'session')
                RETURNING id
                """,
                (session_db_id, project_db_id, summary, key_decisions, files_changed, embedding_vec),
            )
            capture_id = cur.fetchone()["id"]

        logger.info(
            "memory/capture: project=%s platform=%s capture_id=%s",
            project_id, platform, capture_id,
        )

        return JSONResponse(
            {
                "success": True,
                "project_db_id": project_db_id,
                "session_db_id": session_db_id,
                "capture_id": capture_id,
            }
        )

    except Exception as e:
        logger.error("memory/capture error: %s", e, exc_info=True)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ---------------------------------------------------------------------------
# /memory/insight  — Tier-2 active capture (structured insight with category/topic)
# ---------------------------------------------------------------------------

_VALID_CATEGORIES = {"procedure", "preference", "context", "correction", "decision", "general"}
_VALID_SCOPES = {"project", "user", "session", "global"}


async def handle_memory_insight(request: Request) -> JSONResponse:
    """
    POST /memory/insight

    Body (JSON):
      project_id   str  — stable project UUID (REQUIRED)
      insight      str  — the insight text, 1-4 sentences (REQUIRED)
      category     str  — procedure|preference|context|correction|decision|general
      scope        str  — project|user|session|global
      topic        str  — short label, e.g. 'git workflow' (enables dedup + diff)
      project_path str  — absolute path to project root (optional)
      platform     str  — 'cursor' | 'claude_code' | etc.
      user_id      str  — from user_config.json (optional)
      machine_id   str  — (optional)

    If a capture with the same project_id + topic already exists, the existing
    content is stored as prev_content and a unified diff is computed.

    Returns: {success, capture_id, action, category, scope, topic}
    """
    try:
        db, eg = _get_shared()
    except RuntimeError as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=503)

    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Invalid JSON: {e}"}, status_code=400)

    project_id = body.get("project_id")
    insight = body.get("insight", "").strip()

    if not project_id or not insight:
        return JSONResponse(
            {"success": False, "error": "project_id and insight are required"},
            status_code=400,
        )

    category = body.get("category", "general")
    if category not in _VALID_CATEGORIES:
        category = "general"
    scope = body.get("scope", "project")
    if scope not in _VALID_SCOPES:
        scope = "project"

    topic = body.get("topic") or None
    project_path = body.get("project_path", "")
    platform = body.get("platform", "cursor")
    user_id = body.get("user_id", "")
    machine_id = body.get("machine_id", "")
    display_name = body.get("display_name") or (project_path.split("\\")[-1] or project_path.split("/")[-1] or project_id)

    try:
        import json as _json
        from datetime import datetime, timezone
        from galdr.tools.plugins._agent_memory_shared import (
            init as mem_init,
            upsert_project,
            ensure_session,
            embed as embed_fn,
            embed_str,
        )

        mem_init({"db": db, "embedding_generator": eg})

        project_db_id = upsert_project(
            project_id=project_id,
            user_id=user_id,
            machine_id=machine_id,
            project_path=project_path,
            display_name=display_name,
        )

        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        conversation_id = f"insight_{project_id}_{ts}"
        session_db_id = ensure_session(
            conversation_id=conversation_id,
            project_row_id=project_db_id,
            platform=platform,
            capture_tier="active",
            status="completed",
            loop_count=0,
        )

        # Diff tracking — check for existing capture with same topic
        prev_content = None
        diff_text = None
        action = "created"

        if topic:
            with db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT id, summary FROM agent_memory_captures
                    WHERE project_id=%s AND topic=%s
                    ORDER BY created_at DESC LIMIT 1
                    """,
                    (project_db_id, topic),
                )
                row = cur.fetchone()

            if row:
                prev_content = row["summary"]
                if prev_content and prev_content.strip() == insight:
                    return JSONResponse({
                        "success": True,
                        "action": "skipped_duplicate",
                        "topic": topic,
                        "message": f"Insight for topic '{topic}' is unchanged — skipped.",
                    })
                if prev_content:
                    diff_lines = list(difflib.unified_diff(
                        prev_content.splitlines(keepends=True),
                        insight.splitlines(keepends=True),
                        fromfile=f"{topic} (before)",
                        tofile=f"{topic} (after)",
                        lineterm="",
                    ))
                    diff_text = "".join(diff_lines) if diff_lines else None
                action = "updated"

        embedding_vec = embed_str(embed_fn(f"{category} {topic or ''} {insight}"))

        with db.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO agent_memory_captures
                    (session_id, project_id, summary, key_decisions, files_changed, embedding,
                     category, scope, topic, prev_content, diff_text)
                VALUES (%s, %s, %s, NULL, NULL, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    session_db_id, project_db_id, insight, embedding_vec,
                    category, scope, topic, prev_content, diff_text,
                ),
            )
            capture_id = cur.fetchone()["id"]

        logger.info(
            "memory/insight: %s category=%s topic=%s project=%s",
            action, category, topic, project_id,
        )

        resp = {
            "success": True,
            "capture_id": capture_id,
            "action": action,
            "category": category,
            "scope": scope,
            "topic": topic,
            "project_id": project_id,
        }
        if action == "updated" and diff_text:
            resp["diff_summary"] = f"Updated '{topic}' — {len(diff_text)} chars changed"
        resp["message"] = (
            f"Insight {action} under category '{category}'"
            + (f" / topic '{topic}'" if topic else "")
            + ". Will appear in future session context."
        )
        return JSONResponse(resp)

    except Exception as e:
        logger.error("memory/insight error: %s", e, exc_info=True)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ---------------------------------------------------------------------------
# /memory/context  — token-budgeted context for session-start injection
# ---------------------------------------------------------------------------

async def handle_memory_context(request: Request) -> JSONResponse:
    """
    GET /memory/context?project_id=...&max_tokens=4000&platform=cursor

    Returns token-budgeted context block for session-start injection.
    """
    try:
        db, _ = _get_shared()
    except RuntimeError as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=503)

    project_id = request.query_params.get("project_id")
    if not project_id:
        return JSONResponse({"success": False, "error": "project_id required"}, status_code=400)

    max_tokens = int(request.query_params.get("max_tokens", 4000))
    platform_filter = request.query_params.get("platform")

    try:
        platform_clause = "AND s.platform = %s" if platform_filter else ""
        params_base: list = [project_id]
        if platform_filter:
            params_base.append(platform_filter)

        with db.get_cursor() as cur:
            # Recent sessions with summaries
            cur.execute(
                f"""
                SELECT s.conversation_id, s.platform, s.session_summary, s.ended_at,
                       COUNT(t.id) AS turn_count
                FROM agent_sessions s
                JOIN agent_projects p ON s.project_id = p.id
                LEFT JOIN agent_turns t ON t.session_id = s.id
                WHERE p.project_id = %s
                  AND s.session_summary IS NOT NULL
                  {platform_clause}
                GROUP BY s.id, s.conversation_id, s.platform, s.session_summary, s.ended_at
                ORDER BY s.ended_at DESC
                LIMIT 5
                """,
                params_base,
            )
            sessions = cur.fetchall()

            # Recent captures — latest per topic, plus un-topicked entries
            # Use DISTINCT ON (topic) to avoid showing stale versions of updated insights.
            cur.execute(
                f"""
                SELECT DISTINCT ON (COALESCE(c.topic, c.id::text))
                       c.summary, c.key_decisions, c.files_changed, c.created_at,
                       c.category, c.scope, c.topic
                FROM agent_memory_captures c
                JOIN agent_sessions s ON c.session_id = s.id
                JOIN agent_projects p ON c.project_id = p.id
                WHERE p.project_id = %s
                  {platform_clause}
                ORDER BY COALESCE(c.topic, c.id::text), c.created_at DESC
                LIMIT 20
                """,
                params_base,
            )
            captures = cur.fetchall()

        # Build context block with token budget
        lines = ["# Agent Memory Context", ""]
        approx_chars = len(lines[0])
        budget = max_tokens * 4  # rough chars-per-token

        if sessions:
            lines.append("## Recent Sessions")
            for row in sessions:
                plat = row["platform"]
                summ = row["session_summary"]
                ended_at = row["ended_at"]
                turn_cnt = row["turn_count"]
                date_str = ended_at.strftime("%Y-%m-%d") if ended_at else "unknown"
                entry = f"- [{plat}] {date_str} ({turn_cnt} turns): {summ or 'no summary'}"
                approx_chars += len(entry)
                if approx_chars > budget:
                    break
                lines.append(entry)
            lines.append("")

        if captures:
            # Group by category for a richer context block
            from collections import defaultdict
            by_category: dict = defaultdict(list)
            for row in captures:
                cat = row.get("category") or "context"
                by_category[cat].append(row)

            category_order = ["procedure", "preference", "correction", "decision", "context", "general"]
            category_labels = {
                "procedure": "## Procedures & How-Tos",
                "preference": "## User Preferences",
                "correction": "## Corrections (Avoid These)",
                "decision": "## Architectural Decisions",
                "context": "## Project Context",
                "general": "## Notes",
            }

            for cat in category_order:
                rows = by_category.get(cat, [])
                if not rows:
                    continue
                section_header = category_labels.get(cat, f"## {cat.title()}")
                lines.append(section_header)
                for row in rows:
                    topic = row.get("topic")
                    summary = row.get("summary") or row.get("key_decisions") or ""
                    created_at = row.get("created_at")
                    if not summary:
                        continue
                    date_str = created_at.strftime("%Y-%m-%d") if created_at else "unknown"
                    prefix = f"**{topic}**:" if topic else f"[{date_str}]"
                    entry = f"- {prefix} {summary}"
                    approx_chars += len(entry)
                    if approx_chars > budget:
                        break
                    lines.append(entry)
                lines.append("")

        context_text = "\n".join(lines)

        return JSONResponse(
            {
                "success": True,
                "project_id": project_id,
                "context": context_text,
                "approx_chars": approx_chars,
                "sessions_included": len(sessions),
                "captures_included": len(captures),
            }
        )

    except Exception as e:
        logger.error("memory/context error: %s", e, exc_info=True)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ---------------------------------------------------------------------------
# /memory/health
# ---------------------------------------------------------------------------

async def handle_memory_health(request: Request) -> JSONResponse:
    """GET /memory/health — quick health check for the REST bridge."""
    db_ok = _shared["db"] is not None
    return JSONResponse(
        {
            "success": True,
            "db_connected": db_ok,
            "endpoints": [
                "POST /memory/ingest",
                "POST /memory/capture",
                "POST /memory/insight",
                "GET  /memory/context?project_id=...",
                "GET  /memory/health",
            ],
        }
    )


# ---------------------------------------------------------------------------
# Route list — imported by server.py
# ---------------------------------------------------------------------------

MEMORY_ROUTES = [
    Route("/memory/health",  endpoint=handle_memory_health,  methods=["GET"]),
    Route("/memory/ingest",  endpoint=handle_memory_ingest,  methods=["POST"]),
    Route("/memory/capture", endpoint=handle_memory_capture, methods=["POST"]),
    Route("/memory/insight", endpoint=handle_memory_insight, methods=["POST"]),
    Route("/memory/context", endpoint=handle_memory_context, methods=["GET"]),
]
