"""
Video Batch Process Tool Plugin

Process multiple videos efficiently with controlled concurrency.
"""
from typing import Optional, List

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_batch_process"

TOOL_DESCRIPTION = (
    "Process multiple videos efficiently with controlled concurrency. "
    "Takes a list of video IDs and runs full analysis on each. "
    "Respects rate limits and handles failures gracefully. "
    "Use this for bulk processing of playlist videos."
)

TOOL_PARAMS = {
    "video_ids": "Comma-separated list of video IDs or JSON array",
    "concurrency": "Max concurrent analyses (default: 3)",
    "extract_frames": "Extract and analyze frames (default: True)",
    "frame_interval": "Seconds between frame captures (default: 30)",
    "max_frames": "Maximum frames per video (default: 10)"
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
    video_ids: str,
    concurrency: int = 3,
    extract_frames: bool = True,
    frame_interval: Optional[int] = None,
    max_frames: Optional[int] = None
) -> dict:
    """
    Process multiple videos.
    
    Args:
        video_ids: Comma-separated IDs or JSON array
        
    Returns:
        dict with results for each video
    """
    from galdr_video_analyzer.core.analyzer import batch_analyze
    import json
    
    # Parse video_ids
    ids_list = []
    
    # Try JSON array first
    try:
        if video_ids.startswith('['):
            ids_list = json.loads(video_ids)
    except json.JSONDecodeError:
        pass
    
    # Fall back to comma-separated
    if not ids_list:
        ids_list = [vid.strip() for vid in video_ids.split(',') if vid.strip()]
    
    if not ids_list:
        return {
            'success': False,
            'error': 'No valid video IDs provided'
        }
    
    # Use config defaults
    frame_interval = frame_interval or _config.get('default_frame_interval', 30)
    max_frames = max_frames or _config.get('max_frames', 10)
    
    return await batch_analyze(
        video_ids=ids_list,
        config=_config,
        concurrency=concurrency,
        extract_frames=extract_frames,
        frame_interval=frame_interval,
        max_frames=max_frames
    )
