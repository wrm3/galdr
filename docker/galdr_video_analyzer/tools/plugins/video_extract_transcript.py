"""
Video Extract Transcript Tool Plugin

Extracts transcript/captions from a YouTube video.
"""
from typing import Optional, List

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "video_extract_transcript"

TOOL_DESCRIPTION = (
    "Extract transcript/captions from a YouTube video. "
    "Returns full text and timestamped segments. "
    "Supports manual captions and auto-generated subtitles. "
    "Prefers English but can specify other languages."
)

TOOL_PARAMS = {
    "video_id": "YouTube video ID",
    "video_url": "Full YouTube video URL (alternative)",
    "languages": "Preferred languages as comma-separated list (default: 'en,en-US,en-GB')",
    "include_auto": "Include auto-generated captions (default: True)"
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
    languages: Optional[str] = None,
    include_auto: bool = True
) -> dict:
    """
    Extract video transcript.
    
    Returns:
        dict with transcript text and segments
    """
    from galdr_video_analyzer.core.transcript import extract_transcript
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
    
    # Parse languages
    lang_list = None
    if languages:
        lang_list = [l.strip() for l in languages.split(',')]
    
    return await extract_transcript(
        video_id=video_id,
        video_url=video_url,
        languages=lang_list,
        include_auto=include_auto
    )
