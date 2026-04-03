#!/usr/bin/env python3
"""
cursor_adapter.py — Cursor session memory capture adapter.

Reads Cursor's state.vscdb (SQLite, cursorDiskKV table), extracts the
conversation specified by --conversation-id, and POSTs the turns to the
galdr memory REST bridge at http://localhost:8082/memory/ingest.

Requirements: Python 3.8+ standard library only (sqlite3, json, urllib).

Usage (called from agent-complete.ps1):
    python .cursor/hooks/cursor_adapter.py \
        --conversation-id <UUID> \
        --project-id     <proj_XXXX from .galdr/.project_id> \
        --project-path   <absolute path to project> \
        --platform       cursor \
        [--loop-count N] \
        [--status completed|partial] \
        [--mcp-url http://localhost:8082] \
        [--user-config ~/.galdr/user_config.json]
"""

import argparse
import hashlib
import json
import logging
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Logging (writes to .cursor/logs/cursor_adapter.log relative to cwd)
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [cursor_adapter] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("cursor_adapter")


# ---------------------------------------------------------------------------
# Cursor state.vscdb location
# ---------------------------------------------------------------------------

def find_state_vscdb() -> Optional[Path]:
    """Locate Cursor's state.vscdb in the platform-appropriate AppData path."""
    candidates = []

    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            candidates.append(Path(appdata) / "Cursor" / "User" / "globalStorage" / "state.vscdb")
        # Fallback: LOCALAPPDATA
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            candidates.append(Path(localappdata) / "Cursor" / "User" / "globalStorage" / "state.vscdb")
    elif sys.platform == "darwin":
        home = Path.home()
        candidates.append(home / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "state.vscdb")
    else:
        # Linux / WSL
        home = Path.home()
        candidates.append(home / ".config" / "Cursor" / "User" / "globalStorage" / "state.vscdb")

    for path in candidates:
        if path.exists():
            return path

    return None


# ---------------------------------------------------------------------------
# Auto-detect the most recent conversation from state.vscdb
# ---------------------------------------------------------------------------

def find_latest_conversation_id(db_path: Path) -> Optional[str]:
    """
    Find the most recently active Cursor conversation by scanning all
    composerData:* keys in state.vscdb and picking the one with the
    highest turn count or most recent bubbleId.

    Used as fallback when Cursor doesn't pass conversation_id in the hook
    event payload (which happens in most Cursor versions).
    """
    import shutil
    import tempfile

    tmp_fd, tmp_str = tempfile.mkstemp(suffix=".db")
    os.close(tmp_fd)
    tmp_path = Path(tmp_str)

    try:
        try:
            shutil.copy2(db_path, tmp_path)
        except Exception as e:
            logger.error(f"find_latest: failed to copy state.vscdb: {e}")
            return None

        conn = sqlite3.connect(str(tmp_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Fetch all composerData keys — each is a separate conversation
        cur.execute(
            "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'"
        )
        rows = cur.fetchall()
        conn.close()

        best_id = None
        best_bubble_count = -1

        for row in rows:
            key = row["key"] if isinstance(row, sqlite3.Row) else row[0]
            raw_value = row["value"] if isinstance(row, sqlite3.Row) else row[1]

            conv_id = key.split(":", 1)[1] if ":" in key else None
            if not conv_id:
                continue

            if isinstance(raw_value, (bytes, bytearray)):
                raw_value = raw_value.decode("utf-8", errors="replace")

            try:
                data = json.loads(raw_value)
            except Exception:
                continue

            headers = data.get("fullConversationHeadersOnly", [])
            bubble_count = len(headers)

            if bubble_count > best_bubble_count:
                best_bubble_count = bubble_count
                best_id = conv_id

        if best_id:
            logger.info(f"Auto-detected conversation: {best_id} ({best_bubble_count} bubbles)")
        else:
            logger.warning("Could not auto-detect any conversation from state.vscdb")

        return best_id

    finally:
        try:
            tmp_path.unlink()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Extract conversation from state.vscdb
# ---------------------------------------------------------------------------

def extract_turns_from_vscdb(db_path: Path, conversation_id: str) -> list[dict]:
    """
    Extract conversation turns from Cursor's state.vscdb.

    Cursor stores data in the cursorDiskKV table.
    Relevant key patterns (as of Cursor 0.48+):
      composerData:<conv_id>                     — conversation metadata + bubble headers
      bubbleId:<conv_id>:<bubble_id>             — individual message content
        type 1 = user/human message
        type 2 = AI/assistant response

    The file is locked by Cursor when running, so we copy it to a temp
    location before opening it (read-only, no WAL complications).

    Returns a list of {user, agent} dicts representing turns.
    """
    turns = []
    tmp_path: Optional[Path] = None

    try:
        # ----------------------------------------------------------------
        # Step 0: Copy the DB to bypass Cursor's exclusive file lock
        # ----------------------------------------------------------------
        import shutil
        import tempfile

        tmp_fd, tmp_str = tempfile.mkstemp(suffix=".db")
        os.close(tmp_fd)
        tmp_path = Path(tmp_str)

        try:
            shutil.copy2(db_path, tmp_path)
        except (OSError, shutil.Error) as e:
            logger.error(f"Failed to copy state.vscdb to temp: {e}")
            return turns

        conn = sqlite3.connect(str(tmp_path))
        conn.row_factory = sqlite3.Row

    except Exception as e:
        logger.error(f"Cannot open state.vscdb at {db_path}: {e}")
        return turns

    try:
        cur = conn.cursor()

        # ----------------------------------------------------------------
        # Step 1: Fetch composerData for this conversation
        # ----------------------------------------------------------------
        composer_key = f"composerData:{conversation_id}"
        cur.execute("SELECT value FROM cursorDiskKV WHERE key = ?", (composer_key,))
        row = cur.fetchone()

        if not row:
            # Fallback: partial match (helps if conversation_id is a prefix)
            cur.execute(
                "SELECT key, value FROM cursorDiskKV WHERE key LIKE ?",
                (f"composerData:%{conversation_id}%",),
            )
            rows = cur.fetchall()
            row = rows[0] if rows else None

        if not row:
            logger.warning(f"No composerData found for conversation_id={conversation_id}")
            conn.close()
            return turns

        raw_value = row["value"] if isinstance(row, sqlite3.Row) else row[0]
        if isinstance(raw_value, (bytes, bytearray)):
            raw_value = raw_value.decode("utf-8", errors="replace")

        try:
            composer_data = json.loads(raw_value)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse composerData JSON: {e}")
            conn.close()
            return turns

        # ----------------------------------------------------------------
        # Step 2: Extract bubble headers from fullConversationHeadersOnly
        # ----------------------------------------------------------------
        # Format (Cursor 0.48+): [{bubbleId: "<uuid>", type: 1|2}, ...]
        #   type 1 = user message, type 2 = AI response
        headers = composer_data.get("fullConversationHeadersOnly", [])

        # Fallback for older Cursor versions that stored bubbles inline
        if not headers:
            for key in ["bubbles", "conversation"]:
                val = composer_data.get(key, [])
                if isinstance(val, dict):
                    val = val.get("bubbles", [])
                if isinstance(val, list) and val:
                    headers = [
                        {"bubbleId": b.get("bubbleId"), "type": 1 if b.get("role") in ("user", "human") else 2}
                        for b in val if isinstance(b, dict) and b.get("bubbleId")
                    ]
                    break

        logger.info(f"Found {len(headers)} bubble headers for conversation {conversation_id}")

        # ----------------------------------------------------------------
        # Step 3: Fetch each bubble by "bubbleId:<conv_id>:<bubble_id>"
        # ----------------------------------------------------------------
        user_msg: Optional[str] = None

        for header in headers:
            bubble_id = header.get("bubbleId")
            bubble_type = header.get("type", 0)  # 1=user, 2=AI

            if not bubble_id:
                continue

            # Primary key format (Cursor 0.48+)
            bubble_key = f"bubbleId:{conversation_id}:{bubble_id}"
            cur.execute("SELECT value FROM cursorDiskKV WHERE key = ?", (bubble_key,))
            bubble_row = cur.fetchone()

            # Fallback: old format without conv_id prefix
            if not bubble_row:
                fallback_key = f"bubbleId:{bubble_id}"
                cur.execute("SELECT value FROM cursorDiskKV WHERE key = ?", (fallback_key,))
                bubble_row = cur.fetchone()

            if not bubble_row:
                # Some bubbles (tool calls, etc.) may not have stored content — skip
                continue

            raw_bubble = bubble_row["value"] if isinstance(bubble_row, sqlite3.Row) else bubble_row[0]
            if isinstance(raw_bubble, (bytes, bytearray)):
                raw_bubble = raw_bubble.decode("utf-8", errors="replace")

            try:
                bubble = json.loads(raw_bubble)
            except json.JSONDecodeError:
                continue

            # Extract text from the bubble object
            if isinstance(bubble, dict):
                text = bubble.get("text") or bubble.get("rawText") or bubble.get("content", "")
            else:
                text = str(bubble)

            if not isinstance(text, str):
                text = json.dumps(text)

            text = text.strip()

            # Pair user + AI messages into turns
            if bubble_type == 1:  # user
                user_msg = text
            elif bubble_type == 2:  # AI
                if text:  # skip empty AI bubbles (tool results, etc.)
                    turns.append({
                        "user": user_msg or "",
                        "agent": text,
                    })
                    user_msg = None

        # Flush dangling user message (session ended mid-turn)
        if user_msg:
            turns.append({"user": user_msg, "agent": ""})

        logger.info(f"Extracted {len(turns)} turns from conversation {conversation_id}")

    except Exception as e:
        logger.error(f"Unexpected error reading state.vscdb: {e}", exc_info=True)
    finally:
        conn.close()
        if tmp_path and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass

    return turns


# ---------------------------------------------------------------------------
# Load user / machine identity
# ---------------------------------------------------------------------------

def load_user_config(user_config_path: Optional[str] = None) -> dict:
    """
    Load user_id and machine_id from ~/.galdr/user_config.json.
    Creates the file with auto-generated UUIDs if it does not exist.
    """
    if user_config_path:
        config_path = Path(user_config_path)
    else:
        config_path = Path.home() / ".galdr" / "user_config.json"

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Auto-create with UUIDs derived from machine identifiers
    import uuid

    user_id = str(uuid.uuid4())

    machine_id = _detect_machine_id()
    if not machine_id:
        machine_id = str(uuid.uuid4())

    config = {
        "user_id": user_id,
        "machine_id": machine_id,
        "mcp_url": "http://localhost:8082",   # Override to point at your shared server
        "created_at": _utcnow_str(),
        "platform": sys.platform,
    }

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        logger.info(f"Created user config at {config_path}")
    except Exception as e:
        logger.warning(f"Could not write user config: {e}")

    return config


def _detect_machine_id() -> Optional[str]:
    """Try to read a stable machine ID from the OS."""
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
            )
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
            return value
        except Exception:
            pass
    elif sys.platform == "darwin":
        try:
            import subprocess
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                text=True,
            )
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    return line.split('"')[-2]
        except Exception:
            pass
    # Antigravity installation_id as fallback (cross-platform)
    antigravity_id_path = Path.home() / ".gemini" / "antigravity" / "installation_id"
    if antigravity_id_path.exists():
        try:
            return antigravity_id_path.read_text(encoding="utf-8").strip()
        except Exception:
            pass

    else:
        for path in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
            try:
                with open(path) as f:
                    return f.read().strip()
            except Exception:
                pass
    return None


def _utcnow_str() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Load project identity
# ---------------------------------------------------------------------------

def load_project_id(project_path: str) -> Optional[str]:
    """Read .galdr/.project_id from the project root."""
    pid_file = Path(project_path) / ".galdr" / ".project_id"
    if pid_file.exists():
        return pid_file.read_text(encoding="utf-8").strip()
    return None


# ---------------------------------------------------------------------------
# POST to memory REST bridge
# ---------------------------------------------------------------------------


def _write_fallback_cursor(project_path_str: str, project_id: str, conversation_id: str,
                           platform: str, turns: list, status: str, error: str) -> None:
    """Write session data to local fallback file when server is unavailable."""
    import datetime
    fallback_path = Path(project_path_str) / ".galdr" / "memory_fallback.jsonl"
    fallback_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "project_id": project_id,
        "conversation_id": conversation_id,
        "platform": platform,
        "project_path": project_path_str,
        "status": status,
        "error": error,
        "turns": turns,
        "fallback_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    with open(fallback_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    logger.warning("Fallback: session %s written to %s", conversation_id, fallback_path)


def post_to_memory_ingest(
    mcp_url: str,
    project_id: str,
    conversation_id: str,
    platform: str,
    project_path: str,
    turns: list,
    user_id: str = "",
    machine_id: str = "",
    loop_count: int = 0,
    status: str = "completed",
) -> bool:
    """POST turns to /memory/ingest. Returns True on success."""
    payload = {
        "project_id": project_id,
        "conversation_id": conversation_id,
        "platform": platform,
        "project_path": project_path,
        "display_name": Path(project_path).name if project_path else project_id,
        "user_id": user_id,
        "machine_id": machine_id,
        "loop_count": loop_count,
        "status": status,
        "turns": turns,
    }

    url = mcp_url.rstrip("/") + "/memory/ingest"
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    error_msg = ""
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
            result = json.loads(body)
            if result.get("success"):
                logger.info(
                    f"Ingested {result.get('ingested_turns', '?')} turns for "
                    f"conversation {conversation_id}"
                )
                return True
            else:
                logger.error(f"memory/ingest returned failure: {result}")
                return False
    except urllib.error.URLError as e:
        logger.error(f"Cannot reach galdr memory bridge at {url}: {e}")
        logger.error("Is the galdr Docker container running? (docker ps)")
        error_msg = str(e)
    except Exception as e:
        logger.error(f"Unexpected error calling memory/ingest: {e}", exc_info=True)
        error_msg = str(e)

    # Server unavailable — write to local fallback for later ingestion
    if project_path and error_msg:
        try:
            _write_fallback_cursor(project_path, project_id, conversation_id,
                                   platform, turns, status, error_msg)
        except Exception as fe:
            logger.error("Fallback write also failed: %s", fe)
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture a Cursor conversation into galdr agent memory."
    )
    parser.add_argument("--conversation-id", default=None, help="Cursor conversation UUID (auto-detected if omitted or 'unknown')")
    parser.add_argument("--project-id", default=None, help="galdr project UUID (reads .galdr/.project_id if omitted)")
    parser.add_argument("--project-path", default=None, help="Absolute path to project root (defaults to cwd)")
    parser.add_argument("--platform", default="cursor", help="Platform identifier (default: cursor)")
    parser.add_argument("--loop-count", type=int, default=0, help="Number of agent loops")
    parser.add_argument("--status", default="completed", choices=["completed", "partial"], help="Session status")
    # mcp_url priority: --mcp-url flag > user_config.json > localhost default
    _early_config: dict = {}
    _early_config_path = Path.home() / ".galdr" / "user_config.json"
    if _early_config_path.exists():
        try:
            import json as _json
            _early_config = _json.loads(_early_config_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    _default_mcp_url = _early_config.get("mcp_url", "http://localhost:8082")

    parser.add_argument("--mcp-url", default=_default_mcp_url,
                        help="galdr MCP server base URL (default from ~/.galdr/user_config.json or localhost:8082)")
    parser.add_argument("--user-config", default=None, help="Path to user_config.json")
    parser.add_argument("--vscdb", default=None, help="Override path to state.vscdb")
    args = parser.parse_args()

    # Resolve project path
    project_path = args.project_path or str(Path.cwd())

    # Load project ID
    project_id = args.project_id or load_project_id(project_path)
    if not project_id:
        # Fallback: generate a deterministic ID from the path
        import uuid
        project_id = "proj_" + hashlib.md5(project_path.encode()).hexdigest()[:8]
        logger.warning(f"No .galdr/.project_id found — using derived ID: {project_id}")

    # Load user identity
    user_config = load_user_config(args.user_config)
    user_id = user_config.get("user_id", "")
    machine_id = user_config.get("machine_id", "")

    # Find state.vscdb
    if args.vscdb:
        db_path = Path(args.vscdb)
    else:
        db_path = find_state_vscdb()

    if not db_path or not db_path.exists():
        logger.error(
            "state.vscdb not found. Cursor may not be installed or the path has changed. "
            "Use --vscdb to specify the path manually."
        )
        return 1

    logger.info(f"Using state.vscdb: {db_path}")

    # Resolve conversation_id — auto-detect if not provided or Cursor sent "unknown"
    conversation_id = args.conversation_id
    if not conversation_id or conversation_id.lower() in ("unknown", "none", ""):
        logger.info("conversation_id not provided by hook — auto-detecting from state.vscdb")
        conversation_id = find_latest_conversation_id(db_path)
        if not conversation_id:
            logger.error("Could not determine conversation_id — aborting capture")
            return 1

    # Extract turns
    turns = extract_turns_from_vscdb(db_path, conversation_id)
    if not turns:
        logger.warning(
            f"No turns extracted for conversation {args.conversation_id}. "
            "The conversation may be empty or use an unsupported Cursor format."
        )
        # Still call ingest so the session record is created (loop_count preserved)

    # POST to memory bridge
    ok = post_to_memory_ingest(
        mcp_url=args.mcp_url,
        project_id=project_id,
        conversation_id=conversation_id,
        platform=args.platform,
        project_path=project_path,
        turns=turns,
        user_id=user_id,
        machine_id=machine_id,
        loop_count=args.loop_count,
        status=args.status,
    )

    # Step-count reflection enrichment —————————————————————————————————————
    # If this session had enough turns, write (or enrich) a pending_reflection.json
    # so the NEXT session-start hook injects the memory-check reminder.
    #
    # We write here (after extraction) so we have the real turn count rather than
    # relying solely on the loop_count Cursor reports in the event payload.
    REFLECTION_TURN_THRESHOLD = 5
    if ok and len(turns) >= REFLECTION_TURN_THRESHOLD:
        _write_reflection_hint(
            project_path=project_path,
            conversation_id=conversation_id,
            turn_count=len(turns),
            turns=turns,
        )

    return 0 if ok else 2


def _write_reflection_hint(
    project_path: str,
    conversation_id: str,
    turn_count: int,
    turns: list[dict],
) -> None:
    """Write .cursor/logs/pending_reflection.json with richer metadata than
    agent-complete.ps1 can provide (actual turn count + topic hints)."""
    import time

    log_dir = Path(project_path) / ".cursor" / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        return

    reflection_file = log_dir / "pending_reflection.json"

    # Extract rough topic hints from first/last user messages
    recent_topics: list[str] = []
    user_msgs = [t.get("user", "") for t in turns if t.get("user")]
    if user_msgs:
        # First and last user messages give a sense of the session arc
        for msg in [user_msgs[0], user_msgs[-1]]:
            snippet = msg.strip()[:120].replace("\n", " ")
            if snippet:
                recent_topics.append(snippet)

    hint = {
        "conversation_id": conversation_id,
        "turn_count": turn_count,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "cursor_adapter",
        "recent_topics": recent_topics,
    }

    try:
        reflection_file.write_text(json.dumps(hint, indent=2), encoding="utf-8")
        logger.info(
            f"Reflection hint written ({turn_count} turns) → {reflection_file}"
        )
    except Exception as e:
        logger.warning(f"Could not write reflection hint: {e}")


if __name__ == "__main__":
    sys.exit(main())
