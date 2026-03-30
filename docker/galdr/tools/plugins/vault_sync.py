"""
Vault Sync Tool Plugin

Indexes vault note content into the vault_notes PostgreSQL table with
pgvector embeddings. The agent reads the file on the host and passes
the content here — Docker never touches the filesystem.

Two modes:
  - "ingest": Agent passes path + content directly (primary mode)
  - "delete": Remove a DB entry by path (for cleanup)
"""
import hashlib
import json
import logging
import re
from typing import Optional

TOOL_NAME = "vault_sync"

TOOL_DESCRIPTION = (
    "Index a vault note into the database for semantic search. "
    "The agent reads the local file and passes its content here. "
    "Example: vault_sync(path='videos/summaries/2026-03-21_video.md', content='---\\ndate: ...\\n---\\n# Title\\n...') "
    "Docker never reads the vault filesystem — the agent is the bridge."
)

TOOL_PARAMS = {
    "path": "Relative path of the note within the vault (e.g. 'videos/summaries/2026-03-21_video.md')",
    "content": "Full markdown content of the note (including YAML frontmatter). Required for ingest mode.",
    "mode": "Mode: 'ingest' (default — upsert note into DB) or 'delete' (remove note from DB by path)",
}

_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def setup(context: dict):
    global _db, _embedding_gen
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")


def _parse_frontmatter(content: str) -> dict:
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
            fm[key.strip()] = val
    return fm


def _get_body(content: str) -> str:
    match = FRONTMATTER_RE.match(content)
    if match:
        return content[match.end():].strip()
    return content.strip()


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _ingest_note(path: str, content: str) -> dict:
    """Parse and upsert a single note into the database."""
    ch = _content_hash(content)

    with _db.get_cursor() as cur:
        cur.execute("SELECT content_hash FROM vault_notes WHERE path = %s", (path,))
        row = cur.fetchone()
        if row and (row.get("content_hash") if isinstance(row, dict) else list(row.values())[0]) == ch:
            return {"path": path, "status": "unchanged"}

    fm = _parse_frontmatter(content)
    body = _get_body(content)
    links = LINK_RE.findall(content)

    title = fm.get("title", "")
    if not title:
        for line in body.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title:
            title = path.rsplit("/", 1)[-1].replace(".md", "")

    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    aliases = fm.get("aliases", [])
    if isinstance(aliases, str):
        aliases = [aliases]

    embedding = None
    if _embedding_gen and body:
        try:
            embed_text = f"{title}\n\n{body[:8000]}"
            embedding = _embedding_gen.generate(embed_text)
        except Exception as e:
            _logger.warning(f"Embedding generation failed for {path}: {e}")

    note_date = fm.get("date")

    with _db.get_cursor() as cur:
        cur.execute("""
            INSERT INTO vault_notes
                (path, project_id, project_name, title, note_date, note_type,
                 source, tags, aliases, url, source_repo, source_type,
                 content, body, frontmatter, links, content_hash, embedding, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (path) DO UPDATE SET
                project_id = EXCLUDED.project_id,
                project_name = EXCLUDED.project_name,
                title = EXCLUDED.title,
                note_date = EXCLUDED.note_date,
                note_type = EXCLUDED.note_type,
                source = EXCLUDED.source,
                tags = EXCLUDED.tags,
                aliases = EXCLUDED.aliases,
                url = EXCLUDED.url,
                source_repo = EXCLUDED.source_repo,
                source_type = EXCLUDED.source_type,
                content = EXCLUDED.content,
                body = EXCLUDED.body,
                frontmatter = EXCLUDED.frontmatter,
                links = EXCLUDED.links,
                content_hash = EXCLUDED.content_hash,
                embedding = EXCLUDED.embedding,
                updated_at = NOW()
        """, (
            path,
            fm.get("project_id", ""),
            fm.get("project", ""),
            title,
            note_date if note_date else None,
            fm.get("type", ""),
            fm.get("source", ""),
            tags,
            aliases,
            fm.get("url", ""),
            fm.get("source_repo", ""),
            fm.get("source_type", ""),
            content,
            body,
            json.dumps(fm),
            links,
            ch,
            embedding,
        ))

    status = "updated" if row else "created"
    return {"path": path, "status": status, "title": title}


async def execute(
    path: str,
    content: Optional[str] = None,
    mode: str = "ingest",
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not path:
        return {"success": False, "error": "path is required"}

    if mode == "delete":
        with _db.get_cursor() as cur:
            cur.execute("DELETE FROM vault_notes WHERE path = %s", (path,))
            deleted = cur.rowcount
        return {"success": True, "mode": "delete", "path": path, "deleted": deleted}

    if not content:
        return {"success": False, "error": "content is required for ingest mode. Agent must read the file and pass its content."}

    try:
        result = _ingest_note(path, content)
        return {"success": True, "mode": "ingest", "result": result}
    except Exception as e:
        _logger.error(f"Failed to ingest {path}: {e}")
        return {"success": False, "error": str(e)}
