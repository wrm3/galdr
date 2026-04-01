"""
Video Analyze Tool Plugin

Full analysis pipeline: metadata + transcript + frames + vision analysis.
This is the primary tool for processing videos.
"""
from typing import Optional

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_analyze"

TOOL_DESCRIPTION = (
    "Perform full analysis on a YouTube video. "
    "Extracts metadata, transcript, key frames, and runs Claude vision analysis. "
    "Returns comprehensive analysis suitable for RAG ingestion. "
    "Results are cached for efficiency. "
    "This is the primary tool for processing new videos."
)

TOOL_PARAMS = {
    "video_id": "YouTube video ID (e.g., 'dQw4w9WgXcQ')",
    "video_url": "Full YouTube video URL (alternative to video_id)",
    "extract_frames": "Extract and analyze frames with vision (default: True)",
    "frame_interval": "Seconds between frame captures (default: 30)",
    "max_frames": "Maximum frames to extract (default: 10)",
    "cache_results": "Cache results for reuse (default: True)",
    "transcript_mode": (
        "How to get transcript: "
        "'captions' = YouTube captions only, "
        "'audio' = download audio + Whisper STT, "
        "'auto' = try captions first, fall back to audio (default)"
    ),
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
    extract_frames: bool = True,
    frame_interval: Optional[int] = None,
    max_frames: Optional[int] = None,
    cache_results: bool = True,
    transcript_mode: str = "auto",
) -> dict:
    """
    Full video analysis pipeline.
    
    Returns:
        Comprehensive analysis dict with metadata, transcript, frames, vision
    """
    from galdr_video_analyzer.core.analyzer import analyze_video
    
    cfg = _config or {}
    frame_interval = frame_interval or cfg.get('default_frame_interval', 30)
    max_frames = max_frames or cfg.get('max_frames', 10)
    
    return await analyze_video(
        video_id=video_id,
        video_url=video_url,
        extract_frames=extract_frames,
        frame_interval=frame_interval,
        max_frames=max_frames,
        cache_results=cache_results,
        config=_config,
        transcript_mode=transcript_mode,
    )
