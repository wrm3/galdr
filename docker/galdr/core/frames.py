"""
Video frame extraction using yt-dlp and OpenCV.

Downloads video and extracts key frames at specified intervals.
"""
import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


async def extract_frames(
    video_id: str,
    video_url: Optional[str] = None,
    interval: int = 30,
    max_frames: int = 10,
    output_dir: Optional[Path] = None,
    quality: str = 'worst'  # Use lowest quality for faster download
) -> Dict[str, Any]:
    """
    Extract frames from a YouTube video at regular intervals.
    
    Args:
        video_id: YouTube video ID
        video_url: Full video URL (optional)
        interval: Seconds between frame captures
        max_frames: Maximum frames to extract
        output_dir: Directory to save frames
        quality: Video quality for download ('worst' recommended for speed)
        
    Returns:
        dict with success and list of frame paths
    """
    import yt_dlp
    
    url = video_url or f"https://www.youtube.com/watch?v={video_id}"
    output_dir = output_dir or Path('./frames')
    
    # Create video-specific output directory
    video_frames_dir = output_dir / video_id
    video_frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if frames already exist
    existing_frames = list(video_frames_dir.glob("frame_*.jpg"))
    if existing_frames:
        logger.info(f"Found {len(existing_frames)} existing frames for {video_id}")
        return {
            'success': True,
            'video_id': video_id,
            'frames': [str(f) for f in sorted(existing_frames)],
            'frame_count': len(existing_frames),
            'from_cache': True
        }
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            video_file = temp_path / f"{video_id}.mp4"
            
            # Download video
            logger.info(f"Downloading video {video_id} for frame extraction...")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': f'{quality}[ext=mp4]/{quality}',
                'outtmpl': str(video_file),
            }
            
            def download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    return info
            
            info = await asyncio.to_thread(download)
            
            if not video_file.exists():
                # Try to find the actual downloaded file
                downloaded = list(temp_path.glob(f"{video_id}.*"))
                if downloaded:
                    video_file = downloaded[0]
                else:
                    return {
                        'success': False,
                        'error': 'Video download failed - file not found',
                        'video_id': video_id
                    }
            
            duration = info.get('duration', 0)
            
            # Extract frames using OpenCV
            frames = await _extract_frames_opencv(
                video_path=video_file,
                video_id=video_id,
                output_dir=video_frames_dir,
                interval=interval,
                max_frames=max_frames,
                duration=duration
            )
            
            return {
                'success': True,
                'video_id': video_id,
                'frames': frames,
                'frame_count': len(frames),
                'interval_seconds': interval,
                'video_duration': duration,
                'from_cache': False
            }
            
    except Exception as e:
        logger.exception(f"Failed to extract frames for {video_id}")
        return {
            'success': False,
            'error': str(e),
            'video_id': video_id
        }


async def _extract_frames_opencv(
    video_path: Path,
    video_id: str,
    output_dir: Path,
    interval: int,
    max_frames: int,
    duration: int
) -> List[str]:
    """
    Extract frames from video file using OpenCV.
    
    Returns:
        List of frame file paths
    """
    try:
        import cv2
    except ImportError:
        logger.error("OpenCV not installed. Install with: pip install opencv-python")
        raise ImportError("opencv-python required for frame extraction")
    
    def extract():
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if fps <= 0:
            fps = 30  # Fallback
        
        # Calculate which frames to extract
        frame_interval = int(fps * interval)
        frames_to_extract = []
        
        current_frame = 0
        while current_frame < total_frames and len(frames_to_extract) < max_frames:
            frames_to_extract.append(current_frame)
            current_frame += frame_interval
        
        # Extract frames
        extracted_paths = []
        
        for frame_num in frames_to_extract:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            
            if ret:
                timestamp = int(frame_num / fps)
                frame_filename = f"frame_{timestamp:06d}s.jpg"
                frame_path = output_dir / frame_filename
                
                cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                extracted_paths.append(str(frame_path))
                logger.debug(f"Extracted frame at {timestamp}s: {frame_path}")
        
        cap.release()
        return extracted_paths
    
    return await asyncio.to_thread(extract)


async def cleanup_frames(
    video_id: str,
    frames_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Remove extracted frames for a video.
    
    Args:
        video_id: YouTube video ID
        frames_dir: Base frames directory
        
    Returns:
        dict with success and count of removed files
    """
    import shutil
    
    frames_dir = frames_dir or Path('./frames')
    video_frames_dir = frames_dir / video_id
    
    if not video_frames_dir.exists():
        return {
            'success': True,
            'video_id': video_id,
            'removed': 0,
            'message': 'No frames directory found'
        }
    
    try:
        files = list(video_frames_dir.glob("*"))
        count = len(files)
        
        def remove():
            shutil.rmtree(video_frames_dir)
        
        await asyncio.to_thread(remove)
        
        return {
            'success': True,
            'video_id': video_id,
            'removed': count,
            'message': f'Removed {count} files'
        }
        
    except Exception as e:
        logger.exception(f"Failed to cleanup frames for {video_id}")
        return {
            'success': False,
            'error': str(e),
            'video_id': video_id
        }
