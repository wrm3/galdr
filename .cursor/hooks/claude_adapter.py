"""
claude_adapter.py — Claude Code session ingestion for galdr memory system

Reads ~/.claude/projects/<encoded-path>/<session>.jsonl and POSTs conversation
turns to the galdr memory REST bridge at http://localhost:8082/memory/ingest.

Usage (called by Claude Code stop hook or manually):
    python claude_adapter.py [--session-id UUID] [--project-path PATH] [--status STATUS]

Claude Code stop hook passes:
    CLAUDE_SESSION_ID  - env var with session UUID
    CLAUDE_PROJECT_DIR - env var with project working directory

Standalone:
    python claude_adapter.py --session-id <uuid> --project-path G:\\galdr
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [claude_adapter] %(levelname)s %(message)s",
)
logger = logging.getLogger("claude_adapter")

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"
USER_CONFIG_PATH = Path.home() / ".galdr" / "user_config.json"
HTTP_TIMEOUT = 120  # seconds — ingestion can be slow for large sessions

DEFAULT_MCP_URL = "http://localhost:8082"   # overridden by user_config.json or --mcp-url flag


def _get_configured_mcp_url() -> str:
    """Read mcp_url from ~/.galdr/user_config.json, fall back to localhost."""
    if USER_CONFIG_PATH.exists():
        try:
            cfg = json.loads(USER_CONFIG_PATH.read_text(encoding="utf-8"))
            return cfg.get("mcp_url", DEFAULT_MCP_URL).rstrip("/")
        except Exception:
            pass
    return DEFAULT_MCP_URL


# ---------------------------------------------------------------------------
# Identity helpers
# ---------------------------------------------------------------------------

def load_user_config() -> dict:
    """Load or create ~/.galdr/user_config.json."""
    import uuid as uuid_mod

    config_dir = USER_CONFIG_PATH.parent
    config_dir.mkdir(parents=True, exist_ok=True)

    if USER_CONFIG_PATH.exists():
        try:
            return json.loads(USER_CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Generate new identity
    machine_id = _get_machine_id()
    config = {
        "user_id": str(uuid_mod.uuid4()),
        "machine_id": machine_id,
        "mcp_url": "http://localhost:8082",   # Override to point at your shared server
        "created": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    }
    USER_CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    logger.info("Created new user_config.json: user_id=%s", config["user_id"])
    return config


def _get_machine_id() -> str:
    """Get a stable machine identifier."""
    import sys
    # Try Windows MachineGuid
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
            )
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
            return str(value)
        except Exception:
            pass

    # Try Antigravity installation_id (cross-platform)
    antigravity_id = Path.home() / ".gemini" / "antigravity" / "installation_id"
    if antigravity_id.exists():
        try:
            return antigravity_id.read_text(encoding="utf-8").strip()
        except Exception:
            pass

    # VS Code / Cursor devDeviceId (Windows)
    if sys.platform == "win32":
        import os as _os
        for vscode_storage in [
            _os.path.expandvars(r"%APPDATA%\Cursor\User\globalStorage\storage.json"),
            _os.path.expandvars(r"%APPDATA%\Code\User\globalStorage\storage.json"),
        ]:
            try:
                with open(vscode_storage, encoding="utf-8") as f:
                    vsc_data = json.load(f)
                dev_id = vsc_data.get("telemetry.devDeviceId") or vsc_data.get(
                    "telemetry", {}
                ).get("devDeviceId")
                if dev_id:
                    return str(dev_id)
            except Exception:
                pass

    # Linux: /etc/machine-id
    for machine_id_path in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
        try:
            with open(machine_id_path) as f:
                return f.read().strip()
        except Exception:
            pass

    # macOS: ioreg
    if sys.platform == "darwin":
        try:
            import subprocess
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"], text=True
            )
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    return line.split('"')[-2]
        except Exception:
            pass

    # Final fallback: MAC address-based UUID
    import uuid as uuid_mod
    return str(uuid_mod.getnode())


def load_project_id(project_path: Path) -> str:
    """Read .galdr/.project_id or derive a deterministic ID."""
    project_id_file = project_path / ".galdr" / ".project_id"
    if project_id_file.exists():
        pid = project_id_file.read_text(encoding="utf-8").strip()
        if pid:
            return pid
    # Derive deterministic ID from project path
    proj_hash = hashlib.sha256(str(project_path).encode()).hexdigest()[:8]
    derived = f"proj_{proj_hash}"
    logger.warning("No .galdr/.project_id found — using derived ID: %s", derived)
    return derived


# ---------------------------------------------------------------------------
# Project directory resolution
# ---------------------------------------------------------------------------

def _path_to_claude_dirname(project_path: Path) -> str:
    """
    Convert a Windows project path to Claude Code's project directory name.

    Examples:
        G:\\galdr  → g--galdr-rules
        G:\\Maestro2     → g--Maestro2
        C:\\Users\\foo   → c--Users-foo

    Observed transformation rules:
      - Drive letter: lowercased
      - Colon ':' → '-'
      - Backslash '\\' → '-'
      - Underscore '_' → '-'
      - Forward slash '/' → '-'
    """
    path_str = str(project_path)
    result = ""
    for ch in path_str:
        if ch == ":":
            result += "-"
        elif ch in ("\\/"):
            result += "-"
        elif ch == "_":
            result += "-"
        elif ch == " ":
            result += "-"
        else:
            result += ch
    # Lowercase the drive letter only (first char)
    if result:
        result = result[0].lower() + result[1:]
    return result


def find_claude_project_dir(project_path: Path) -> Optional[Path]:
    """
    Find the ~/.claude/projects/ subdirectory for this project.

    Tries the encoded name first; falls back to scanning all subdirs and
    comparing their name against candidate encodings.
    """
    if not CLAUDE_PROJECTS_DIR.exists():
        return None

    # Primary attempt: direct encoding
    encoded = _path_to_claude_dirname(project_path)
    candidate = CLAUDE_PROJECTS_DIR / encoded
    if candidate.exists():
        return candidate

    # Fallback: scan all subdirs for a name match (case-insensitive)
    encoded_lower = encoded.lower()
    for subdir in CLAUDE_PROJECTS_DIR.iterdir():
        if subdir.is_dir() and subdir.name.lower() == encoded_lower:
            return subdir

    logger.warning(
        "No Claude project dir found for %s (tried: %s)", project_path, encoded
    )
    return None


# ---------------------------------------------------------------------------
# JSONL parsing
# ---------------------------------------------------------------------------

def find_jsonl_file(project_dir: Path, session_id: Optional[str] = None) -> Optional[Path]:
    """Return the JSONL file path for the given session (or the most recent one)."""
    if session_id:
        p = project_dir / f"{session_id}.jsonl"
        if p.exists():
            return p
        logger.warning("JSONL not found for session %s in %s", session_id, project_dir)

    # Most recently modified JSONL in the project dir (flat files only)
    jsonl_files = sorted(
        [f for f in project_dir.iterdir() if f.is_file() and f.suffix == ".jsonl"],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if jsonl_files:
        logger.info("Using most recent JSONL: %s", jsonl_files[0].name)
        return jsonl_files[0]

    return None


def _extract_text_from_content(content_blocks: list) -> tuple[str, list[str], list[str]]:
    """
    Extract text, tool names, and file references from a message content array.
    Skips 'thinking' blocks (Claude extended thinking).

    Returns:
        (text, tool_names, file_refs)
    """
    _FILE_TOOLS = {
        "read_file", "write_file", "edit_file", "create_file", "delete_file",
        "str_replace", "str_replace_editor", "view", "insert", "undo_edit",
    }
    parts: list[str] = []
    tool_names: list[str] = []
    file_refs: list[str] = []

    for block in content_blocks if isinstance(content_blocks, list) else []:
        if not isinstance(block, dict):
            continue
        btype = block.get("type", "")

        if btype == "text":
            text = block.get("text", "")
            if text:
                parts.append(text)

        elif btype == "tool_use":
            tname = block.get("name", "")
            if tname:
                tool_names.append(tname)
            # Extract file paths from tool input
            inp = block.get("input", {})
            if isinstance(inp, dict):
                for fkey in ("path", "file_path", "target_file", "filename"):
                    fval = inp.get(fkey)
                    if fval and isinstance(fval, str) and fval not in file_refs:
                        file_refs.append(fval)
                # edit_file / str_replace passes path at top level
                if tname in _FILE_TOOLS:
                    p = inp.get("path") or inp.get("file_path") or inp.get("target_file")
                    if p and p not in file_refs:
                        file_refs.append(p)

        elif btype == "tool_result":
            # tool_result blocks contain file content; skip text but note the path if available
            pass

    return "\n".join(parts), list(dict.fromkeys(tool_names)), list(dict.fromkeys(file_refs))


def extract_turns_from_jsonl(jsonl_path: Path) -> list[dict]:
    """
    Parse a Claude Code JSONL file and return a list of enriched turn dicts:

        [{
          "user":             "...",
          "agent":            "...",
          "tool_names":       ["read_file", "bash", ...],
          "file_refs":        ["src/app.py", ...],
          "session_metadata": {"gitBranch": "main", "cwd": "/path/...", "version": "..."},
        }, ...]

    Strategy:
    - type="user"      → pending user message
    - type="assistant" → only accept lines where stop_reason is set (final streaming chunk)
    - type="system"    → extract session metadata (gitBranch, cwd, version, etc.)
    - type="progress", "queue-operation", "file-history-snapshot" → skip
    """
    turns: list[dict] = []
    pending_user: Optional[str] = None
    pending_tools: list[str] = []
    pending_files: list[str] = []
    session_metadata: dict = {}

    try:
        with open(jsonl_path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = obj.get("type", "")

                # ── Session metadata from system messages ──────────────────
                if msg_type == "system":
                    for mkey in ("gitBranch", "cwd", "version", "requestId",
                                 "model", "sessionId"):
                        val = obj.get(mkey)
                        if val is not None and mkey not in session_metadata:
                            session_metadata[mkey] = str(val)
                    continue

                if msg_type in ("progress", "queue-operation",
                                "file-history-snapshot", "result"):
                    continue

                # ── User message ───────────────────────────────────────────
                if msg_type == "user":
                    msg = obj.get("message", {})
                    content = msg.get("content", [])
                    if isinstance(content, str):
                        text = content
                        tnames, frefs = [], []
                    else:
                        text, tnames, frefs = _extract_text_from_content(content)

                    if text.strip():
                        if pending_user is not None:
                            turns.append({
                                "user": pending_user, "agent": "",
                                "tool_names": pending_tools,
                                "file_refs": pending_files,
                                "session_metadata": dict(session_metadata),
                            })
                        pending_user = text.strip()
                        pending_tools = list(tnames)
                        pending_files = list(frefs)

                # ── Assistant message ──────────────────────────────────────
                elif msg_type == "assistant":
                    msg = obj.get("message", {})
                    if not msg.get("stop_reason"):
                        continue
                    content = msg.get("content", [])
                    agent_text, tnames, frefs = _extract_text_from_content(content)
                    agent_text = agent_text.strip()

                    # Accumulate tools/files from the assistant's response too
                    all_tools = list(dict.fromkeys(pending_tools + tnames))
                    all_files = list(dict.fromkeys(pending_files + frefs))

                    if agent_text or all_tools:
                        if pending_user is not None:
                            turns.append({
                                "user": pending_user,
                                "agent": agent_text,
                                "tool_names": all_tools,
                                "file_refs": all_files,
                                "session_metadata": dict(session_metadata),
                            })
                            pending_user = None
                            pending_tools = []
                            pending_files = []
                        else:
                            turns.append({
                                "user": "",
                                "agent": agent_text,
                                "tool_names": all_tools,
                                "file_refs": all_files,
                                "session_metadata": dict(session_metadata),
                            })

        # Flush any trailing user message with no assistant response
        if pending_user is not None:
            turns.append({
                "user": pending_user, "agent": "",
                "tool_names": pending_tools,
                "file_refs": pending_files,
                "session_metadata": dict(session_metadata),
            })

    except OSError as e:
        logger.error("Cannot read JSONL %s: %s", jsonl_path, e)

    return turns


# ---------------------------------------------------------------------------
# REST ingestion
# ---------------------------------------------------------------------------

def _write_fallback(project_path: Path, project_id: str, session_id: str,
                    turns: list, status: str, error: str) -> None:
    """Write session data to local fallback file when server is unavailable."""
    fallback_path = project_path / ".galdr" / "memory_fallback.jsonl"
    fallback_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "project_id": project_id,
        "conversation_id": session_id,
        "platform": "claude_code",
        "status": status,
        "error": error,
        "turns": turns,
        "fallback_timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    }
    with open(fallback_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    logger.warning("Fallback: session %s written to %s", session_id, fallback_path)


def post_to_memory_ingest(
    project_id: str,
    session_id: str,
    turns: list[dict],
    status: str = "completed",
    mcp_url: Optional[str] = None,
    project_path: Optional[Path] = None,
) -> bool:
    """POST extracted turns to the galdr memory REST bridge."""
    ingest_url = (mcp_url or _get_configured_mcp_url()).rstrip("/") + "/memory/ingest"
    payload = {
        "project_id": project_id,
        "conversation_id": session_id,
        "platform": "claude_code",
        "status": status,
        "turns": turns,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ingest_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            ingested = body.get("ingested_turns", body.get("ingested", 0))
            total = body.get("total_turns", len(turns))
            logger.info(
                "Ingested %d/%d turns for session %s (platform=claude_code)",
                ingested,
                total,
                session_id,
            )
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        logger.error("HTTP %d from memory bridge: %s", e.code, body[:400])
        error_msg = f"HTTP {e.code}: {body[:200]}"
    except Exception as e:
        logger.error("Failed to POST to memory bridge: %s", e)
        error_msg = str(e)

    # Server unavailable — write to local fallback for later ingestion
    if project_path:
        try:
            _write_fallback(project_path, project_id, session_id, turns, status, error_msg)
        except Exception as fe:
            logger.error("Fallback write also failed: %s", fe)
    return False


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Claude Code → galdr memory adapter")
    parser.add_argument("--session-id", default=None, help="Specific session UUID to ingest")
    parser.add_argument(
        "--project-path",
        default=None,
        help="Absolute path to the project (default: CWD or CLAUDE_PROJECT_DIR env var)",
    )
    parser.add_argument(
        "--status",
        default="completed",
        choices=["completed", "partial", "active"],
        help="Session status to record",
    )
    parser.add_argument(
        "--mcp-url",
        default=_get_configured_mcp_url(),
        help="galdr MCP server base URL (default from ~/.galdr/user_config.json or localhost:8082)",
    )
    args = parser.parse_args()

    # Resolve project path
    project_path_str = (
        args.project_path
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or os.getcwd()
    )
    project_path = Path(project_path_str).resolve()

    # Resolve session ID
    session_id = args.session_id or os.environ.get("CLAUDE_SESSION_ID")

    logger.info("Project path : %s", project_path)
    logger.info("Session ID   : %s", session_id or "(latest)")

    # Load identity
    user_config = load_user_config()  # noqa: F841 (ensures config file created)
    project_id = load_project_id(project_path)
    logger.info("Project ID   : %s", project_id)

    # Find Claude project directory
    claude_proj_dir = find_claude_project_dir(project_path)
    if not claude_proj_dir:
        logger.error("Cannot locate Claude Code project dir for %s", project_path)
        return 1

    logger.info("Claude dir   : %s", claude_proj_dir)

    # Find JSONL file
    jsonl_file = find_jsonl_file(claude_proj_dir, session_id)
    if not jsonl_file:
        logger.error("No JSONL session file found in %s", claude_proj_dir)
        return 1

    # Use filename stem as session_id if not provided
    if not session_id:
        session_id = jsonl_file.stem
    logger.info("JSONL file   : %s", jsonl_file.name)

    # Parse turns
    turns = extract_turns_from_jsonl(jsonl_file)
    logger.info("Extracted %d turns from %s", len(turns), jsonl_file.name)

    if not turns:
        logger.warning("No turns found — nothing to ingest")
        return 0

    # POST to memory bridge
    success = post_to_memory_ingest(
        project_id=project_id,
        session_id=session_id,
        turns=turns,
        status=args.status,
        mcp_url=args.mcp_url,
        project_path=project_path,
    )
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
