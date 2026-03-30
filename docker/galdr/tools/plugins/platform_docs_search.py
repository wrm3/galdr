"""
platform_docs_search — semantic search over crawled platform docs.

Searches the RAG knowledge base for platform documentation (Cursor, Claude, Gemini).
Docs are crawled by crawl4ai (host-side) and ingested via update_crawl_registry.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "platform_docs_search"
TOOL_DESCRIPTION = (
    "Search platform documentation (Cursor, Claude API, Gemini) for up-to-date information. "
    "Content is crawled by crawl4ai (host-side script) from official docs. "
    "Use for: Cursor IDE features, Claude API parameters, Gemini API usage, MCP configuration. "
    "Returns the most relevant doc sections matching your query."
)
TOOL_PARAMS = {
    "query":    "Natural language search query (e.g., 'how to configure MCP tools in Cursor')",
    "platform": "Filter by platform: 'cursor' | 'claude' | 'gemini' | null for all (optional)",
    "limit":    "Max results to return (1-10, default: 5)",
}

RAG_SUBJECT = "platform_docs"
_db = None


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(
    query: str,
    platform: Optional[str] = None,
    limit: int = 5,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not available"}

    limit = max(1, min(limit, 10))

    try:
        embedding = _get_embedding(query)
        if not embedding:
            return {"success": False, "error": "Could not generate embedding for query"}

        embed_str = "[" + ",".join(str(x) for x in embedding) + "]"

        sql = """
            SELECT content, metadata, 1 - (embedding <=> %s::vector) AS similarity
            FROM memory_captures
            WHERE subject = %s
        """
        params: list = [embed_str, RAG_SUBJECT]

        if platform:
            sql += " AND metadata->>'platform' = %s"
            params.append(platform.lower())

        sql += " ORDER BY embedding <=> %s::vector LIMIT %s"
        params.extend([embed_str, limit])

        with _db.get_cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        if not rows:
            return {
                "success": True,
                "results": [],
                "message": (
                    "No platform docs found. "
                    "Run `python scripts/platform_crawl.py --target all` to crawl platform docs, "
                    "or use the @g-platform-crawl command."
                ),
            }

        results = []
        for row in rows:
            content = row["content"]
            metadata = row["metadata"] or {}
            similarity = row["similarity"]
            if isinstance(metadata, str):
                import json
                metadata = json.loads(metadata)
            results.append({
                "content": content,
                "url": metadata.get("url", ""),
                "title": metadata.get("title", ""),
                "platform": metadata.get("platform", ""),
                "similarity": round(float(similarity), 4),
                "content_hash": metadata.get("content_hash", ""),
            })

        return {
            "success": True,
            "query": query,
            "platform_filter": platform,
            "results": results,
            "result_count": len(results),
        }

    except Exception as e:
        logger.exception("platform_docs_search failed")
        return {"success": False, "error": str(e)}


def _get_embedding(text: str) -> Optional[list[float]]:
    """Generate embedding using OpenAI if available."""
    import os
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        logger.warning("No OPENAI_API_KEY — platform_docs_search requires embeddings")
        return None
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        resp = client.embeddings.create(model="text-embedding-3-small", input=text)
        return resp.data[0].embedding
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        return None
