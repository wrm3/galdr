"""
Claude vision analysis for video frames.

Uses Anthropic Claude to analyze extracted video frames.
"""
import asyncio
import base64
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


async def analyze_frames(
    frame_paths: List[str],
    video_context: str = "",
    anthropic_api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 2000
) -> Dict[str, Any]:
    """
    Analyze video frames using Claude vision.
    
    Args:
        frame_paths: List of paths to frame images
        video_context: Context about the video (title, description, etc.)
        anthropic_api_key: Anthropic API key
        model: Claude model to use
        max_tokens: Max response tokens
        
    Returns:
        dict with success and analysis results
    """
    if not anthropic_api_key:
        return {
            'success': False,
            'error': 'Anthropic API key not configured',
            'frame_count': len(frame_paths)
        }
    
    if not frame_paths:
        return {
            'success': False,
            'error': 'No frames provided',
            'frame_count': 0
        }
    
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        
        # Prepare image content
        content = []
        
        # Add context
        context_text = f"""Analyze these frames extracted from a YouTube video.

Video context: {video_context if video_context else 'No context provided'}

Please analyze the visual content and provide:
1. A summary of what the video appears to be about
2. Key visual elements (slides, code, diagrams, people, etc.)
3. Any text visible in the frames
4. Key topics or concepts being presented
5. The apparent type of content (tutorial, presentation, demo, interview, etc.)

Provide a structured analysis suitable for content indexing."""

        content.append({
            "type": "text",
            "text": context_text
        })
        
        # Add images (limit to prevent token overflow)
        max_images = min(len(frame_paths), 8)  # Claude limit considerations
        
        for frame_path in frame_paths[:max_images]:
            try:
                image_data = await _load_image_as_base64(frame_path)
                if image_data:
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    })
            except Exception as e:
                logger.warning(f"Failed to load frame {frame_path}: {e}")
        
        if len(content) == 1:  # Only text, no images loaded
            return {
                'success': False,
                'error': 'Failed to load any frame images',
                'frame_count': len(frame_paths)
            }
        
        # Call Claude
        def call_claude():
            return client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": content
                }]
            )
        
        logger.info(f"Analyzing {len(content) - 1} frames with Claude vision...")
        response = await asyncio.to_thread(call_claude)
        
        # Extract response text
        analysis_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                analysis_text += block.text
        
        # Parse structured analysis
        analysis = _parse_vision_analysis(analysis_text)
        
        return {
            'success': True,
            'frames_analyzed': len(content) - 1,
            'total_frames': len(frame_paths),
            'model': model,
            'analysis': analysis,
            'raw_analysis': analysis_text,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            }
        }
        
    except ImportError:
        return {
            'success': False,
            'error': 'anthropic package not installed. Install: pip install anthropic',
            'frame_count': len(frame_paths)
        }
    except Exception as e:
        logger.exception("Vision analysis failed")
        return {
            'success': False,
            'error': str(e),
            'frame_count': len(frame_paths)
        }


async def _load_image_as_base64(path: str) -> Optional[str]:
    """Load image file and convert to base64."""
    import aiofiles
    
    file_path = Path(path)
    if not file_path.exists():
        return None
    
    async with aiofiles.open(file_path, 'rb') as f:
        data = await f.read()
    
    return base64.standard_b64encode(data).decode('utf-8')


def _parse_vision_analysis(text: str) -> Dict[str, Any]:
    """
    Parse the Claude vision analysis into structured format.
    
    Returns:
        Structured analysis dict
    """
    # Simple parsing - could be enhanced with more sophisticated extraction
    analysis = {
        'summary': '',
        'visual_elements': [],
        'visible_text': [],
        'key_topics': [],
        'content_type': '',
        'raw_text': text
    }
    
    # Try to extract sections based on numbered format
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect section headers
        lower = line.lower()
        if '1.' in line and 'summary' in lower:
            current_section = 'summary'
        elif '2.' in line and ('visual' in lower or 'element' in lower):
            current_section = 'visual_elements'
        elif '3.' in line and 'text' in lower:
            current_section = 'visible_text'
        elif '4.' in line and ('topic' in lower or 'concept' in lower):
            current_section = 'key_topics'
        elif '5.' in line and ('type' in lower or 'content' in lower):
            current_section = 'content_type'
        elif current_section:
            # Add content to current section
            # Remove bullet points and list markers
            clean_line = line.lstrip('•-* ')
            if clean_line:
                if current_section in ['summary', 'content_type']:
                    if analysis[current_section]:
                        analysis[current_section] += ' ' + clean_line
                    else:
                        analysis[current_section] = clean_line
                else:
                    analysis[current_section].append(clean_line)
    
    return analysis


async def analyze_single_frame(
    frame_path: str,
    prompt: str,
    anthropic_api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-6"
) -> Dict[str, Any]:
    """
    Analyze a single frame with a custom prompt.
    
    Args:
        frame_path: Path to frame image
        prompt: Custom analysis prompt
        anthropic_api_key: API key
        model: Model to use
        
    Returns:
        dict with analysis
    """
    if not anthropic_api_key:
        return {'success': False, 'error': 'No API key'}
    
    try:
        import anthropic
        
        image_data = await _load_image_as_base64(frame_path)
        if not image_data:
            return {'success': False, 'error': 'Failed to load image'}
        
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        
        def call():
            return client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }]
            )
        
        response = await asyncio.to_thread(call)
        
        return {
            'success': True,
            'analysis': response.content[0].text if response.content else '',
            'model': model
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}
