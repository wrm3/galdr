"""
Full video analysis pipeline orchestration.

Combines metadata, transcript, frames, and vision analysis.
"""
import asyncio
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

import aiofiles

logger = logging.getLogger(__name__)


async def analyze_video(
    video_id: Optional[str] = None,
    video_url: Optional[str] = None,
    extract_frames: bool = True,
    frame_interval: int = 30,
    max_frames: int = 10,
    cache_results: bool = True,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Full video analysis pipeline.
    
    Steps:
    1. Resolve video_id from URL if needed
    2. Check cache (if enabled)
    3. Extract metadata
    4. Extract transcript
    5. Extract frames (if enabled)
    6. Run vision analysis on frames (if enabled)
    7. Compile and return results
    8. Cache results (if enabled)
    
    Args:
        video_id: YouTube video ID
        video_url: Full video URL (alternative)
        extract_frames: Whether to extract and analyze frames
        frame_interval: Seconds between frame captures
        max_frames: Maximum frames to extract
        cache_results: Cache results for future use
        config: Configuration dictionary
        
    Returns:
        Comprehensive analysis dict
    """
    from .metadata import extract_metadata
    from .transcript import extract_transcript
    from .frames import extract_frames as do_extract_frames
    from .vision import analyze_frames
    
    config = config or {}
    cache_dir = config.get('cache_dir', Path('./cache'))
    frames_dir = config.get('frames_dir', Path('./frames'))
    anthropic_key = config.get('anthropic_api_key')
    
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
    
    # Check cache
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{video_id}_analysis.json"
    
    if cache_results and cache_file.exists():
        try:
            async with aiofiles.open(cache_file, 'r', encoding='utf-8') as f:
                cached = json.loads(await f.read())
            cached['from_cache'] = True
            logger.info(f"Returning cached analysis for {video_id}")
            return cached
        except Exception as e:
            logger.warning(f"Failed to load cache for {video_id}: {e}")
    
    # Initialize result
    result = {
        'success': False,
        'video_id': video_id,
        'video_url': f"https://www.youtube.com/watch?v={video_id}",
        'analyzed_at': datetime.utcnow().isoformat() + 'Z',
        'from_cache': False,
        'components': {
            'metadata': False,
            'transcript': False,
            'frames': False,
            'vision': False
        }
    }
    
    try:
        # Step 1: Metadata
        logger.info(f"[{video_id}] Extracting metadata...")
        metadata_result = await extract_metadata(video_id)
        
        if metadata_result['success']:
            result['metadata'] = metadata_result['metadata']
            result['components']['metadata'] = True
            logger.info(f"[{video_id}] Metadata: {result['metadata'].get('title', 'No title')[:50]}...")
        else:
            result['metadata_error'] = metadata_result.get('error')
            logger.warning(f"[{video_id}] Metadata extraction failed: {metadata_result.get('error')}")
        
        # Step 2: Transcript
        logger.info(f"[{video_id}] Extracting transcript...")
        transcript_result = await extract_transcript(video_id)
        
        if transcript_result['success']:
            result['transcript'] = transcript_result['transcript']
            result['transcript_segments'] = transcript_result.get('segments', [])
            result['transcript_stats'] = {
                'word_count': transcript_result.get('word_count', 0),
                'segment_count': transcript_result.get('segment_count', 0),
                'source': transcript_result.get('source', 'unknown'),
                'language': transcript_result.get('language', 'unknown')
            }
            result['components']['transcript'] = True
            logger.info(f"[{video_id}] Transcript: {result['transcript_stats']['word_count']} words")
        else:
            result['transcript_error'] = transcript_result.get('error')
            logger.warning(f"[{video_id}] Transcript extraction failed: {transcript_result.get('error')}")
        
        # Step 3 & 4: Frames + Vision (if enabled)
        if extract_frames:
            logger.info(f"[{video_id}] Extracting frames (interval={frame_interval}s, max={max_frames})...")
            frames_result = await do_extract_frames(
                video_id=video_id,
                interval=frame_interval,
                max_frames=max_frames,
                output_dir=frames_dir
            )
            
            if frames_result['success']:
                result['frames'] = frames_result['frames']
                result['frame_count'] = frames_result['frame_count']
                result['components']['frames'] = True
                logger.info(f"[{video_id}] Extracted {result['frame_count']} frames")
                
                # Vision analysis (only if we have API key)
                if anthropic_key and frames_result['frames']:
                    logger.info(f"[{video_id}] Running vision analysis...")
                    
                    # Get video context from metadata
                    video_context = ""
                    if result.get('metadata'):
                        video_context = f"Title: {result['metadata'].get('title', '')}\n"
                        video_context += f"Channel: {result['metadata'].get('channel', '')}\n"
                        video_context += f"Description: {result['metadata'].get('description', '')[:500]}"
                    
                    vision_result = await analyze_frames(
                        frame_paths=frames_result['frames'],
                        video_context=video_context,
                        anthropic_api_key=anthropic_key
                    )
                    
                    if vision_result['success']:
                        result['vision_analysis'] = vision_result['analysis']
                        result['vision_usage'] = vision_result.get('usage', {})
                        result['components']['vision'] = True
                        logger.info(f"[{video_id}] Vision analysis complete")
                    else:
                        result['vision_error'] = vision_result.get('error')
                        logger.warning(f"[{video_id}] Vision analysis failed: {vision_result.get('error')}")
                else:
                    if not anthropic_key:
                        result['vision_error'] = 'Anthropic API key not configured'
            else:
                result['frames_error'] = frames_result.get('error')
                logger.warning(f"[{video_id}] Frame extraction failed: {frames_result.get('error')}")
        
        # Mark success if we got at least metadata or transcript
        result['success'] = result['components']['metadata'] or result['components']['transcript']
        
        # Cache results
        if cache_results and result['success']:
            try:
                async with aiofiles.open(cache_file, 'w', encoding='utf-8') as f:
                    # Make a copy without non-serializable items
                    cache_data = result.copy()
                    await f.write(json.dumps(cache_data, indent=2, default=str))
                logger.info(f"[{video_id}] Cached analysis to {cache_file}")
            except Exception as e:
                logger.warning(f"[{video_id}] Failed to cache: {e}")
        
        return result
        
    except Exception as e:
        logger.exception(f"[{video_id}] Analysis failed")
        result['error'] = str(e)
        return result


async def batch_analyze(
    video_ids: list,
    config: Optional[Dict[str, Any]] = None,
    concurrency: int = 3,
    **kwargs
) -> Dict[str, Any]:
    """
    Analyze multiple videos with controlled concurrency.
    
    Args:
        video_ids: List of video IDs to analyze
        config: Configuration dictionary
        concurrency: Max concurrent analyses
        **kwargs: Passed to analyze_video
        
    Returns:
        Dict with results for each video
    """
    import asyncio
    
    semaphore = asyncio.Semaphore(concurrency)
    
    async def analyze_with_limit(video_id: str):
        async with semaphore:
            return await analyze_video(video_id=video_id, config=config, **kwargs)
    
    # Run all analyses
    tasks = [analyze_with_limit(vid) for vid in video_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Compile results
    output = {
        'success': True,
        'total': len(video_ids),
        'successful': 0,
        'failed': 0,
        'results': {}
    }
    
    for video_id, result in zip(video_ids, results):
        if isinstance(result, Exception):
            output['results'][video_id] = {
                'success': False,
                'error': str(result)
            }
            output['failed'] += 1
        else:
            output['results'][video_id] = result
            if result.get('success'):
                output['successful'] += 1
            else:
                output['failed'] += 1
    
    return output
