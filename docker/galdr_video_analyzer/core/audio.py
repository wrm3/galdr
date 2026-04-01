"""
Audio extraction and speech-to-text transcription using yt-dlp + faster-whisper.

Fallback path for videos without YouTube captions (e.g., freshly uploaded).
Downloads audio only (no video), runs Whisper STT locally in the container.
"""
import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

_whisper_model = None
_whisper_lock = asyncio.Lock()


async def _get_whisper_model(model_size: str = "base"):
    """Lazy-load the Whisper model (singleton, thread-safe)."""
    global _whisper_model
    async with _whisper_lock:
        if _whisper_model is None:
            from faster_whisper import WhisperModel
            logger.info(f"Loading faster-whisper model: {model_size}")
            _whisper_model = await asyncio.to_thread(
                WhisperModel, model_size, device="cpu", compute_type="int8"
            )
            logger.info("Whisper model loaded")
    return _whisper_model


async def extract_audio(
    video_id: str,
    video_url: Optional[str] = None,
    output_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Download audio-only from a YouTube video using yt-dlp.

    Returns path to the extracted audio file (.wav).
    """
    import yt_dlp

    url = video_url or f"https://www.youtube.com/watch?v={video_id}"
    output_dir = output_dir or Path(tempfile.mkdtemp())
    audio_path = output_dir / f"{video_id}.wav"

    if audio_path.exists():
        return {"success": True, "audio_path": str(audio_path), "from_cache": True}

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / f"{video_id}.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",
            }
        ],
    }

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=True)

        info = await asyncio.to_thread(download)

        if not audio_path.exists():
            candidates = list(output_dir.glob(f"{video_id}.*"))
            wav_files = [f for f in candidates if f.suffix == ".wav"]
            if wav_files:
                audio_path = wav_files[0]
            else:
                return {
                    "success": False,
                    "error": f"Audio extraction failed — no .wav found. Files: {[f.name for f in candidates]}",
                    "video_id": video_id,
                }

        duration = info.get("duration", 0)
        return {
            "success": True,
            "video_id": video_id,
            "audio_path": str(audio_path),
            "duration": duration,
            "from_cache": False,
        }

    except Exception as e:
        logger.exception(f"Failed to extract audio for {video_id}")
        return {"success": False, "error": str(e), "video_id": video_id}


async def transcribe_audio(
    audio_path: str,
    video_id: str = "",
    model_size: str = "base",
    language: Optional[str] = "en",
) -> Dict[str, Any]:
    """
    Run faster-whisper STT on an audio file.

    Args:
        audio_path: Path to .wav file
        video_id: For logging/metadata
        model_size: Whisper model size (tiny, base, small, medium, large-v3)
        language: Force language (None = auto-detect)

    Returns:
        dict with transcript text and timestamped segments
    """
    try:
        model = await _get_whisper_model(model_size)

        def run_transcription():
            segments_iter, info = model.transcribe(
                audio_path,
                language=language,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
            )
            segments = []
            full_text_parts = []
            for seg in segments_iter:
                segments.append({
                    "start": f"{int(seg.start // 3600):02d}:{int(seg.start % 3600 // 60):02d}:{seg.start % 60:06.3f}",
                    "end": f"{int(seg.end // 3600):02d}:{int(seg.end % 3600 // 60):02d}:{seg.end % 60:06.3f}",
                    "start_seconds": round(seg.start, 3),
                    "end_seconds": round(seg.end, 3),
                    "text": seg.text.strip(),
                })
                full_text_parts.append(seg.text.strip())
            return segments, " ".join(full_text_parts), info

        logger.info(f"[{video_id}] Running Whisper transcription ({model_size})...")
        segments, full_text, info = await asyncio.to_thread(run_transcription)
        logger.info(f"[{video_id}] Whisper done: {len(segments)} segments, {len(full_text.split())} words")

        return {
            "success": True,
            "video_id": video_id,
            "transcript": full_text,
            "segments": segments,
            "segment_count": len(segments),
            "character_count": len(full_text),
            "word_count": len(full_text.split()),
            "source": "whisper",
            "language": info.language if hasattr(info, "language") else language,
            "language_probability": round(info.language_probability, 3) if hasattr(info, "language_probability") else None,
            "whisper_model": model_size,
        }

    except Exception as e:
        logger.exception(f"[{video_id}] Whisper transcription failed")
        return {"success": False, "error": str(e), "video_id": video_id}


async def extract_and_transcribe(
    video_id: str,
    video_url: Optional[str] = None,
    model_size: str = "base",
    language: Optional[str] = "en",
    cleanup: bool = True,
) -> Dict[str, Any]:
    """
    Full audio pipeline: download audio -> Whisper STT -> return transcript.

    This is the single-call convenience function for the backlog processor.
    """
    audio_dir = Path(tempfile.mkdtemp())
    try:
        audio_result = await extract_audio(video_id, video_url, audio_dir)
        if not audio_result["success"]:
            return audio_result

        transcript_result = await transcribe_audio(
            audio_path=audio_result["audio_path"],
            video_id=video_id,
            model_size=model_size,
            language=language,
        )
        transcript_result["audio_duration"] = audio_result.get("duration", 0)
        return transcript_result

    finally:
        if cleanup:
            import shutil
            try:
                shutil.rmtree(audio_dir, ignore_errors=True)
            except Exception:
                pass
