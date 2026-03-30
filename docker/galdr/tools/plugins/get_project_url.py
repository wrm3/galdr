"""
get_project_url — Return the web UI URL for a project or user.

Saves tokens by letting agents return a URL instead of streaming
all task/session data through the conversation.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

TOOL_NAME = "get_project_url"
TOOL_DESCRIPTION = (
    "Get the web UI URL for a project's task dashboard or a user's session history. "
    "Returns a clickable URL that the user can open in their browser. "
    "Use this instead of streaming large amounts of task/session data through the conversation."
)
TOOL_PARAMS = {
    "project_id": "Project UUID to get task dashboard URL (optional)",
    "user_id":    "User ID to get session history URL (optional)",
    "page":       "Which page: 'tasks' | 'status' | 'sessions' | 'memory' (default: 'tasks')",
}

_config = None


def setup(context: dict):
    global _config
    _config = context.get("config", {})


def execute(
    project_id: Optional[str] = None,
    user_id: Optional[str] = None,
    page: str = "tasks",
) -> dict:
    base_url = (_config or {}).get("GALDR_url", "")
    if not base_url:
        base_url = os.environ.get("GALDR_URL", "http://localhost:8082")

    urls: dict[str, str] = {}

    if project_id:
        urls["tasks"] = f"{base_url}/projects/{project_id}/tasks"
        urls["status"] = f"{base_url}/projects/{project_id}/status"
        urls["visualizer"] = f"{base_url}/admin/galdr"

    if user_id:
        urls["sessions"] = f"{base_url}/users/{user_id}/sessions"
        urls["memory"] = f"{base_url}/users/{user_id}/memory"

    if not urls:
        return {
            "success": False,
            "error": "Provide at least one of project_id or user_id",
        }

    primary_url = urls.get(page, list(urls.values())[0])

    return {
        "success": True,
        "url": primary_url,
        "all_urls": urls,
        "base_url": base_url,
    }
