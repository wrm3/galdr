"""
sync_ws.py — WebSocket endpoint for .galdr/ and vault file synchronization.

Protocol:
  Client connects: ws://server:8082/sync/{project_id}?user_id={user_id}
  Client sends JSON messages:
    { "type": "file_changed", "path": "TASKS.md", "content": "...", "hash": "abc123",
      "file_type": "galdr" }
    { "type": "file_changed", "path": "notes/research.md", "content": "...", "hash": "def456",
      "file_type": "vault" }
    { "type": "sync_request" }   -- request all files for this project
    { "type": "ping" }

  Server responds:
    { "type": "ack", "path": "TASKS.md", "version": 5 }
    { "type": "sync_response", "files": [...] }
    { "type": "file_broadcast", "path": "...", "content": "...", "hash": "...",
      "sender": "user_id" }
    { "type": "pong" }
    { "type": "error", "message": "..." }

Design: One project_id = one user. No multi-user conflict resolution.
Vault files are shared across users on the same server.
"""

import hashlib
import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional

from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

_db = None

# Connected clients: { project_id: set(websocket) }
# Used for broadcasting vault file changes
_connections: dict[str, set[WebSocket]] = defaultdict(set)

# Vault subscribers: { vault_id: set(websocket) }
_vault_connections: dict[str, set[WebSocket]] = defaultdict(set)


def init_sync_ws(db) -> None:
    global _db
    _db = db


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


async def _upsert_file(project_id: str, file_path: str, content: str,
                       content_hash: str, file_type: str,
                       user_id: Optional[str] = None) -> int:
    """Store or update a file in project_files. Returns the new version."""
    if not _db:
        return 0

    with _db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO project_files
                    (project_id, file_path, content, content_hash, version,
                     file_type, last_modified_by, updated_at)
                VALUES (%s, %s, %s, %s, 1, %s, %s, NOW())
                ON CONFLICT (project_id, file_path) DO UPDATE
                    SET content         = EXCLUDED.content,
                        content_hash    = EXCLUDED.content_hash,
                        version         = project_files.version + 1,
                        file_type       = EXCLUDED.file_type,
                        last_modified_by = EXCLUDED.last_modified_by,
                        updated_at      = NOW()
                RETURNING version
                """,
                (project_id, file_path, content, content_hash,
                 file_type, user_id),
            )
            version = cur.fetchone()[0]
            conn.commit()
    return version


async def _get_all_files(project_id: str,
                         file_type: Optional[str] = None) -> list[dict]:
    """Retrieve all files for a project from project_files table."""
    if not _db:
        return []

    sql = """
        SELECT file_path, content, content_hash, version, file_type, updated_at
        FROM project_files
        WHERE project_id = %s
    """
    params: list = [project_id]
    if file_type:
        sql += " AND file_type = %s"
        params.append(file_type)
    sql += " ORDER BY file_path"

    with _db.get_cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    return [
        {
            "path": row["file_path"],
            "content": row["content"],
            "hash": row["content_hash"],
            "version": row["version"],
            "file_type": row["file_type"],
            "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
        }
        for row in rows
    ]


async def _broadcast_to_vault(vault_id: str, sender: WebSocket,
                              message: dict) -> None:
    """Broadcast a vault file change to all connected clients on the same vault."""
    dead: list[WebSocket] = []
    for ws in _vault_connections.get(vault_id, set()):
        if ws is sender:
            continue
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _vault_connections[vault_id].discard(ws)


async def handle_sync_ws(websocket: WebSocket) -> None:
    """WebSocket handler for file synchronization."""
    project_id = websocket.path_params.get("project_id", "")
    user_id = websocket.query_params.get("user_id", "")
    vault_id = websocket.query_params.get("vault_id", "")

    if not project_id:
        await websocket.close(code=4000, reason="project_id required")
        return

    await websocket.accept()
    _connections[project_id].add(websocket)
    if vault_id:
        _vault_connections[vault_id].add(websocket)

    logger.info("WebSocket connected: project=%s user=%s vault=%s",
                project_id, user_id, vault_id)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error", "message": "Invalid JSON"
                })
                continue

            msg_type = msg.get("type", "")

            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})

            elif msg_type == "file_changed":
                path = msg.get("path", "")
                content = msg.get("content", "")
                file_type = msg.get("file_type", "galdr")
                content_hash = msg.get("hash") or _sha256(content)

                if not path:
                    await websocket.send_json({
                        "type": "error", "message": "path required"
                    })
                    continue

                version = await _upsert_file(
                    project_id, path, content, content_hash,
                    file_type, user_id,
                )

                await websocket.send_json({
                    "type": "ack",
                    "path": path,
                    "version": version,
                    "file_type": file_type,
                })

                if file_type == "vault" and vault_id:
                    await _broadcast_to_vault(vault_id, websocket, {
                        "type": "file_broadcast",
                        "path": path,
                        "content": content,
                        "hash": content_hash,
                        "file_type": "vault",
                        "sender": user_id,
                        "version": version,
                    })

                    await _auto_index_vault_file(path, content, project_id)

            elif msg_type == "sync_request":
                file_type = msg.get("file_type")
                files = await _get_all_files(project_id, file_type)
                await websocket.send_json({
                    "type": "sync_response",
                    "files": files,
                    "count": len(files),
                })

            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}",
                })

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: project=%s user=%s",
                    project_id, user_id)
    except Exception as e:
        logger.error("WebSocket error: %s", e)
    finally:
        _connections[project_id].discard(websocket)
        if vault_id:
            _vault_connections[vault_id].discard(websocket)


async def _auto_index_vault_file(path: str, content: str,
                                 project_id: str) -> None:
    """Auto-index vault files into vault_notes for search (best-effort).
    Uses the vault_sync plugin's _ingest_note for full frontmatter parsing."""
    if not _db:
        return
    try:
        from .tools.plugins.vault_sync import _ingest_note
        _ingest_note(path, content)
    except Exception as e:
        logger.debug("Auto-index vault file failed (non-fatal): %s", e)


# Route list — imported by server.py
SYNC_ROUTES = [
    WebSocketRoute("/sync/{project_id}", handle_sync_ws),
]
