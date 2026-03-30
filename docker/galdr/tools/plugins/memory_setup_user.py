"""
memory_setup_user — MCP tool (stateless)

Returns user identity instructions or validates a user_id against the DB.
Does NOT write to the filesystem — user identity is stored host-side in:
  - %APPDATA%/galdr/user_config.json (Windows) or ~/.config/galdr/user_config.json (Linux/Mac)
  - .galdr/.user_id (per-project, read by agents and passed as params to memory tools)

The session-start hook and agents handle file creation on the host.
This tool only provides guidance (setup) or DB lookups (whoami).
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "memory_setup_user"
TOOL_DESCRIPTION = (
    "Create or update ~/.galdr/user_config.json for memory identity tracking. "
    "Generates a stable machine_id (random UUID, stored in ~/.galdr/machine_id) "
    "that works across Windows, macOS, Linux, and shared Docker containers. "
    "Also provides memory_whoami() to read the current user config. "
    "Call this once per machine when setting up galdr. "
    "Teammates each call it on their own machine with their own user_id."
)
TOOL_PARAMS = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "description": "Action to perform: 'setup' (returns host-side instructions) or 'whoami' (validates user_id against DB).",
            "enum": ["setup", "whoami"],
            "default": "whoami",
        },
        "user_id": {
            "type": "string",
            "description": (
                "The user_id read from .galdr/.user_id on the host. "
                "Required for action='whoami' to look up session history."
            ),
        },
        "machine_id": {
            "type": "string",
            "description": "Machine UUID from the host-side user_config.json. Optional.",
        },
    },
    "required": ["action"],
}

_db = None


def setup(context: dict):
    global _db
    _db = context.get("db")


async def execute(
    action: str = "whoami",
    user_id: Optional[str] = None,
    machine_id: Optional[str] = None,
) -> dict[str, Any]:

    if action == "whoami":
        if not user_id:
            return {
                "configured": False,
                "message": (
                    "No user_id provided. The agent should read .galdr/.user_id "
                    "from the project directory and pass it as a parameter. "
                    "If that file doesn't exist, check %APPDATA%/galdr/user_config.json (Windows) "
                    "or ~/.config/galdr/user_config.json (Linux/Mac). "
                    "If neither exists, run action='setup' for instructions."
                ),
            }

        result: dict[str, Any] = {
            "configured": True,
            "user_id": user_id,
            "machine_id": machine_id or "(not provided)",
        }

        if _db:
            try:
                with _db.get_cursor() as cur:
                    cur.execute(
                        "SELECT COUNT(*) AS cnt FROM agent_sessions WHERE user_id = %s",
                        (user_id,),
                    )
                    row = cur.fetchone()
                    result["session_count"] = row["cnt"] if row else 0
            except Exception as e:
                logger.warning(f"DB lookup failed for user_id={user_id}: {e}")
                result["session_count"] = "(db unavailable)"

        return result

    if action == "setup":
        return {
            "success": True,
            "message": "User identity is stored on the HOST machine, not in Docker.",
            "instructions": [
                "1. The session-start hook auto-creates the identity files on first run.",
                "2. Canonical config: %APPDATA%/galdr/user_config.json (Win) or ~/.config/galdr/user_config.json (Linux/Mac).",
                "3. Per-project shortcut: .galdr/.user_id (contains just the user_id string).",
                "4. Agents read .galdr/.user_id and pass it as a parameter to memory_ingest_session, memory_capture_session, etc.",
                "5. To set up manually: create .galdr/.user_id with your user_id (e.g. 'usr_alice').",
            ],
            "host_paths": {
                "windows": "%APPDATA%\\galdr\\user_config.json",
                "linux_mac": "~/.config/galdr/user_config.json",
                "per_project": ".galdr/.user_id",
            },
            "config_format": {
                "user_id": "usr_yourname",
                "display_name": "Your Name",
                "machine_id": "(auto-generated UUID)",
                "platform": "(auto-detected)",
                "created_at": "(ISO timestamp)",
            },
        }

    return {"success": False, "error": f"Unknown action '{action}'. Use 'setup' or 'whoami'."}
