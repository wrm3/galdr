"""
File Index Plugin

Gives the AI agent full filesystem visibility — bypassing .gitignore limitations
in Cursor's Glob/Grep tools.

## Architecture (Postgres-backed, host-indexed)

The file walking runs on the HOST via .cursor/hooks/file_indexer.py, which
writes file metadata directly to the PostgreSQL `file_index` table (port 5433).
This MCP plugin reads from that same table (inside Docker via internal Postgres).

No volume mounts or file path juggling needed — Postgres is the shared layer.

## Host setup
    pip install psycopg2-binary
    python G:\\galdr\\.cursor\\hooks\\file_indexer.py

## Automatic rebuild
    session-start.ps1 calls file-index-rebuild.ps1 at session start (max 1x/12h)

## Tools
  - file_index(action='status')  : Show index stats (file count, roots, last indexed)
  - file_index(action='rebuild') : Return instructions for host-side rebuild
  - file_index(action='find')    : Search files by name glob or path prefix
  - file_index(action='grep')    : Regex search across file contents
  - file_index(action='read')    : Read a file's contents by absolute path
"""

import re
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "file_index"

TOOL_DESCRIPTION = (
    "File system indexer — gives the AI full filesystem visibility beyond what Cursor's "
    "Glob/Grep tools can see (they respect .gitignore; this does not). "
    "Sees .galdr/ tasks, research/, and all linked projects on G:\\\\ and P:\\\\. "
    "Actions: "
    "'status' — check index health (call this first); "
    "'rebuild' — get instructions to trigger a host-side rebuild; "
    "'find' — search indexed files by name glob (*.md) or path prefix; "
    "'grep' — regex search across file contents; "
    "'read' — read any file from disk by absolute path."
)

TOOL_PARAMS = {
    "action": (
        "Required. One of: 'status' | 'rebuild' | 'find' | 'grep' | 'read'. "
        "Call 'status' first to verify the index is populated. "
        "Call 'rebuild' to get instructions for refreshing the index."
    ),
    "pattern": (
        "For 'find': glob against filename (e.g. '*.md', 'TASK*.md', '*config*'). "
        "For 'grep': Python regex to match file contents (e.g. 'C-011', 'def setup', 'TODO')."
    ),
    "path_prefix": (
        "For 'find' or 'grep': filter to paths starting with this prefix. "
        "Examples: 'G:\\\\galdr\\\\.galdr', 'G:\\\\Maestro2', 'P:\\\\hieroglyphics'"
    ),
    "file_types": (
        "For 'grep': comma-separated extensions to limit scope. "
        "Example: '.md,.py,.ts'"
    ),
    "path": (
        "For 'read': absolute path to read. "
        "Example: 'G:\\\\galdr\\\\.galdr\\\\TASKS.md'"
    ),
    "max_results": "Max results to return (default: 50, max: 200).",
    "max_chars": "For 'read': max characters to return (default: 50000). Large files are paginated.",
    "offset_chars": "For 'read': start reading from this character offset (for pagination).",
    "context_lines": "For 'grep': lines of context around each match (default: 2).",
}

# ── Module state ───────────────────────────────────────────────────────────────
_db = None
_config = None


def setup(context: dict):
    global _db, _config
    _db = context.get("db")
    _config = context.get("config", {}) or {}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _table_exists() -> bool:
    if not _db:
        return False
    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'file_index'
                    )
                """)
                return bool(cur.fetchone()[0])
    except Exception:
        return False


# ── action: status ────────────────────────────────────────────────────────────

def _do_status() -> dict:
    if not _db:
        return {
            "success": False,
            "indexed": False,
            "error": "No database connection.",
        }
    if not _table_exists():
        return {
            "success": False,
            "indexed": False,
            "message": "file_index table does not exist. Run the host-side indexer.",
            "host_command": r"python G:\galdr\.cursor\hooks\file_indexer.py",
        }
    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM file_index")
                total = cur.fetchone()[0]
                cur.execute("""
                    SELECT root, COUNT(*) as cnt, MAX(indexed_at) as last_indexed
                    FROM file_index GROUP BY root ORDER BY root
                """)
                roots_info = [
                    {"root": row[0], "file_count": row[1],
                     "last_indexed": row[2].isoformat() if row[2] else None}
                    for row in cur.fetchall()
                ]
        return {
            "success": True,
            "indexed": total > 0,
            "total_files": total,
            "roots": roots_info,
            "tip": (
                "Index is ready. Use find/grep/read to explore files."
                if total > 0 else
                "Index is empty. Run: python G:\\galdr\\.cursor\\hooks\\file_indexer.py"
            ),
        }
    except Exception as e:
        return {"success": False, "error": f"Status query failed: {e}"}


# ── action: rebuild ────────────────────────────────────────────────────────────

def _do_rebuild() -> dict:
    return {
        "success": False,
        "action_required": "host",
        "message": "Run one of these in a host terminal to rebuild the file index:",
        "commands": {
            "powershell": r"& 'G:\galdr\.cursor\hooks\file-index-rebuild.ps1'",
            "powershell_force": r"& 'G:\galdr\.cursor\hooks\file-index-rebuild.ps1' -Force",
            "python": r"python G:\galdr\.cursor\hooks\file_indexer.py",
            "python_force": r"python G:\galdr\.cursor\hooks\file_indexer.py --force",
        },
        "auto_rebuild": (
            "session-start.ps1 runs this automatically at session start (max 1x per 12h). "
            "After running, call file_index(action='status') to confirm."
        ),
    }


# ── action: find ──────────────────────────────────────────────────────────────

def _do_find(pattern: Optional[str], path_prefix: Optional[str], max_results: int) -> dict:
    if not _db:
        return {"error": "No database connection."}
    if not _table_exists():
        return {
            "error": "file_index table not found.",
            "tip": r"Run: python G:\galdr\.cursor\hooks\file_indexer.py",
        }

    with _db.get_connection() as conn:
        with conn.cursor() as cur:
            conditions = []
            params = []

            if pattern:
                sql_pat = pattern.replace("*", "%").replace("?", "_")
                conditions.append("filename ILIKE %s")
                params.append(sql_pat)

            if path_prefix:
                prefix = path_prefix.rstrip("\\/")
                # Use lower() comparison to avoid case issues on Windows paths
                conditions.append("LOWER(abs_path) LIKE LOWER(%s)")
                params.append(prefix.replace("\\", "\\\\") + "%")

            where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            params.append(min(max_results, 200))

            cur.execute(f"""
                SELECT abs_path, filename, ext, size_bytes, modified_at, root
                FROM file_index {where}
                ORDER BY modified_at DESC NULLS LAST
                LIMIT %s
            """, params)
            rows = cur.fetchall()

            # Total count
            cur.execute(f"SELECT COUNT(*) FROM file_index {where}", params[:-1])
            total = cur.fetchone()[0]

    results = [
        {
            "path": row[0], "filename": row[1], "ext": row[2] or "",
            "size_bytes": row[3],
            "modified": row[4].isoformat() if row[4] else None,
            "root": row[5],
        }
        for row in rows
    ]

    return {
        "success": True,
        "count": len(results),
        "total_matching": total,
        "results": results,
        "truncated": total > len(results),
        "tip": (
            "Use file_index(action='read', path='...') to read any file. "
            "Use file_index(action='grep') to search file contents."
        ) if results else (
            "No matches. Verify index with file_index(action='status')."
        ),
    }


# ── action: grep ──────────────────────────────────────────────────────────────

def _do_grep(
    pattern: str,
    file_types: Optional[str],
    path_prefix: Optional[str],
    max_results: int,
    context_lines: int,
) -> dict:
    if not _db:
        return {"error": "No database connection."}
    if not _table_exists():
        return {"error": "file_index table not found. Run host-side indexer first."}

    with _db.get_connection() as conn:
        with conn.cursor() as cur:
            conditions = []
            params = []

            if file_types:
                exts = [
                    e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
                    for e in file_types.split(",")
                ]
                placeholders = ",".join(["%s"] * len(exts))
                conditions.append(f"ext IN ({placeholders})")
                params.extend(exts)

            if path_prefix:
                prefix = path_prefix.rstrip("\\/")
                conditions.append("LOWER(abs_path) LIKE LOWER(%s)")
                params.append(prefix.replace("\\", "\\\\") + "%")

            where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cur.execute(f"SELECT abs_path FROM file_index {where} ORDER BY modified_at DESC NULLS LAST", params)
            candidates = [row[0] for row in cur.fetchall()]

    if not candidates:
        return {
            "success": True, "count": 0, "results": [],
            "tip": "No files match filters. Check file_index(action='status').",
        }

    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        return {"error": f"Invalid regex: {e}"}

    matches = []
    files_searched = 0
    files_with_match = 0

    for abs_path in candidates:
        if files_with_match >= max_results:
            break
        try:
            with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            files_searched += 1
            file_matches = []
            for i, line in enumerate(lines):
                if rx.search(line):
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    ctx = [
                        f"{j+1}{'>' if j == i else ' '} {lines[j].rstrip()}"
                        for j in range(start, end)
                    ]
                    file_matches.append({
                        "line": i + 1,
                        "match": line.rstrip(),
                        "context": "\n".join(ctx),
                    })
            if file_matches:
                files_with_match += 1
                matches.append({
                    "path": abs_path,
                    "match_count": len(file_matches),
                    "matches": file_matches[:10],
                })
        except (PermissionError, OSError, UnicodeDecodeError):
            pass
        except Exception as ex:
            logger.debug(f"file_grep: skipped {abs_path}: {ex}")

    return {
        "success": True,
        "pattern": pattern,
        "files_searched": files_searched,
        "files_with_match": files_with_match,
        "results": matches,
        "truncated": files_with_match >= max_results,
    }


# ── action: read ──────────────────────────────────────────────────────────────

def _do_read(path: str, max_chars: int, offset_chars: int) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        return {
            "error": f"File not found: {path}",
            "tip": "Use file_index(action='find', pattern='filename.ext') to locate it first.",
        }
    if not file_path.is_file():
        return {"error": f"Not a file: {path}"}
    try:
        size = file_path.stat().st_size
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            if offset_chars:
                f.read(offset_chars)
            content = f.read(max_chars)
        truncated = len(content) >= max_chars
        end = offset_chars + len(content)
        return {
            "success": True,
            "path": str(file_path),
            "size_bytes": size,
            "offset_chars": offset_chars,
            "chars_returned": len(content),
            "truncated": truncated,
            "next_offset_chars": end if truncated else None,
            "content": content,
            "tip": f"Large file — call with offset_chars={end} for next chunk." if truncated else None,
        }
    except PermissionError:
        return {"error": f"Permission denied: {path}"}
    except Exception as e:
        return {"error": f"Read failed: {e}"}


# ── Main dispatcher ────────────────────────────────────────────────────────────

async def execute(
    action: str,
    pattern: Optional[str] = None,
    path_prefix: Optional[str] = None,
    file_types: Optional[str] = None,
    path: Optional[str] = None,
    max_results: int = 50,
    max_chars: int = 50000,
    offset_chars: int = 0,
    context_lines: int = 2,
) -> dict:
    action = action.strip().lower()

    if action == "status":
        return _do_status()

    elif action == "rebuild":
        return _do_rebuild()

    elif action == "find":
        if not pattern and not path_prefix:
            return {"error": "find requires at least one of: pattern, path_prefix"}
        return _do_find(pattern, path_prefix, min(max_results, 200))

    elif action == "grep":
        if not pattern:
            return {"error": "grep requires: pattern (Python regex)"}
        return _do_grep(
            pattern, file_types, path_prefix,
            min(max_results, 200), max(0, min(context_lines, 10)),
        )

    elif action == "read":
        if not path:
            return {"error": "read requires: path (absolute file path)"}
        return _do_read(path, max(1, min(max_chars, 1_000_000)), max(0, offset_chars))

    else:
        return {
            "error": f"Unknown action: '{action}'",
            "valid_actions": ["status", "rebuild", "find", "grep", "read"],
        }
