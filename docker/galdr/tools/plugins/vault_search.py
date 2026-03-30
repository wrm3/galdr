"""
Vault Search Tool Plugin

Semantic and keyword search against the vault_notes database table.
Returns matching notes ranked by relevance (cosine similarity for semantic,
ts_rank for keyword).
"""
import logging
from typing import Optional

TOOL_NAME = "vault_search"

TOOL_DESCRIPTION = (
    "Search the vault knowledge base using semantic (vector) or keyword search. "
    "Returns matching notes with title, path, snippet, and similarity score. "
    "Use for finding research, video summaries, harvested ideas, platform docs, etc."
)

TOOL_PARAMS = {
    "query": "Search query — natural language for semantic, keywords for keyword mode",
    "mode": "Search mode: 'semantic' (default, uses embeddings), 'keyword' (PostgreSQL full-text), 'hybrid' (both)",
    "note_type": "Filter by note type (e.g. 'video_summary', 'harvest', 'research', 'platform_docs'). Optional.",
    "project_id": "Filter by project_id. Optional.",
    "tags": "Comma-separated tags to filter by. Optional.",
    "limit": "Max results (default 10, max 50)",
}

_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


def _snippet(body: str, max_len: int = 300) -> str:
    if not body:
        return ""
    text = body.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0] + "..."


async def execute(
    query: str,
    mode: str = "semantic",
    note_type: Optional[str] = None,
    project_id: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 10,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not query:
        return {"success": False, "error": "Query is required"}

    limit = min(max(1, int(limit)), 50)
    results = []

    where_clauses = []
    params = []

    if note_type:
        where_clauses.append("note_type = %s")
        params.append(note_type)
    if project_id:
        where_clauses.append("project_id = %s")
        params.append(project_id)
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            where_clauses.append("tags && %s")
            params.append(tag_list)

    where_sql = ""
    if where_clauses:
        where_sql = "AND " + " AND ".join(where_clauses)

    if mode in ("semantic", "hybrid"):
        if not _embedding_gen:
            if mode == "semantic":
                return {"success": False, "error": "Embedding generator not available — try mode='keyword'"}
        else:
            try:
                query_embedding = _embedding_gen.generate(query)
            except Exception as e:
                return {"success": False, "error": f"Embedding generation failed: {e}"}

            with _db.get_cursor() as cur:
                sql = f"""
                    SELECT path, title, note_type, tags, url, body,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM vault_notes
                    WHERE embedding IS NOT NULL {where_sql}
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """
                cur.execute(sql, [query_embedding] + params + [query_embedding, limit])
                for row in cur.fetchall():
                    results.append({
                        "path": row["path"],
                        "title": row["title"],
                        "type": row["note_type"],
                        "tags": row["tags"],
                        "url": row.get("url", ""),
                        "snippet": _snippet(row["body"]),
                        "similarity": round(float(row["similarity"]), 4),
                        "search_mode": "semantic",
                    })

    if mode in ("keyword", "hybrid"):
        with _db.get_cursor() as cur:
            ts_query = " & ".join(query.split())
            sql = f"""
                SELECT path, title, note_type, tags, url, body,
                       ts_rank(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, '')),
                               to_tsquery('english', %s)) AS rank
                FROM vault_notes
                WHERE to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))
                      @@ to_tsquery('english', %s) {where_sql}
                ORDER BY rank DESC
                LIMIT %s
            """
            cur.execute(sql, [ts_query, ts_query] + params + [limit])
            for row in cur.fetchall():
                # Deduplicate against semantic results
                if not any(r["path"] == row["path"] for r in results):
                    results.append({
                        "path": row["path"],
                        "title": row["title"],
                        "type": row["note_type"],
                        "tags": row["tags"],
                        "url": row.get("url", ""),
                        "snippet": _snippet(row["body"]),
                        "rank": round(float(row["rank"]), 4),
                        "search_mode": "keyword",
                    })

    return {
        "success": True,
        "query": query,
        "mode": mode,
        "count": len(results),
        "results": results[:limit],
    }
