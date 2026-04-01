"""
url_ingest — Fetch a web URL and index it into vault_notes.

One-shot ingestion for articles, blogs, news, and general web pages.
Uses crawl4ai to extract readable content, generates vault frontmatter,
creates an embedding, and stores in vault_notes.
"""
import hashlib
import logging
import os
import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

TOOL_NAME = "url_ingest"

TOOL_DESCRIPTION = (
    "Fetch a web URL (article, blog, news) and index it into the vault database. "
    "Extracts readable content via crawl4ai, generates frontmatter and embedding, "
    "stores in vault_notes. Idempotent — skips unchanged content. "
    "Example: url_ingest(url='https://example.com/article', tags=['ai', 'agents'])"
)

TOOL_PARAMS = {
    "url": "URL to fetch and ingest (required)",
    "title": "Override page title (optional — auto-extracted if omitted)",
    "tags": "List of tags for the note (optional)",
    "note_type": "Vault note type (default: 'article')",
    "refresh_policy": "Refresh policy: 'none' (one-time), 'weekly', 'monthly' (default: 'none')",
}

_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


def _embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text[:8000])
        return result.tolist() if hasattr(result, "tolist") else list(result)
    except Exception as e:
        _logger.warning("Embedding failed: %s", e)
        return None


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _url_to_slug(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_") or "index"
    path = re.sub(r"[^a-zA-Z0-9_\-.]", "_", path)
    if len(path) > 120:
        path = path[:120]
    if not path.endswith(".md"):
        path += ".md"
    return path


async def _fetch_content(url: str) -> tuple[Optional[str], Optional[str]]:
    """Fetch URL content. Tries crawl4ai first, falls back to httpx + html2text."""
    # Try crawl4ai (full browser rendering)
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

        browser_config = BrowserConfig(headless=True)
        crawl_config = CrawlerRunConfig(
            word_count_threshold=50,
            remove_overlay_elements=True,
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawl_config)

        if result.success and result.markdown and result.markdown.strip():
            page_title = (result.metadata.get("title", "") if result.metadata else "") or None
            return result.markdown, page_title

        _logger.info("crawl4ai returned empty for %s, trying httpx fallback", url)
    except Exception as e:
        _logger.info("crawl4ai unavailable (%s), trying httpx fallback", e)

    # Fallback: httpx + basic HTML-to-text
    try:
        import httpx

        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; galdr-bot/1.0)",
                "Accept": "text/html,application/xhtml+xml",
            })
            resp.raise_for_status()
            html = resp.text

        page_title = None
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if title_match:
            page_title = title_match.group(1).strip()

        try:
            import html2text
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = True
            h.body_width = 0
            markdown = h.handle(html)
        except ImportError:
            markdown = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
            markdown = re.sub(r"<style[^>]*>.*?</style>", "", markdown, flags=re.DOTALL | re.IGNORECASE)
            markdown = re.sub(r"<[^>]+>", " ", markdown)
            markdown = re.sub(r"\s+", " ", markdown).strip()

        return markdown, page_title
    except Exception as e:
        _logger.error("httpx fallback failed for %s: %s", url, e)
        return None, None


async def execute(
    url: str,
    title: Optional[str] = None,
    tags: Optional[list] = None,
    note_type: str = "article",
    refresh_policy: str = "none",
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not url or not url.strip():
        return {"success": False, "error": "url is required"}

    url = url.strip()
    tags = tags or []
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    slug = _url_to_slug(url)
    vault_path = f"ingested/{note_type}/{domain}/{slug}"

    markdown, extracted_title = await _fetch_content(url)
    if markdown is None:
        return {"success": False, "error": "Failed to extract readable content", "url": url}
    if not markdown.strip():
        return {"success": False, "error": "No readable content extracted", "url": url}
    if not title:
        title = extracted_title or domain

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    frontmatter = (
        f"---\n"
        f'title: "{title}"\n'
        f'date: "{now}"\n'
        f"type: {note_type}\n"
        f'source: "{url}"\n'
        f'url: "{url}"\n'
        f"ingestion_type: url_ingest\n"
        f"refresh_policy: {refresh_policy}\n"
        f"topics: {tags}\n"
        f"---\n\n"
    )
    content = frontmatter + markdown
    ch = _content_hash(content)

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT content_hash FROM vault_notes WHERE path = %s", (vault_path,))
                row = cur.fetchone()
                if row:
                    existing_hash = row[0] if isinstance(row, tuple) else row.get("content_hash")
                    if existing_hash == ch:
                        return {
                            "success": True,
                            "path": vault_path,
                            "title": title,
                            "status": "unchanged",
                            "url": url,
                        }

                embedding = _embed(f"{title}\n\n{markdown[:6000]}")

                import json as _json
                fm_dict = {
                    "title": title, "date": now, "type": note_type,
                    "source": url, "url": url,
                    "ingestion_type": "url_ingest",
                    "refresh_policy": refresh_policy, "topics": tags,
                }
                cur.execute(
                    """
                    INSERT INTO vault_notes
                        (path, title, content, body, content_hash, embedding,
                         note_type, source, source_type, url, tags,
                         frontmatter, links, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (path) DO UPDATE SET
                        title        = EXCLUDED.title,
                        content      = EXCLUDED.content,
                        body         = EXCLUDED.body,
                        content_hash = EXCLUDED.content_hash,
                        embedding    = EXCLUDED.embedding,
                        tags         = EXCLUDED.tags,
                        frontmatter  = EXCLUDED.frontmatter,
                        updated_at   = NOW()
                    """,
                    (
                        vault_path, title, content, markdown, ch, embedding,
                        note_type, url, "crawl4ai", url, tags,
                        _json.dumps(fm_dict), [],
                    ),
                )
                conn.commit()

        status = "updated" if row else "created"
        return {
            "success": True,
            "path": vault_path,
            "title": title,
            "status": status,
            "url": url,
            "content_length": len(markdown),
        }
    except Exception as e:
        _logger.error("DB error ingesting %s: %s", url, e)
        return {"success": False, "error": str(e), "url": url}
