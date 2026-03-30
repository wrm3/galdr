"""
Vault List Tool Plugin

Browse and list vault notes from the database. Supports filtering by type,
project, tags, and path prefix. Returns metadata without full content.
"""
import logging
from typing import Optional

TOOL_NAME = "vault_list"

TOOL_DESCRIPTION = (
    "List vault notes from the database. Filter by type, project, tags, or path prefix. "
    "Returns note metadata (path, title, type, date, tags) without full content. "
    "Use vault_read to fetch full content of a specific note."
)

TOOL_PARAMS = {
    "path_prefix": "Filter by path prefix (e.g. 'videos/', 'research/harvests/'). Optional.",
    "note_type": "Filter by note type (e.g. 'video_summary', 'harvest', 'research', 'platform_docs'). Optional.",
    "project_id": "Filter by project_id. Optional.",
    "tags": "Comma-separated tags to filter by. Optional.",
    "sort_by": "Sort field: 'updated' (default), 'created', 'title', 'date'",
    "limit": "Max results (default 25, max 100)",
    "offset": "Pagination offset (default 0)",
}

_db = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(
    path_prefix: Optional[str] = None,
    note_type: Optional[str] = None,
    project_id: Optional[str] = None,
    tags: Optional[str] = None,
    sort_by: str = "updated",
    limit: int = 25,
    offset: int = 0,
) -> dict:
    if not _db:
        return {"success": False, "error": "Database not configured"}

    limit = min(max(1, int(limit)), 100)
    offset = max(0, int(offset))

    where_clauses = []
    params = []

    if path_prefix:
        where_clauses.append("path LIKE %s")
        params.append(f"{path_prefix}%")
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
        where_sql = "WHERE " + " AND ".join(where_clauses)

    sort_map = {
        "updated": "updated_at DESC",
        "created": "created_at DESC",
        "title": "title ASC",
        "date": "note_date DESC NULLS LAST",
    }
    order_sql = sort_map.get(sort_by, "updated_at DESC")

    with _db.get_cursor() as cur:
        # Get total count
        cur.execute(f"SELECT COUNT(*) AS cnt FROM vault_notes {where_sql}", params)
        total = cur.fetchone()["cnt"] if cur.rowcount else 0

        # Get page
        cur.execute(f"""
            SELECT path, title, note_type, note_date, tags, url,
                   project_id, project_name,
                   LENGTH(body) AS body_length,
                   array_length(links, 1) AS link_count,
                   created_at, updated_at
            FROM vault_notes
            {where_sql}
            ORDER BY {order_sql}
            LIMIT %s OFFSET %s
        """, params + [limit, offset])

        notes = []
        for row in cur.fetchall():
            notes.append({
                "path": row["path"],
                "title": row["title"],
                "type": row["note_type"],
                "date": str(row["note_date"]) if row["note_date"] else None,
                "tags": row["tags"],
                "url": row.get("url", ""),
                "project_id": row.get("project_id", ""),
                "body_length": row["body_length"] or 0,
                "link_count": row["link_count"] or 0,
                "updated_at": str(row["updated_at"]),
            })

    return {
        "success": True,
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(notes),
        "notes": notes,
    }
