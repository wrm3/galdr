"""
Video Analyze Tool Plugin

Full analysis pipeline: metadata + transcript + frames + vision analysis.
Persists results to vault_notes for searchability and materialization.
"""
import hashlib
import logging
import re
from datetime import datetime, timezone
from typing import Optional

TOOL_NAME = "video_analyze"

TOOL_DESCRIPTION = (
    "Perform full analysis on a YouTube video. "
    "Extracts metadata, transcript, key frames, and runs Claude vision analysis. "
    "Results are persisted to vault_notes and cached for efficiency. "
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
    "persist_to_db": "Write results to vault_notes (default: true). Set false for preview-only.",
}

_config = None
_db = None
_embedding_gen = None
_logger = logging.getLogger(__name__)


def setup(context: dict):
    """Called once during plugin loading."""
    global _config, _db, _embedding_gen
    _config = context.get('config', {})
    _db = context.get('db')
    _embedding_gen = context.get('embedding_generator')


def _embed(text: str) -> Optional[list]:
    if not _embedding_gen:
        return None
    try:
        result = _embedding_gen.generate(text[:8000])
        return result.tolist() if hasattr(result, "tolist") else list(result)
    except Exception as e:
        _logger.warning("Embedding failed: %s", e)
        return None


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _format_duration(seconds: int) -> str:
    if not seconds:
        return "unknown"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"


def _build_vault_note(result: dict, transcript_mode: str) -> tuple[str, str, str]:
    """Build frontmatter + body markdown from analysis result. Returns (vault_path, content, body)."""
    video_id = result.get("video_id", "unknown")
    meta = result.get("metadata", {})
    title = meta.get("title", f"YouTube Video {video_id}")
    channel = meta.get("channel", "Unknown")
    description = (meta.get("description") or "")[:2000]
    duration = meta.get("duration", 0)
    upload_date = meta.get("upload_date") or result.get("analyzed_at", "")[:10]
    tags = meta.get("tags", []) or meta.get("categories", []) or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    tags = tags[:20]

    transcript = result.get("transcript", "")
    transcript_stats = result.get("transcript_stats", {})
    vision = result.get("vision_analysis", "")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    vault_path = f"ingested/youtube/{video_id}.md"

    frontmatter = (
        f"---\n"
        f'title: "{title}"\n'
        f'date: "{now}"\n'
        f"type: video\n"
        f'source: "youtube"\n'
        f'url: "https://www.youtube.com/watch?v={video_id}"\n'
        f"ingestion_type: video_analyze\n"
        f"transcript_mode: {transcript_mode}\n"
        f'channel: "{channel}"\n'
        f"duration: {duration}\n"
        f"topics: {tags}\n"
        f"---\n\n"
    )

    body = f"# {title}\n\n"
    body += f"**Channel**: {channel} | **Duration**: {_format_duration(duration)} | **Published**: {upload_date}\n\n"

    if description:
        body += f"## Description\n\n{description}\n\n"

    if transcript:
        src = transcript_stats.get("source", "unknown")
        wc = transcript_stats.get("word_count", 0)
        body += f"## Transcript ({src}, {wc} words)\n\n{transcript}\n\n"

    if vision:
        body += f"## Vision Analysis\n\n{vision}\n\n"

    content = frontmatter + body
    return vault_path, content, body


def _persist_to_vault(result: dict, transcript_mode: str) -> dict:
    """Write analysis result to vault_notes. Returns status dict."""
    if not _db:
        return {"persisted": False, "reason": "no database configured"}

    vault_path, content, body = _build_vault_note(result, transcript_mode)
    ch = _content_hash(content)
    meta = result.get("metadata", {})
    title = meta.get("title", f"YouTube Video {result.get('video_id')}")
    video_id = result.get("video_id", "unknown")
    tags = meta.get("tags", []) or meta.get("categories", []) or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    tags = tags[:20]

    try:
        with _db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT content_hash FROM vault_notes WHERE path = %s", (vault_path,))
                row = cur.fetchone()
                if row:
                    existing_hash = row[0] if isinstance(row, tuple) else row.get("content_hash")
                    if existing_hash == ch:
                        return {"persisted": True, "status": "unchanged", "path": vault_path}

                embedding = _embed(f"{title}\n{body[:3000]}")

                import json as _json
                fm_dict = {
                    "title": title, "date": now, "type": "video",
                    "source": "youtube", "url": f"https://www.youtube.com/watch?v={video_id}",
                    "ingestion_type": "video_analyze", "transcript_mode": transcript_mode,
                    "channel": meta.get("channel", ""), "duration": meta.get("duration", 0),
                    "topics": tags,
                }
                cur.execute(
                    """
                    INSERT INTO vault_notes
                        (path, title, content, body, content_hash, embedding,
                         note_type, source, source_type, url, tags,
                         frontmatter, links, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (path) DO UPDATE SET
                        title        = EXCLUDED.title,
                        content      = EXCLUDED.content,
                        body         = EXCLUDED.body,
                        content_hash = EXCLUDED.content_hash,
                        embedding    = EXCLUDED.embedding,
                        tags         = EXCLUDED.tags,
                        frontmatter  = EXCLUDED.frontmatter,
                        updated_at   = NOW()
                    """,
                    (vault_path, title, content, body, ch, embedding,
                     "video", "youtube", "video_analyze",
                     f"https://www.youtube.com/watch?v={video_id}", tags,
                     _json.dumps(fm_dict), []),
                )
                conn.commit()

        status = "updated" if row else "created"
        return {"persisted": True, "status": status, "path": vault_path}
    except Exception as e:
        _logger.error("DB error persisting video %s: %s", video_id, e)
        return {"persisted": False, "reason": str(e)}


async def execute(
    video_id: Optional[str] = None,
    video_url: Optional[str] = None,
    extract_frames: bool = True,
    frame_interval: Optional[int] = None,
    max_frames: Optional[int] = None,
    cache_results: bool = True,
    transcript_mode: str = "auto",
    persist_to_db: bool = True,
) -> dict:
    """Full video analysis pipeline with vault_notes persistence."""
    from galdr_video_analyzer.core.analyzer import analyze_video

    cfg = _config or {}
    frame_interval = frame_interval or cfg.get('default_frame_interval', 30)
    max_frames = max_frames or cfg.get('max_frames', 10)

    result = await analyze_video(
        video_id=video_id,
        video_url=video_url,
        extract_frames=extract_frames,
        frame_interval=frame_interval,
        max_frames=max_frames,
        cache_results=cache_results,
        config=_config,
        transcript_mode=transcript_mode,
    )

    if result.get("success") and persist_to_db:
        db_result = _persist_to_vault(result, transcript_mode)
        result["vault_persist"] = db_result
        _logger.info("Video %s vault persist: %s", result.get("video_id"), db_result)

    return result
