"""
Video Extract Metadata Tool Plugin

Extracts metadata from a YouTube video (title, description, channel, etc.).
"""
from typing import Optional

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_extract_metadata"

TOOL_DESCRIPTION = (
    "Extract metadata from a YouTube video. "
    "Returns title, description, channel, duration, view count, upload date, tags, etc. "
    "Fast operation - does not download the video."
)

TOOL_PARAMS = {
    "video_id": "YouTube video ID (e.g., 'dQw4w9WgXcQ')",
    "video_url": "Full YouTube video URL (alternative to video_id)"
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
    video_id: Optional[str] = None,
    video_url: Optional[str] = None
) -> dict:
    """
    Extract video metadata.
    
    Returns:
        dict with success and metadata fields
    """
    from galdr_video_analyzer.core.metadata import extract_metadata
    import re
    
    # Resolve video_id from URL if needed
    if not video_id and video_url:
        match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', video_url)
        if match:
            video_id = match.group(1)
    
    if not video_id:
        return {
            'success': False,
            'error': 'video_id or video_url required'
        }
    
    return await extract_metadata(video_id=video_id, video_url=video_url)
