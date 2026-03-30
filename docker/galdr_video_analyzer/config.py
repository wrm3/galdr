"""
Configuration management for galdr_video_analyzer.

Loads configuration from environment variables with sensible defaults.
"""
import os
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Environment Variables:
        ANTHROPIC_API_KEY: Required for vision analysis
        OPENAI_API_KEY: Optional, for embeddings if needed
        VIDEO_CACHE_DIR: Directory for cached video data (default: ./cache)
        VIDEO_FRAMES_DIR: Directory for extracted frames (default: ./frames)
        VIDEO_STATE_FILE: State file path (default: ./state.json)
        FRAME_INTERVAL: Seconds between frame captures (default: 30)
        MAX_FRAMES: Maximum frames per video (default: 10)
        
    Returns:
        Configuration dictionary
    """
    # Get project root (parent of this file's directory)
    project_root = Path(__file__).parent.parent.resolve()
    
    return {
        # API Keys
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        
        # Directories (relative to project root)
        'cache_dir': Path(os.getenv('VIDEO_CACHE_DIR', str(project_root / 'cache'))),
        'frames_dir': Path(os.getenv('VIDEO_FRAMES_DIR', str(project_root / 'frames'))),
        'state_file': Path(os.getenv('VIDEO_STATE_FILE', str(project_root / 'state.json'))),
        
        # Frame extraction settings
        'default_frame_interval': int(os.getenv('FRAME_INTERVAL', '30')),
        'max_frames': int(os.getenv('MAX_FRAMES', '10')),
        
        # Processing settings
        'default_playlist_limit': int(os.getenv('PLAYLIST_LIMIT', '50')),
        
        # Project root for reference
        'project_root': project_root,
    }


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate configuration and return validation results.
    
    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []
    
    # Check required API keys
    if not config.get('anthropic_api_key'):
        warnings.append("ANTHROPIC_API_KEY not set - vision analysis will be disabled")
    
    # Check directories exist or can be created
    for dir_key in ['cache_dir', 'frames_dir']:
        dir_path = config.get(dir_key)
        if dir_path:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create {dir_key}: {e}")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }
