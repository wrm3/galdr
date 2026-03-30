"""
platform_crawl_trigger — Kick off a server-side crawl4ai crawl.

Runs asynchronously in the server process. Results are stored in
vault_notes with embeddings and broadcast to connected WebSocket clients.
"""
import asyncio
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "platform_crawl_trigger"
TOOL_DESCRIPTION = (
    "Start a server-side documentation crawl using crawl4ai. "
    "Crawls the specified target (e.g. 'cursor', 'claude', 'gemini') or a custom URL. "
    "Results are stored in the database and broadcast to connected clients. "
    "The crawl runs asynchronously — use platform_crawl_status to check progress."
)
TOOL_PARAMS = {
    "target":    "Built-in target name ('cursor', 'claude', 'gemini') or 'custom'",
    "urls":      "List of URLs to crawl (required if target='custom', ignored otherwise)",
    "max_pages": "Maximum pages to crawl (default: 50)",
    "max_depth": "Maximum link depth (default: 3)",
    "user_id":   "User ID triggering the crawl (optional, for audit trail)",
}

_db = None
_embedding_gen = None
_config = None
_logger = logging.getLogger(__name__)

# In-memory crawl state
_active_crawls: dict[str, dict] = {}

BUILTIN_TARGETS = {
    "cursor": {
        "name": "Cursor IDE",
        "urls": ["https://docs.cursor.com"],
        "max_pages": 100,
        "max_depth": 3,
    },
    "claude": {
        "name": "Claude / Anthropic",
        "urls": ["https://docs.anthropic.com"],
        "max_pages": 100,
        "max_depth": 3,
    },
    "gemini": {
        "name": "Google Gemini",
        "urls": ["https://ai.google.dev/gemini-api/docs"],
        "max_pages": 100,
        "max_depth": 3,
    },
}


def setup(context: dict):
    global _db, _embedding_gen, _config
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")
    _config = context.get("config", {})


def _embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text[:8000])
        return result.tolist() if hasattr(result, "tolist") else list(result)
    except Exception as e:
        _logger.warning("Embedding failed: %s", e)
        return None


async def _run_crawl(crawl_id: str, target_name: str, urls: list[str],
                     max_pages: int, max_depth: int, user_id: str) -> None:
    """Background crawl task using crawl4ai."""
    state = _active_crawls[crawl_id]
    state["status"] = "running"
    state["started_at"] = datetime.now(timezone.utc).isoformat()

    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

        browser_config = BrowserConfig(headless=True)
        crawl_config = CrawlerRunConfig(
            word_count_threshold=50,
            remove_overlay_elements=True,
        )

        pages_crawled = 0
        visited: set[str] = set()
        to_visit: list[tuple[str, int]] = [(url, 0) for url in urls]

        async with AsyncWebCrawler(config=browser_config) as crawler:
            while to_visit and pages_crawled < max_pages:
                url, depth = to_visit.pop(0)
                if url in visited:
                    continue
                visited.add(url)

                try:
                    result = await crawler.arun(url=url, config=crawl_config)
                    if not result.success:
                        _logger.warning("Crawl failed for %s: %s", url, result.error_message)
                        continue

                    pages_crawled += 1
                    state["pages_crawled"] = pages_crawled
                    state["current_url"] = url

                    markdown = result.markdown or ""
                    if not markdown.strip():
                        continue

                    title = result.metadata.get("title", url) if result.metadata else url
                    path = f"platforms/{target_name}/{_url_to_path(url)}"

                    frontmatter = (
                        f"---\n"
                        f"title: \"{title}\"\n"
                        f"source: \"{url}\"\n"
                        f"type: platform_docs\n"
                        f"platform: {target_name}\n"
                        f"date: \"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}\"\n"
                        f"crawled_by: server\n"
                        f"---\n\n"
                    )
                    content = frontmatter + markdown

                    _store_crawled_page(path, content, url, target_name)

                    if depth < max_depth and result.links:
                        internal = result.links.get("internal", [])
                        for link_info in internal[:20]:
                            link_url = link_info.get("href", "") if isinstance(link_info, dict) else str(link_info)
                            if link_url and link_url not in visited:
                                to_visit.append((link_url, depth + 1))

                except Exception as e:
                    _logger.warning("Error crawling %s: %s", url, e)
                    continue

        state["status"] = "completed"
        state["pages_crawled"] = pages_crawled
        state["completed_at"] = datetime.now(timezone.utc).isoformat()

        if _db:
            _update_crawl_schedule(target_name)

    except ImportError:
        state["status"] = "failed"
        state["error"] = "crawl4ai not installed in this Docker image"
        _logger.error("crawl4ai not available — add to requirements.txt and rebuild")
    except Exception as e:
        state["status"] = "failed"
        state["error"] = str(e)
        _logger.error("Crawl %s failed: %s", crawl_id, e)


def _url_to_path(url: str) -> str:
    """Convert URL to a filesystem-safe path."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_") or "index"
    return f"{path}.md"


def _store_crawled_page(path: str, content: str, url: str,
                        target_name: str) -> None:
    """Store a crawled page in vault_notes."""
    if not _db:
        return

    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    embedding = _embed(content[:4000])

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO vault_notes
                        (path, title, content, body, content_hash, embedding,
                         note_type, source, source_type, url, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (path) DO UPDATE
                        SET content      = EXCLUDED.content,
                            body         = EXCLUDED.body,
                            content_hash = EXCLUDED.content_hash,
                            embedding    = EXCLUDED.embedding,
                            updated_at   = NOW()
                    """,
                    (
                        path,
                        path.rsplit("/", 1)[-1].replace(".md", "").replace("_", " "),
                        content,
                        content,
                        content_hash,
                        embedding,
                        "platform_docs",
                        target_name,
                        "crawl4ai",
                        url,
                    ),
                )
                conn.commit()
    except Exception as e:
        _logger.warning("Failed to store crawled page %s: %s", path, e)


def _update_crawl_schedule(target_name: str) -> None:
    """Update last_crawled_at for the target in crawl_targets table."""
    if not _db:
        return
    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE crawl_targets
                    SET last_crawled_at = NOW()
                    WHERE name = %s
                    """,
                    (target_name,),
                )
                conn.commit()
    except Exception as e:
        _logger.debug("Failed to update crawl schedule: %s", e)


async def execute(
    target: str = "cursor",
    urls: Optional[list] = None,
    max_pages: int = 50,
    max_depth: int = 3,
    user_id: Optional[str] = None,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    # Resolve target
    if target == "custom":
        if not urls:
            return {"success": False, "error": "urls required for custom target"}
        target_name = "custom"
        target_urls = urls
    elif target in BUILTIN_TARGETS:
        t = BUILTIN_TARGETS[target]
        target_name = target
        target_urls = t["urls"]
        max_pages = max_pages or t["max_pages"]
        max_depth = max_depth or t["max_depth"]
    else:
        # Check DB for custom targets
        try:
            with _db.get_cursor() as cur:
                cur.execute(
                    "SELECT urls, max_pages, max_depth FROM crawl_targets WHERE name = %s",
                    (target,),
                )
                row = cur.fetchone()
                if row:
                    target_name = target
                    target_urls = row["urls"] if isinstance(row["urls"], list) else json.loads(row["urls"])
                    max_pages = max_pages or row["max_pages"]
                    max_depth = max_depth or row["max_depth"]
                else:
                    return {
                        "success": False,
                        "error": f"Unknown target: {target}. Available: {list(BUILTIN_TARGETS.keys())}",
                    }
        except Exception as e:
            return {"success": False, "error": f"Failed to look up target: {e}"}

    # Check if already running
    for cid, state in _active_crawls.items():
        if state.get("target") == target_name and state.get("status") == "running":
            return {
                "success": False,
                "error": f"Crawl already running for {target_name}",
                "crawl_id": cid,
            }

    crawl_id = f"{target_name}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    _active_crawls[crawl_id] = {
        "crawl_id": crawl_id,
        "target": target_name,
        "status": "queued",
        "pages_crawled": 0,
        "max_pages": max_pages,
        "queued_at": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
    }

    asyncio.create_task(
        _run_crawl(crawl_id, target_name, target_urls, max_pages, max_depth, user_id or "")
    )

    return {
        "success": True,
        "crawl_id": crawl_id,
        "target": target_name,
        "urls": target_urls,
        "max_pages": max_pages,
        "max_depth": max_depth,
        "status": "queued",
        "message": f"Crawl started for {target_name}. Use platform_crawl_status to check progress.",
    }
