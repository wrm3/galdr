"""
memory_search_combined.py — Unified semantic search across agent memory + RAG knowledge base.

Searches both:
  1. agent_turns (agent memory) — conversations, decisions, code discussions
  2. content_chunks (RAG knowledge base) — ingested documents, URLs, research

Returns merged, ranked results with clear source labels so the AI can tell
whether a result came from a past conversation or an ingested knowledge source.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_search_combined"
TOOL_DESCRIPTION = (
    "Semantic search across BOTH agent conversation memory and the RAG knowledge base. "
    "Returns merged results ranked by relevance with source labels: "
    "'memory' (past conversations) or 'rag' (ingested documents/URLs). "
    "Use this when you want to check everything the system knows about a topic — "
    "not just documents, but also past decisions and discussions.\n\n"
    "Parameters:\n"
    "  query        (str, required) — natural language search query\n"
    "  project_id   (str, optional) — filter memory results to a specific project\n"
    "  platform     (str, optional) — filter memory by platform (cursor/claude_code/etc.)\n"
    "  user_id      (str, optional) — filter memory results to a specific user\n"
    "  limit        (int, optional) — max results per source, default 5, max 20\n"
    "  memory_only  (bool, optional) — search only agent memory, skip RAG\n"
    "  rag_only     (bool, optional) — search only RAG knowledge base, skip memory"
)

_db = None
_embedding_gen = None


def setup(context: dict) -> None:
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


def _embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text)
        return result.tolist() if hasattr(result, "tolist") else list(result)
    except Exception as e:
        logger.warning("embedding failed: %s", e)
        return None


def _vec_str(vec: Optional[list]) -> Optional[str]:
    if not vec:
        return None
    return f"[{','.join(map(str, vec))}]"


async def execute(
    query: str,
    project_id: Optional[str] = None,
    platform: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 5,
    memory_only: bool = False,
    rag_only: bool = False,
) -> dict:
    """
    Perform unified semantic search across agent memory and/or the RAG knowledge base.
    """
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not query or not query.strip():
        return {"success": False, "error": "query is required"}

    limit = max(1, min(limit, 20))
    results: list[dict] = []
    rag_count = 0
    memory_count = 0

    # Generate query embedding once, used for both searches
    query_vec = _embed(query.strip())
    vec_str = _vec_str(query_vec)

    # ── 1. Agent Memory Search ────────────────────────────────────────────────
    if not rag_only and query_vec:
        try:
            with _db.get_cursor() as cur:
                # Build WHERE clause for optional filters
                where_parts = ["at.embedding IS NOT NULL"]
                params: list = []

                if project_id:
                    where_parts.append("ap.project_id = %s")
                    params.append(project_id)
                if platform:
                    where_parts.append("at.platform = %s")
                    params.append(platform)
                if user_id:
                    where_parts.append("at.user_id = %s")
                    params.append(user_id)

                where_sql = " AND ".join(where_parts)

                cur.execute(
                    f"""
                    SELECT
                        at.id,
                        at.user_message,
                        at.agent_response,
                        at.llm_title,
                        at.llm_description,
                        at.platform,
                        at.tool_names,
                        at.file_refs,
                        at.session_metadata,
                        at.created_at,
                        ap.project_id          AS project_id,
                        ap.display_name        AS project_name,
                        sess.conversation_id,
                        1 - (at.embedding <=> %s::vector) AS similarity
                    FROM agent_turns at
                    JOIN agent_sessions sess ON at.session_id = sess.id
                    JOIN agent_projects ap   ON sess.project_id = ap.id
                    WHERE {where_sql}
                    ORDER BY at.embedding <=> %s::vector
                    LIMIT %s
                    """,
                    [vec_str] + params + [vec_str, limit],
                )
                mem_rows = cur.fetchall()

            for row in mem_rows:
                snippet = (row["llm_title"] or row["user_message"] or "")[:200]
                agent_snippet = (row["agent_response"] or "")[:300]
                results.append({
                    "source":          "memory",
                    "similarity":      round(float(row["similarity"] or 0), 4),
                    "title":           row["llm_title"] or snippet[:80],
                    "snippet":         snippet,
                    "agent_response_snippet": agent_snippet,
                    "platform":        row["platform"],
                    "project_id":      row["project_id"],
                    "project_name":    row["project_name"],
                    "conversation_id": row["conversation_id"],
                    "tool_names":      row["tool_names"] or [],
                    "file_refs":       row["file_refs"] or [],
                    "git_branch":      (row["session_metadata"] or {}).get("gitBranch"),
                    "created_at":      row["created_at"].isoformat() if row["created_at"] else None,
                    "memory_turn_id":  row["id"],
                })
                memory_count += 1

        except Exception as e:
            logger.warning("agent memory search error: %s", e)
            results.append({"source": "memory", "error": str(e)})

    elif not rag_only and not query_vec:
        # Fallback: full-text search when no embedding available
        try:
            with _db.get_cursor() as cur:
                where_parts = ["1=1"]
                params = []
                if project_id:
                    where_parts.append("ap.project_id = %s")
                    params.append(project_id)
                if user_id:
                    where_parts.append("at.user_id = %s")
                    params.append(user_id)
                where_sql = " AND ".join(where_parts)

                cur.execute(
                    f"""
                    SELECT at.id, at.user_message, at.agent_response,
                           at.llm_title, at.platform, at.created_at,
                           ap.project_id, ap.display_name AS project_name,
                           sess.conversation_id,
                           ts_rank(
                               to_tsvector('english',
                                   COALESCE(at.llm_title,'') || ' ' ||
                                   COALESCE(at.llm_description,'') || ' ' ||
                                   COALESCE(array_to_string(at.file_refs,' '),'')),
                               plainto_tsquery('english', %s)
                           ) AS rank
                    FROM agent_turns at
                    JOIN agent_sessions sess ON at.session_id = sess.id
                    JOIN agent_projects ap   ON sess.project_id = ap.id
                    WHERE {where_sql}
                      AND to_tsvector('english',
                              COALESCE(at.llm_title,'') || ' ' ||
                              COALESCE(at.llm_description,'') || ' ' ||
                              COALESCE(array_to_string(at.file_refs,' '),'')
                          ) @@ plainto_tsquery('english', %s)
                    ORDER BY rank DESC
                    LIMIT %s
                    """,
                    [query] + params + [query, limit],
                )
                fts_rows = cur.fetchall()

            for row in fts_rows:
                results.append({
                    "source":          "memory_fts",
                    "similarity":      round(float(row["rank"] or 0), 4),
                    "title":           row["llm_title"] or (row["user_message"] or "")[:80],
                    "snippet":         (row["user_message"] or "")[:200],
                    "platform":        row["platform"],
                    "project_id":      row["project_id"],
                    "project_name":    row["project_name"],
                    "conversation_id": row["conversation_id"],
                    "created_at":      row["created_at"].isoformat() if row["created_at"] else None,
                    "memory_turn_id":  row["id"],
                })
                memory_count += 1

        except Exception as e:
            logger.warning("memory FTS fallback error: %s", e)

    # ── 2. RAG Knowledge Base Search ─────────────────────────────────────────
    if not memory_only and query_vec:
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        cc.id,
                        cc.chunk_text,
                        cc.chunk_type,
                        s.title         AS source_title,
                        s.url           AS source_url,
                        s.source_type,
                        s.author,
                        cc.created_at,
                        1 - (cc.embedding <=> %s::vector) AS similarity
                    FROM content_chunks cc
                    JOIN sources s ON cc.source_id = s.id
                    WHERE cc.embedding IS NOT NULL
                      AND s.status = 'completed'
                    ORDER BY cc.embedding <=> %s::vector
                    LIMIT %s
                    """,
                    [vec_str, vec_str, limit],
                )
                rag_rows = cur.fetchall()

            for row in rag_rows:
                results.append({
                    "source":       "rag",
                    "similarity":   round(float(row["similarity"] or 0), 4),
                    "title":        row["source_title"] or "Untitled",
                    "snippet":      (row["chunk_text"] or "")[:400],
                    "source_type":  row["source_type"],
                    "source_url":   row["source_url"],
                    "author":       row["author"],
                    "chunk_type":   row["chunk_type"],
                    "created_at":   row["created_at"].isoformat() if row["created_at"] else None,
                    "chunk_id":     str(row["id"]),
                })
                rag_count += 1

        except Exception as e:
            logger.warning("RAG search error: %s", e)
            results.append({"source": "rag", "error": str(e)})

    # ── 3. Sort merged results by similarity ──────────────────────────────────
    results.sort(key=lambda r: r.get("similarity", 0), reverse=True)

    return {
        "success":      True,
        "query":        query,
        "total":        len(results),
        "memory_count": memory_count,
        "rag_count":    rag_count,
        "has_embedding": query_vec is not None,
        "results":      results,
    }
