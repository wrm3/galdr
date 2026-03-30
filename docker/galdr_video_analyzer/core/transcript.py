"""
Video transcript/caption extraction using yt-dlp.

Extracts auto-generated or manual captions from YouTube videos.
"""
import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


async def extract_transcript(
    video_id: str,
    video_url: Optional[str] = None,
    languages: Optional[List[str]] = None,
    include_auto: bool = True
) -> Dict[str, Any]:
    """
    Extract transcript/captions from a YouTube video.
    
    Args:
        video_id: YouTube video ID
        video_url: Full video URL (optional)
        languages: Preferred languages ['en', 'en-US', etc.] (default: ['en'])
        include_auto: Include auto-generated captions (default: True)
        
    Returns:
        dict with success, transcript text, and segments
    """
    import yt_dlp
    
    url = video_url or f"https://www.youtube.com/watch?v={video_id}"
    languages = languages or ['en', 'en-US', 'en-GB']
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_template = str(temp_path / "transcript")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': include_auto,
                'subtitleslangs': languages,
                'subtitlesformat': 'json3',  # Structured format with timestamps
                'outtmpl': output_template,
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
            
            # Check for available subtitles
            subtitles = info.get('subtitles', {})
            auto_subs = info.get('automatic_captions', {})
            
            # Find best available transcript
            transcript_data = None
            source_type = None
            source_lang = None
            
            # Prefer manual subtitles
            for lang in languages:
                if lang in subtitles:
                    transcript_data = subtitles[lang]
                    source_type = 'manual'
                    source_lang = lang
                    break
            
            # Fall back to auto-generated
            if not transcript_data and include_auto:
                for lang in languages:
                    if lang in auto_subs:
                        transcript_data = auto_subs[lang]
                        source_type = 'auto'
                        source_lang = lang
                        break
            
            if not transcript_data:
                available = list(subtitles.keys()) + list(auto_subs.keys())
                return {
                    'success': False,
                    'error': f'No transcript available in {languages}. Available: {available[:10]}',
                    'video_id': video_id,
                    'available_languages': available[:20]
                }
            
            # Download the transcript
            ydl_opts_download = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'writesubtitles': source_type == 'manual',
                'writeautomaticsub': source_type == 'auto',
                'subtitleslangs': [source_lang],
                'subtitlesformat': 'vtt',
                'outtmpl': output_template,
            }
            
            def download_subs():
                with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                    ydl.download([url])
            
            await asyncio.to_thread(download_subs)
            
            # Find and parse the subtitle file
            sub_files = list(temp_path.glob("*.vtt"))
            
            if not sub_files:
                # Try alternative: extract from transcript_data directly
                return await _parse_transcript_from_info(transcript_data, video_id, source_type, source_lang)
            
            # Parse VTT file
            vtt_content = sub_files[0].read_text(encoding='utf-8')
            segments, full_text = _parse_vtt(vtt_content)
            
            return {
                'success': True,
                'video_id': video_id,
                'transcript': full_text,
                'segments': segments,
                'segment_count': len(segments),
                'character_count': len(full_text),
                'word_count': len(full_text.split()),
                'source': source_type,
                'language': source_lang
            }
            
    except Exception as e:
        logger.exception(f"Failed to extract transcript for {video_id}")
        return {
            'success': False,
            'error': str(e),
            'video_id': video_id
        }


async def _parse_transcript_from_info(
    transcript_data: List[Dict],
    video_id: str,
    source_type: str,
    source_lang: str
) -> Dict[str, Any]:
    """Parse transcript from yt-dlp info dict format."""
    try:
        # Try to get a text URL and fetch it
        for fmt in transcript_data:
            if fmt.get('ext') == 'json3':
                # Would need to fetch and parse json3 format
                pass
        
        # Fallback: just indicate transcript is available but couldn't be parsed
        return {
            'success': False,
            'error': 'Transcript available but could not be downloaded',
            'video_id': video_id,
            'source': source_type,
            'language': source_lang
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'video_id': video_id
        }


def _parse_vtt(vtt_content: str) -> tuple:
    """
    Parse VTT subtitle file into segments and full text.
    
    Returns:
        (segments_list, full_text_string)
    """
    import re
    
    lines = vtt_content.strip().split('\n')
    segments = []
    current_segment = None
    
    # VTT timestamp pattern: 00:00:00.000 --> 00:00:05.000
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')
    
    for line in lines:
        line = line.strip()
        
        # Skip WEBVTT header and empty lines
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        
        if not line:
            if current_segment and current_segment.get('text'):
                segments.append(current_segment)
            current_segment = None
            continue
        
        # Check for timestamp
        match = timestamp_pattern.match(line)
        if match:
            current_segment = {
                'start': match.group(1),
                'end': match.group(2),
                'start_seconds': _vtt_time_to_seconds(match.group(1)),
                'end_seconds': _vtt_time_to_seconds(match.group(2)),
                'text': ''
            }
        elif current_segment is not None:
            # Clean the text line
            clean_line = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
            if clean_line:
                if current_segment['text']:
                    current_segment['text'] += ' '
                current_segment['text'] += clean_line
    
    # Don't forget last segment
    if current_segment and current_segment.get('text'):
        segments.append(current_segment)
    
    # Deduplicate (VTT often has overlapping segments)
    seen_texts = set()
    unique_segments = []
    for seg in segments:
        text = seg['text'].strip()
        if text and text not in seen_texts:
            seen_texts.add(text)
            seg['text'] = text
            unique_segments.append(seg)
    
    # Build full text
    full_text = ' '.join(seg['text'] for seg in unique_segments)
    
    return unique_segments, full_text


def _vtt_time_to_seconds(time_str: str) -> float:
    """Convert VTT timestamp to seconds."""
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds
