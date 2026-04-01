"""
vault_export — Return vault_notes content ready for agents to write as .md files.

Respects C-001: Docker never touches the vault filesystem. This tool returns
{path, content} dicts; the calling agent writes files to the vault directory.
"""
import logging
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "vault_export"

TOOL_DESCRIPTION = (
    "Export vault_notes records as ready-to-write .md files. Returns {path, content} "
    "for each matching note. The agent writes these to the vault directory. "
    "Filters: note_type, since (ISO datetime), path_prefix, tags, unexported_only. "
    "Marks exported notes with exported_at timestamp to avoid re-export."
)

TOOL_PARAMS = {
    "note_type": "Filter by note type (e.g. 'video', 'github_repo', 'article', 'paper'). Optional.",
    "since": "Only notes created/updated after this ISO datetime (e.g. '2026-04-01T00:00:00Z'). Optional.",
    "path_prefix": "Filter by vault path prefix (e.g. 'ingested/youtube/'). Optional.",
    "tags": "Comma-separated tags to filter by. Optional.",
    "unexported_only": "Only return notes not yet exported (default: true).",
    "limit": "Max notes to return (default 50, max 200).",
    "offset": "Pagination offset (default 0).",
    "mark_exported": "Set exported_at on returned notes (default: true). Set false for dry-run.",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(
    note_type: Optional[str] = None,
    since: Optional[str] = None,
    path_prefix: Optional[str] = None,
    tags: Optional[str] = None,
    unexported_only: bool = True,
    limit: int = 50,
    offset: int = 0,
    mark_exported: bool = True,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    limit = min(max(1, int(limit)), 200)
    offset = max(0, int(offset))

    where_clauses = []
    params = []

    if note_type:
        where_clauses.append("note_type = %s")
        params.append(note_type)
    if since:
        where_clauses.append("updated_at >= %s")
        params.append(since)
    if path_prefix:
        where_clauses.append("path LIKE %s")
        params.append(f"{path_prefix}%")
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            where_clauses.append("tags && %s")
            params.append(tag_list)
    if unexported_only:
        where_clauses.append("exported_at IS NULL")

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    try:
        with _db.get_cursor() as cur:
            cur.execute(f"SELECT COUNT(*) AS cnt FROM vault_notes {where_sql}", params)
            total = cur.fetchone()["cnt"] if cur.rowcount else 0

            cur.execute(f"""
                SELECT id, path, title, content, note_type, url, tags, updated_at
                FROM vault_notes
                {where_sql}
                ORDER BY updated_at ASC
                LIMIT %s OFFSET %s
            """, params + [limit, offset])

            files = []
            ids_to_mark = []
            for row in cur.fetchall():
                files.append({
                    "path": row["path"],
                    "title": row["title"],
                    "content": row["content"],
                    "note_type": row["note_type"],
                    "url": row.get("url", ""),
                })
                ids_to_mark.append(row["id"])

            if mark_exported and ids_to_mark:
                now = datetime.now(timezone.utc)
                cur.execute(
                    "UPDATE vault_notes SET exported_at = %s WHERE id = ANY(%s)",
                    (now, ids_to_mark),
                )

        return {
            "success": True,
            "total_matching": total,
            "exported_count": len(files),
            "offset": offset,
            "limit": limit,
            "has_more": (offset + len(files)) < total,
            "files": files,
        }
    except Exception as e:
        _logger.error("vault_export error: %s", e)
        return {"success": False, "error": str(e)}
