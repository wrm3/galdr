"""
Video Check New Tool Plugin

Checks a playlist for new videos since the last check.
Tracks state to identify newly added videos.
"""
from typing import Optional

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_check_new"

TOOL_DESCRIPTION = (
    "Check a playlist for new videos since last check. "
    "Compares current playlist against stored state and returns only new videos. "
    "Automatically updates state after check (can be disabled). "
    "Use this for daily/scheduled monitoring of playlists."
)

TOOL_PARAMS = {
    "playlist_url": "Full YouTube playlist URL",
    "update_state": "Update stored state after check (default: True)",
    "limit": "Max new videos to return (default: 50)"
}

# ============================================================
# PLUGIN IMPLEMENTATION
# ============================================================

_config = None
_logger = None


def setup(context: dict):
    """Called once during plugin loading."""
    global _config, _logger
    _config = context.get('config', {})
    _logger = context.get('logger')


async def execute(
    playlist_url: str,
    update_state: bool = True,
    limit: int = 50
) -> dict:
    """
    Check for new videos in playlist.
    
    Returns:
        dict with new_videos list, counts, and state info
    """
    from galdr_video_analyzer.core.playlist import check_new_videos
    
    state_file = _config.get('state_file')
    
    return await check_new_videos(
        playlist_url=playlist_url,
        update_state=update_state,
        limit=limit,
        state_file=state_file
    )
