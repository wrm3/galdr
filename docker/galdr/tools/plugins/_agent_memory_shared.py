"""
Shared helpers for agent_memory MCP tools.
Underscore prefix = utility module (not auto-loaded as a plugin).

Injected context keys:
  db                 — RAGDatabase instance
  embedding_generator — EmbeddingGenerator instance
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

MAX_CONTEXT_TOKENS = 4000
OPENAI_MODEL_SUMMARY = "gpt-4o-mini"

# ── Shared state injected by each plugin's setup() ────────────────────────────
_db = None
_embedding_gen = None


def init(context: dict) -> None:
    """Call from each plugin's setup() to wire in shared state."""
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


# ── Database helpers ──────────────────────────────────────────────────────────

def upsert_project(project_id: str, user_id: str, machine_id: str,
                   project_path: str, display_name: str) -> int:
    with _db.get_cursor() as cur:
        cur.execute(
            "SELECT upsert_agent_project(%s, %s, %s, %s, %s)",
            (project_id, user_id, machine_id, project_path, display_name),
        )
        row = cur.fetchone()
        # RealDictCursor returns a dict; the function result is keyed by the function name
        return list(row.values())[0]


def ensure_session(conversation_id: str, project_row_id: int,
                   platform: str, capture_tier: str,
                   status: Optional[str], loop_count: Optional[int],
                   user_id: Optional[str] = None) -> int:
    with _db.get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_sessions
                (conversation_id, project_id, platform, capture_tier,
                 status, loop_count, user_id, ended_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (conversation_id) DO UPDATE
                SET status     = EXCLUDED.status,
                    loop_count = EXCLUDED.loop_count,
                    user_id    = COALESCE(NULLIF(EXCLUDED.user_id, ''), agent_sessions.user_id)
            RETURNING id
            """,
            (conversation_id, project_row_id, platform, capture_tier,
             status, loop_count, user_id),
        )
        return cur.fetchone()["id"]


def content_hash(user_msg: str, agent_resp: str) -> str:
    return hashlib.md5(f"{user_msg}|||{agent_resp}".encode()).hexdigest()


def summarise_turn(user_msg: str, agent_resp: str) -> tuple[str, str]:
    """GPT-4o-mini title + description; falls back to truncation."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            "Given this developer ↔ AI exchange, produce:\n"
            "1. A 10-15 word title (plain text)\n"
            "2. A 2-4 sentence description of what was accomplished\n\n"
            f"User: {user_msg[:500]}\n\nAgent: {agent_resp[:1000]}\n\n"
            "Respond as JSON: {\"title\": \"...\", \"description\": \"...\"}"
        )
        resp = client.chat.completions.create(
            model=OPENAI_MODEL_SUMMARY,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        data = json.loads(resp.choices[0].message.content)
        return data.get("title", "")[:255], data.get("description", "")
    except Exception as e:
        logger.warning(f"summarise_turn LLM failed: {e}")
        title = (user_msg[:120] + "...") if len(user_msg) > 120 else user_msg
        desc = (agent_resp[:400] + "...") if len(agent_resp) > 400 else agent_resp
        return title, desc


def embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text)
        if hasattr(result, "tolist"):
            return result.tolist()
        return list(result)
    except Exception as e:
        logger.warning(f"embed failed: {e}")
        return None


def embed_str(vec: Optional[list]) -> Optional[str]:
    if not vec:
        return None
    return f"[{','.join(map(str, vec))}]"


def insert_turn(session_id: int, turn_index: int, user_msg: str,
                agent_resp: str, platform: str, capture_tier: str,
                user_id: Optional[str] = None) -> bool:
    """Returns True if inserted, False if duplicate."""
    chash = content_hash(user_msg, agent_resp)
    with _db.get_cursor() as cur:
        cur.execute(
            "SELECT 1 FROM agent_turns WHERE content_hash = %s", (chash,)
        )
        if cur.fetchone():
            return False

    title, description = summarise_turn(user_msg, agent_resp)
    emb = embed(f"{title} {description}")

    with _db.get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_turns
                (session_id, turn_index, content_hash, user_message,
                 agent_response, llm_title, llm_description, embedding,
                 platform, capture_tier, user_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s::vector,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            (session_id, turn_index, chash, user_msg, agent_resp,
             title, description, embed_str(emb), platform, capture_tier,
             user_id),
        )
    return True
