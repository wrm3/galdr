"""
Video metadata extraction using yt-dlp.

Extracts title, description, duration, channel, upload date, tags, etc.
"""
import asyncio
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


async def extract_metadata(
    video_id: str,
    video_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract metadata from a YouTube video.
    
    Args:
        video_id: YouTube video ID
        video_url: Full video URL (optional, constructed from ID if not provided)
        
    Returns:
        dict with success and metadata fields
    """
    import yt_dlp
    
    url = video_url or f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': False,
        }
        
        def extract():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        
        info = await asyncio.to_thread(extract)
        
        if not info:
            return {
                'success': False,
                'error': 'Failed to extract video info',
                'video_id': video_id
            }
        
        # Extract relevant metadata
        metadata = {
            'video_id': video_id,
            'title': info.get('title'),
            'description': info.get('description'),
            'channel': info.get('channel') or info.get('uploader'),
            'channel_id': info.get('channel_id') or info.get('uploader_id'),
            'channel_url': info.get('channel_url') or info.get('uploader_url'),
            'upload_date': info.get('upload_date'),  # YYYYMMDD format
            'duration': info.get('duration'),  # seconds
            'duration_string': info.get('duration_string'),  # HH:MM:SS
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'comment_count': info.get('comment_count'),
            'tags': info.get('tags', []),
            'categories': info.get('categories', []),
            'thumbnail': info.get('thumbnail'),
            'webpage_url': info.get('webpage_url'),
            'is_live': info.get('is_live', False),
            'was_live': info.get('was_live', False),
            'language': info.get('language'),
        }
        
        # Format upload date if present
        if metadata['upload_date'] and len(metadata['upload_date']) == 8:
            date_str = metadata['upload_date']
            metadata['upload_date_formatted'] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        
        return {
            'success': True,
            'video_id': video_id,
            'metadata': metadata
        }
        
    except Exception as e:
        logger.exception(f"Failed to extract metadata for {video_id}")
        return {
            'success': False,
            'error': str(e),
            'video_id': video_id
        }
