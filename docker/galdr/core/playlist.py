"""
Core playlist operations using yt-dlp.

Provides functions for fetching playlist contents and tracking new videos.
"""
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

import aiofiles

logger = logging.getLogger(__name__)


async def get_playlist_videos(
    playlist_url: str,
    limit: int = 50,
    include_metadata: bool = True
) -> Dict[str, Any]:
    """
    Fetch videos from a YouTube playlist.
    
    Args:
        playlist_url: Full playlist URL
        limit: Max videos to return (0 = all)
        include_metadata: Include title, duration, upload_date
        
    Returns:
        dict with success, videos, total_count, playlist_title
    """
    import yt_dlp
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Don't download, just get info
            'ignoreerrors': True,  # Skip unavailable videos
        }
        
        if limit > 0:
            ydl_opts['playlist_items'] = f'1:{limit}'
        
        # Run yt-dlp in thread to avoid blocking
        def extract():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(playlist_url, download=False)
        
        info = await asyncio.to_thread(extract)
        
        if not info:
            return {
                'success': False,
                'error': 'Failed to extract playlist info',
                'videos': [],
                'total_count': 0
            }
        
        videos = []
        entries = info.get('entries', [])
        
        for entry in entries:
            if entry is None:
                continue
            
            video_id = entry.get('id')
            if not video_id:
                continue
                
            video_data = {
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
            
            if include_metadata:
                video_data.update({
                    'title': entry.get('title'),
                    'duration': entry.get('duration'),
                    'upload_date': entry.get('upload_date'),
                    'channel': entry.get('channel') or entry.get('uploader'),
                    'view_count': entry.get('view_count')
                })
            
            videos.append(video_data)
        
        return {
            'success': True,
            'playlist_title': info.get('title'),
            'playlist_id': info.get('id'),
            'playlist_url': playlist_url,
            'videos': videos,
            'total_count': len(videos),
            'has_more': len(videos) >= limit if limit > 0 else False
        }
        
    except Exception as e:
        logger.exception("Failed to get playlist videos")
        return {
            'success': False,
            'error': str(e),
            'videos': [],
            'total_count': 0
        }


async def check_new_videos(
    playlist_url: str,
    update_state: bool = True,
    limit: int = 50,
    state_file: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Check playlist for new videos since last check.
    
    State is stored as JSON:
    {
        "playlist_id": {
            "last_checked": "2025-01-04T12:00:00Z",
            "known_video_ids": ["id1", "id2", ...],
            "playlist_title": "..."
        }
    }
    
    Args:
        playlist_url: Full playlist URL
        update_state: Update stored state after check
        limit: Max new videos to return
        state_file: Path to state file
        
    Returns:
        dict with new_videos list and counts
    """
    state_file = state_file or Path('./state.json')
    
    try:
        # Get current playlist videos (get all to compare properly)
        current = await get_playlist_videos(
            playlist_url=playlist_url,
            limit=0,  # Get all to compare
            include_metadata=True
        )
        
        if not current['success']:
            return current
        
        playlist_id = current['playlist_id']
        current_ids = {v['video_id'] for v in current['videos']}
        
        # Load stored state
        known_ids = set()
        state = {}
        
        if state_file.exists():
            try:
                async with aiofiles.open(state_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    state = json.loads(content) if content.strip() else {}
                
                if playlist_id in state:
                    known_ids = set(state[playlist_id].get('known_video_ids', []))
            except json.JSONDecodeError:
                logger.warning(f"Invalid state file, starting fresh: {state_file}")
                state = {}
        
        # Find new videos (maintain playlist order for newest-first)
        new_videos = []
        for video in current['videos']:
            if video['video_id'] not in known_ids:
                new_videos.append(video)
        
        # Apply limit
        if limit > 0 and len(new_videos) > limit:
            new_videos = new_videos[:limit]
        
        # Update state if requested
        if update_state:
            state[playlist_id] = {
                'last_checked': datetime.utcnow().isoformat() + 'Z',
                'known_video_ids': list(current_ids),
                'playlist_title': current['playlist_title'],
                'total_videos': len(current_ids)
            }
            
            state_file.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(state_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(state, indent=2))
            
            logger.info(f"Updated state for playlist {playlist_id}: {len(current_ids)} videos tracked")
        
        return {
            'success': True,
            'playlist_id': playlist_id,
            'playlist_title': current['playlist_title'],
            'new_videos': new_videos,
            'new_count': len(new_videos),
            'total_in_playlist': len(current_ids),
            'previously_known': len(known_ids),
            'is_first_check': len(known_ids) == 0,
            'state_updated': update_state,
            'state_file': str(state_file)
        }
        
    except Exception as e:
        logger.exception("Failed to check for new videos")
        return {
            'success': False,
            'error': str(e),
            'new_videos': [],
            'new_count': 0
        }
