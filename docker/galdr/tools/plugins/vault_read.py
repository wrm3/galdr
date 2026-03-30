"""
Vault Read Tool Plugin

Read the full content of a vault note from the database by its path.
"""
import logging
from typing import Optional

TOOL_NAME = "vault_read"

TOOL_DESCRIPTION = (
    "Read the full content of a vault note from the database. "
    "Provide the relative path (e.g. 'videos/summaries/2026-03-21_mirofish.md'). "
    "Returns frontmatter, body, links, and metadata."
)

TOOL_PARAMS = {
    "path": "Relative path of the vault note (e.g. 'research/harvests/2026-03-21_react_patterns.md')",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(path: str) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}
    if not path:
        return {"success": False, "error": "Path is required"}

    with _db.get_cursor() as cur:
        cur.execute("""
            SELECT path, title, note_type, note_date, tags, aliases,
                   url, source, source_repo, source_type,
                   project_id, project_name,
                   content, body, frontmatter, links,
                   created_at, updated_at
            FROM vault_notes
            WHERE path = %s
        """, (path,))
        row = cur.fetchone()

    if not row:
        return {"success": False, "error": f"Note not found: {path}"}

    return {
        "success": True,
        "note": {
            "path": row["path"],
            "title": row["title"],
            "type": row["note_type"],
            "date": str(row["note_date"]) if row["note_date"] else None,
            "tags": row["tags"],
            "aliases": row["aliases"],
            "url": row.get("url", ""),
            "source": row.get("source", ""),
            "project_id": row.get("project_id", ""),
            "content": row["content"],
            "body": row["body"],
            "frontmatter": row["frontmatter"],
            "links": row["links"],
            "created_at": str(row["created_at"]),
            "updated_at": str(row["updated_at"]),
        },
    }
