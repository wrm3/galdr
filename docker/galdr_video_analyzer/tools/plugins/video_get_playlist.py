"""
Video Get Playlist Tool Plugin

Fetches video list from a YouTube playlist using yt-dlp.
"""
from typing import Optional

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_get_playlist"

TOOL_DESCRIPTION = (
    "Get list of video IDs and metadata from a YouTube playlist. "
    "Returns videos sorted by playlist order (typically newest first). "
    "Use this to discover which videos are in a playlist before processing."
)

TOOL_PARAMS = {
    "playlist_url": "Full YouTube playlist URL (e.g., https://www.youtube.com/playlist?list=PLxxx)",
    "limit": "Maximum videos to return, 0 for all (default: 50)",
    "include_metadata": "Include title, duration, upload_date (default: True)"
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
    limit: int = 50,
    include_metadata: bool = True
) -> dict:
    """
    Fetch videos from YouTube playlist.
    
    Returns:
        dict with success, videos list, total_count
    """
    from galdr_video_analyzer.core.playlist import get_playlist_videos
    
    return await get_playlist_videos(
        playlist_url=playlist_url,
        limit=limit,
        include_metadata=include_metadata
    )
