"""
research_search — Quick web research via Perplexity API.

Performs a focused web search and returns a synthesized answer with sources.
Optionally stores the result in vault_notes for future reference.
"""
import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "research_search"

TOOL_DESCRIPTION = (
    "Perform a quick web search using Perplexity AI. Returns a synthesized answer "
    "with source citations. Optionally stores the result in the vault. "
    "Example: research_search(query='What is the latest Claude Code update?')"
)

TOOL_PARAMS = {
    "query": "Search query (required)",
    "store_result": "Store the result in vault_notes (default: false)",
    "tags": "Tags for the stored note (optional)",
}

_db = None
_embedding_gen = None
_config = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db, _embedding_gen, _config
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")
    _config = context.get("config", {})


def _get_api_key() -> Optional[str]:
    return _config.get("PERPLEXITY_API_KEY") or os.getenv("PERPLEXITY_API_KEY")


def _embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text[:8000])
        return result.tolist() if hasattr(result, "tolist") else list(result)
    except Exception as e:
        _logger.warning("Embedding failed: %s", e)
        return None


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower())[:80]
    return slug.strip("_")


async def execute(
    query: str,
    store_result: bool = False,
    tags: Optional[list] = None,
) -> dict:
    if not query or not query.strip():
        return {"success": False, "error": "query is required"}

    api_key = _get_api_key()
    if not api_key:
        return {"success": False, "error": "PERPLEXITY_API_KEY not configured. Use config_reload to set it."}

    import httpx

    tags = tags or []

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": query}],
                    "return_citations": True,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as e:
        return {"success": False, "error": f"Perplexity API error: {e}"}

    answer = ""
    if data.get("choices"):
        answer = data["choices"][0].get("message", {}).get("content", "")

    citations = data.get("citations", [])
    sources = [{"url": c} for c in citations] if isinstance(citations, list) else []

    result = {
        "success": True,
        "query": query,
        "answer": answer,
        "sources": sources[:10],
        "model": data.get("model", "sonar"),
    }

    if store_result and _db and answer:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        slug = _slugify(query)
        vault_path = f"ingested/research/{now}_{slug}.md"

        sources_md = "\n".join(f"- {s['url']}" for s in sources[:10])
        frontmatter = (
            f"---\n"
            f'title: "Research: {query[:100]}"\n'
            f'date: "{now}"\n'
            f"type: research\n"
            f'source: "perplexity"\n'
            f"ingestion_type: research_search\n"
            f"refresh_policy: none\n"
            f"topics: {tags}\n"
            f"---\n\n"
        )
        body = f"# {query}\n\n{answer}\n\n## Sources\n\n{sources_md}\n"
        content = frontmatter + body
        ch = hashlib.sha256(content.encode()).hexdigest()[:16]
        embedding = _embed(f"{query}\n\n{answer[:4000]}")

        try:
            with _db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO vault_notes
                            (path, title, content, body, content_hash, embedding,
                             note_type, source, source_type, tags, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                        ON CONFLICT (path) DO UPDATE SET
                            content = EXCLUDED.content, body = EXCLUDED.body,
                            content_hash = EXCLUDED.content_hash, embedding = EXCLUDED.embedding,
                            updated_at = NOW()
                        """,
                        (vault_path, f"Research: {query[:100]}", content, body, ch,
                         embedding, "research", "perplexity", "perplexity_api", tags),
                    )
                    conn.commit()
            result["stored_path"] = vault_path
        except Exception as e:
            _logger.error("Failed to store research result: %s", e)
            result["store_error"] = str(e)

    return result
