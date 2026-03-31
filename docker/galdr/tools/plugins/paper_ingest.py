"""
paper_ingest — Fetch arxiv/HuggingFace paper metadata and index into vault_notes.

Accepts a HuggingFace paper URL or arxiv ID, fetches title, authors, abstract,
and categories from the arxiv API, and stores as a searchable vault note.
"""
import hashlib
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "paper_ingest"

TOOL_DESCRIPTION = (
    "Fetch an academic paper's metadata (title, authors, abstract) from arxiv "
    "and index it into the vault database. Accepts HuggingFace paper URLs or "
    "arxiv IDs/URLs. Example: paper_ingest(url='https://huggingface.co/papers/2603.25804')"
)

TOOL_PARAMS = {
    "url": "HuggingFace paper URL, arxiv URL, or bare arxiv ID (e.g. '2603.25804') — required",
    "tags": "Additional tags (optional — arxiv categories are auto-added)",
}

_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


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


def _extract_arxiv_id(url: str) -> Optional[str]:
    m = ARXIV_ID_RE.search(url)
    return m.group(1) if m else None


async def execute(
    url: str,
    tags: Optional[list] = None,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not url or not url.strip():
        return {"success": False, "error": "url is required"}

    import httpx

    url = url.strip()
    tags = tags or []

    arxiv_id = _extract_arxiv_id(url)
    if not arxiv_id:
        return {"success": False, "error": f"Could not extract arxiv ID from: {url}"}

    vault_path = f"ingested/papers/{arxiv_id}.md"
    api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"

    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(api_url)
            resp.raise_for_status()
    except httpx.HTTPError as e:
        return {"success": False, "error": f"arxiv API error: {e}"}

    try:
        root = ET.fromstring(resp.text)
        entry = root.find("atom:entry", ARXIV_NS)
        if entry is None:
            return {"success": False, "error": f"No paper found for arxiv ID: {arxiv_id}"}

        title = (entry.findtext("atom:title", "", ARXIV_NS) or "").strip().replace("\n", " ")
        abstract = (entry.findtext("atom:summary", "", ARXIV_NS) or "").strip()
        published = entry.findtext("atom:published", "", ARXIV_NS)[:10]

        authors = []
        for author_el in entry.findall("atom:author", ARXIV_NS):
            name = author_el.findtext("atom:name", "", ARXIV_NS)
            if name:
                authors.append(name.strip())

        categories = []
        for cat_el in entry.findall("atom:category", ARXIV_NS):
            cat = cat_el.get("term", "")
            if cat:
                categories.append(cat)

        pdf_link = ""
        for link_el in entry.findall("atom:link", ARXIV_NS):
            if link_el.get("title") == "pdf":
                pdf_link = link_el.get("href", "")
                break

        abs_url = f"https://arxiv.org/abs/{arxiv_id}"

    except ET.ParseError as e:
        return {"success": False, "error": f"Failed to parse arxiv response: {e}"}

    if not title:
        return {"success": False, "error": f"Empty paper entry for {arxiv_id}"}

    all_tags = list(set(tags + categories))
    authors_str = ", ".join(authors[:10])
    if len(authors) > 10:
        authors_str += f" (+{len(authors) - 10} more)"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    frontmatter = (
        f"---\n"
        f'title: "{title}"\n'
        f'date: "{published}"\n'
        f"type: paper\n"
        f'source: "arxiv"\n'
        f'url: "{abs_url}"\n'
        f'arxiv_id: "{arxiv_id}"\n'
        f"ingestion_type: paper_ingest\n"
        f"refresh_policy: none\n"
        f"topics: {all_tags}\n"
        f'authors: "{authors_str}"\n'
        f'ingested_date: "{now}"\n'
        f"---\n\n"
    )

    body = (
        f"# {title}\n\n"
        f"**Authors**: {authors_str}\n"
        f"**Published**: {published}\n"
        f"**arxiv**: [{arxiv_id}]({abs_url})\n"
    )
    if pdf_link:
        body += f"**PDF**: [{arxiv_id}.pdf]({pdf_link})\n"
    body += (
        f"\n## Abstract\n\n{abstract}\n\n"
        f"## Categories\n\n{', '.join(categories)}\n"
    )

    content = frontmatter + body
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
                            "arxiv_id": arxiv_id,
                            "status": "unchanged",
                        }

                embedding = _embed(f"{title}\n\n{abstract}")

                cur.execute(
                    """
                    INSERT INTO vault_notes
                        (path, title, content, body, content_hash, embedding,
                         note_type, source, source_type, url, tags, note_date, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (path) DO UPDATE SET
                        title        = EXCLUDED.title,
                        content      = EXCLUDED.content,
                        body         = EXCLUDED.body,
                        content_hash = EXCLUDED.content_hash,
                        embedding    = EXCLUDED.embedding,
                        tags         = EXCLUDED.tags,
                        updated_at   = NOW()
                    """,
                    (vault_path, title, content, body, ch, embedding,
                     "paper", "arxiv", "arxiv_api", abs_url, all_tags, published),
                )
                conn.commit()

        status = "updated" if row else "created"
        return {
            "success": True,
            "path": vault_path,
            "title": title,
            "authors": authors_str,
            "arxiv_id": arxiv_id,
            "status": status,
        }
    except Exception as e:
        _logger.error("DB error ingesting paper %s: %s", arxiv_id, e)
        return {"success": False, "error": str(e)}
