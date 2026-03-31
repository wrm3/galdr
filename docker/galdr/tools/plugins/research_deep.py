"""
research_deep — Comprehensive web research via Perplexity sonar-pro/deep-research.

Performs a deep multi-source research query and stores the result in vault_notes.
Uses Perplexity's more capable models for thorough analysis.
"""
import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "research_deep"

TOOL_DESCRIPTION = (
    "Perform comprehensive web research using Perplexity AI's deep research models. "
    "Returns a thorough analysis with source citations. Results are stored in the vault "
    "by default. Example: research_deep(query='Compare RAG architectures for production')"
)

TOOL_PARAMS = {
    "query": "Research query (required)",
    "depth": "Research depth: 'standard' (sonar-pro) or 'comprehensive' (sonar-deep-research). Default: 'standard'",
    "store_result": "Store the result in vault_notes (default: true)",
    "tags": "Tags for the stored note (optional)",
}

_db = None
_embedding_gen = None
_config = None
_logger = logging.getLogger(__name__)

DEPTH_MODELS = {
    "standard": "sonar-pro",
    "comprehensive": "sonar-deep-research",
}


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
    depth: str = "standard",
    store_result: bool = True,
    tags: Optional[list] = None,
) -> dict:
    if not query or not query.strip():
        return {"success": False, "error": "query is required"}

    api_key = _get_api_key()
    if not api_key:
        return {"success": False, "error": "PERPLEXITY_API_KEY not configured. Use config_reload to set it."}

    import httpx

    tags = tags or []
    model = DEPTH_MODELS.get(depth, "sonar-pro")

    try:
        timeout = 120 if depth == "comprehensive" else 60
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a thorough research assistant. Provide comprehensive, well-structured analysis with specific details, comparisons, and actionable insights.",
                        },
                        {"role": "user", "content": query},
                    ],
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
        "sources": sources[:20],
        "model": data.get("model", model),
        "depth": depth,
    }

    if store_result and _db and answer:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        slug = _slugify(query)
        vault_path = f"ingested/research/{now}_deep_{slug}.md"

        sources_md = "\n".join(f"- {s['url']}" for s in sources[:20])
        frontmatter = (
            f"---\n"
            f'title: "Deep Research: {query[:100]}"\n'
            f'date: "{now}"\n'
            f"type: research\n"
            f'source: "perplexity"\n'
            f"ingestion_type: research_deep\n"
            f"refresh_policy: none\n"
            f"source_volatility: medium\n"
            f"depth: {depth}\n"
            f"model: {model}\n"
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
                        (vault_path, f"Deep Research: {query[:100]}", content, body, ch,
                         embedding, "research", "perplexity", "perplexity_api", tags),
                    )
                    conn.commit()
            result["stored_path"] = vault_path
        except Exception as e:
            _logger.error("Failed to store research result: %s", e)
            result["store_error"] = str(e)

    return result
