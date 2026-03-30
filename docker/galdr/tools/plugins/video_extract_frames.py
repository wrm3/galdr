"""
Video Extract Frames Tool Plugin

Extracts key frames from a YouTube video for vision analysis.
"""
from typing import Optional

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_extract_frames"

TOOL_DESCRIPTION = (
    "Extract key frames from a YouTube video. "
    "Downloads video and captures frames at regular intervals. "
    "Frames are saved to disk and can be used for vision analysis. "
    "Results are cached - subsequent calls return cached frames."
)

TOOL_PARAMS = {
    "video_id": "YouTube video ID",
    "video_url": "Full YouTube video URL (alternative)",
    "interval": "Seconds between frame captures (default: 30)",
    "max_frames": "Maximum frames to extract (default: 10)"
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
    video_url: Optional[str] = None,
    interval: Optional[int] = None,
    max_frames: Optional[int] = None
) -> dict:
    """
    Extract frames from video.
    
    Returns:
        dict with frame paths
    """
    from galdr_video_analyzer.core.frames import extract_frames
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
    
    # Use config defaults
    interval = interval or _config.get('default_frame_interval', 30)
    max_frames = max_frames or _config.get('max_frames', 10)
    output_dir = _config.get('frames_dir')
    
    return await extract_frames(
        video_id=video_id,
        video_url=video_url,
        interval=interval,
        max_frames=max_frames,
        output_dir=output_dir
    )
