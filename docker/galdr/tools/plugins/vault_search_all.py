"""
Vault Search All — Unified search across ALL knowledge stores.

Fans out to three DB tables in parallel:
  1. vault_notes (vault .md files indexed via vault_sync)
  2. memory_captures (platform_docs from Firecrawl + session captures)
  3. agent_turns (raw session turns from memory_ingest_session)

Returns merged, deduplicated results ranked by relevance.
"""
import logging
from typing import Optional

TOOL_NAME = "vault_search_all"

TOOL_DESCRIPTION = (
    "Search ALL knowledge stores at once: vault notes, platform docs, and agent memory. "
    "Returns merged results from vault_notes (research, videos, harvests), "
    "memory_captures (platform docs, session summaries), and agent_turns (chat history). "
    "Use this instead of calling vault_search, platform_docs_search, and memory_search separately."
)

TOOL_PARAMS = {
    "query": "Search query — natural language",
    "sources": "Comma-separated sources to search: 'all' (default), 'vault', 'platform_docs', 'memory', 'sessions'. Use 'all' to search everything.",
    "project_id": "Filter by project_id (optional — omit to search globally)",
    "limit": "Max results per source (default 10, max 25)",
}

_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


def _snippet(text: str, max_len: int = 300) -> str:
    if not text:
        return ""
    text = text.strip()
    return text[:max_len].rsplit(" ", 1)[0] + "..." if len(text) > max_len else text


def _search_vault_notes(query_embedding, project_id, limit):
    """Search vault_notes table (vault .md files)."""
    results = []
    try:
        where = "AND project_id = %s" if project_id else ""
        params = [query_embedding] + ([project_id] if project_id else []) + [query_embedding, limit]

        with _db.get_cursor() as cur:
            sql = f"""
                SELECT path, title, note_type, tags, url, body,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM vault_notes
                WHERE embedding IS NOT NULL {where}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """
            cur.execute(sql, params)
            for row in cur.fetchall():
                results.append({
                    "source": "vault",
                    "path": row["path"],
                    "title": row["title"] or row["path"],
                    "type": row["note_type"] or "note",
                    "tags": row["tags"] or [],
                    "url": row.get("url", ""),
                    "snippet": _snippet(row["body"]),
                    "score": round(float(row["similarity"]), 4),
                })
    except Exception as e:
        _logger.warning(f"vault_notes search failed: {e}")
    return results


def _search_platform_docs(query_embedding, limit):
    """Search memory_captures where subject='platform_docs' (Firecrawl output)."""
    results = []
    try:
        with _db.get_cursor() as cur:
            cur.execute("""
                SELECT id, content, metadata,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM memory_captures
                WHERE subject = 'platform_docs' AND embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [query_embedding, query_embedding, limit])
            for row in cur.fetchall():
                meta = row.get("metadata") or {}
                if isinstance(meta, str):
                    import json
                    try:
                        meta = json.loads(meta)
                    except Exception:
                        meta = {}
                results.append({
                    "source": "platform_docs",
                    "path": meta.get("url", f"platform_doc_{row['id']}"),
                    "title": meta.get("title", "Platform Doc"),
                    "type": "platform_docs",
                    "tags": [meta.get("platform", "unknown")],
                    "url": meta.get("url", ""),
                    "snippet": _snippet(row["content"]),
                    "score": round(float(row["similarity"]), 4),
                })
    except Exception as e:
        _logger.warning(f"platform_docs search failed: {e}")
    return results


def _search_memory_captures(query_embedding, project_id, limit):
    """Search agent_memory_captures (session summaries, insights)."""
    results = []
    try:
        where = ""
        params = [query_embedding]
        if project_id:
            where = "AND p.project_id = %s"
            params.append(project_id)
        params += [query_embedding, limit]

        with _db.get_cursor() as cur:
            cur.execute(f"""
                SELECT c.id, c.summary, c.key_decisions, c.category, c.topic,
                       s.conversation_id, s.platform,
                       p.project_id, p.display_name,
                       1 - (c.embedding <=> %s::vector) AS similarity
                FROM agent_memory_captures c
                JOIN agent_sessions s ON c.session_id = s.id
                JOIN agent_projects p ON c.project_id = p.id
                WHERE c.embedding IS NOT NULL {where}
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """, params)
            for row in cur.fetchall():
                title_parts = []
                if row.get("category"):
                    title_parts.append(row["category"])
                if row.get("topic"):
                    title_parts.append(row["topic"])
                title = " — ".join(title_parts) if title_parts else f"Session {row.get('conversation_id', '')[:8]}"

                snippet = row.get("summary") or ""
                if row.get("key_decisions"):
                    kd = row["key_decisions"]
                    if isinstance(kd, list):
                        snippet += " | Decisions: " + "; ".join(kd[:3])

                results.append({
                    "source": "memory",
                    "path": f"memory/capture_{row['id']}",
                    "title": title,
                    "type": row.get("category") or "session_capture",
                    "tags": [row.get("platform", ""), row.get("display_name", "")],
                    "url": "",
                    "snippet": _snippet(snippet),
                    "score": round(float(row["similarity"]), 4),
                })
    except Exception as e:
        _logger.warning(f"memory_captures search failed: {e}")
    return results


def _search_session_turns(query_embedding, project_id, limit):
    """Search agent_turns (raw chat history)."""
    results = []
    try:
        where = ""
        params = [query_embedding]
        if project_id:
            where = "AND p.project_id = %s"
            params.append(project_id)
        params += [query_embedding, limit]

        with _db.get_cursor() as cur:
            cur.execute(f"""
                SELECT t.id, t.role, t.content, t.turn_index,
                       s.conversation_id, s.platform,
                       p.project_id, p.display_name,
                       1 - (t.embedding <=> %s::vector) AS similarity
                FROM agent_turns t
                JOIN agent_sessions s ON t.session_id = s.id
                JOIN agent_projects p ON s.project_id = p.id
                WHERE t.embedding IS NOT NULL {where}
                ORDER BY t.embedding <=> %s::vector
                LIMIT %s
            """, params)
            for row in cur.fetchall():
                conv_id = row.get("conversation_id", "")[:8]
                results.append({
                    "source": "sessions",
                    "path": f"sessions/{conv_id}/turn_{row.get('turn_index', 0)}",
                    "title": f"[{row.get('role', 'unknown')}] Session {conv_id}",
                    "type": "chat_turn",
                    "tags": [row.get("platform", ""), row.get("display_name", "")],
                    "url": "",
                    "snippet": _snippet(row.get("content", "")),
                    "score": round(float(row["similarity"]), 4),
                })
    except Exception as e:
        _logger.warning(f"session_turns search failed: {e}")
    return results


async def execute(
    query: str,
    sources: str = "all",
    project_id: Optional[str] = None,
    limit: int = 10,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not query:
        return {"success": False, "error": "Query is required"}
    if not _embedding_gen:
        return {"success": False, "error": "Embedding generator not available"}

    limit = min(max(1, int(limit)), 25)

    try:
        query_embedding = _embedding_gen.generate(query)
    except Exception as e:
        return {"success": False, "error": f"Embedding generation failed: {e}"}

    source_list = [s.strip().lower() for s in sources.split(",")]
    search_all = "all" in source_list

    all_results = []

    if search_all or "vault" in source_list:
        all_results.extend(_search_vault_notes(query_embedding, project_id, limit))

    if search_all or "platform_docs" in source_list:
        all_results.extend(_search_platform_docs(query_embedding, limit))

    if search_all or "memory" in source_list:
        all_results.extend(_search_memory_captures(query_embedding, project_id, limit))

    if search_all or "sessions" in source_list:
        all_results.extend(_search_session_turns(query_embedding, project_id, limit))

    # Sort by score descending, deduplicate by path
    all_results.sort(key=lambda r: r.get("score", 0), reverse=True)
    seen = set()
    deduped = []
    for r in all_results:
        key = r["path"]
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    # Group counts by source
    source_counts = {}
    for r in deduped:
        src = r["source"]
        source_counts[src] = source_counts.get(src, 0) + 1

    return {
        "success": True,
        "query": query,
        "sources_searched": source_list if not search_all else ["vault", "platform_docs", "memory", "sessions"],
        "total_results": len(deduped),
        "source_counts": source_counts,
        "results": deduped[:limit * 2],
    }
