"""
url_backlog_processor — Classify and route a batch of URLs to appropriate ingest tools.

Accepts a list of URLs, auto-classifies each by type (YouTube, GitHub, paper,
docs, article, junk), and dispatches to the right handler. YouTube URLs are
returned for agent-mediated processing; all others are ingested server-side.
"""
import asyncio
import logging
import re
from typing import Optional
from urllib.parse import urlparse

TOOL_NAME = "url_backlog_processor"

TOOL_DESCRIPTION = (
    "Classify and process a batch of URLs. Auto-detects type (YouTube, GitHub, "
    "paper, docs, article) and routes to the appropriate ingest tool. "
    "YouTube URLs are returned for agent processing; others are ingested directly. "
    "Use dry_run=true to classify without ingesting. Max 200 URLs per call."
)

TOOL_PARAMS = {
    "urls": "List of URL strings to process (max 200)",
    "dry_run": "If true, classify only — don't ingest (default: false)",
    "skip_existing": "Skip URLs already in vault_notes (default: true)",
    "youtube_mode": (
        "How to handle YouTube videos: "
        "'return' = return video IDs for agent to process (default), "
        "'metadata' = auto-ingest metadata + captions only (fast, no download), "
        "'audio' = download audio + Whisper STT + metadata (handles fresh uploads without captions), "
        "'full' = full video_analyze with frame extraction + Claude vision (slow, expensive)"
    ),
}

_db = None
_embedding_gen = None
_config = None
_logger = logging.getLogger(__name__)

YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
GITHUB_DOMAIN = "github.com"
GIST_DOMAIN = "gist.github.com"
HF_DOMAIN = "huggingface.co"

_GITHUB_NON_REPO_PATHS = {
    "orgs", "settings", "notifications", "explore", "topics",
    "trending", "collections", "sponsors", "marketplace", "pulls",
    "issues", "codespaces", "features", "security", "pricing",
    "login", "signup", "join", "about", "enterprise", "team",
}

SKIP_DOMAINS = {
    "google.com", "www.google.com",
    "rxinform.org", "startlilly.com", "app.gifthealth.com",
    "ma.lotto.com", "udisc.com", "tools.usps.com",
    "thecountrydiner.com", "www.godaddy.com", "kilo.ai",
}

DOCS_PATTERNS = [
    (re.compile(r"cursor\.com/(docs|en-US/docs)"), "cursor"),
    (re.compile(r"(docs\.anthropic\.com|platform\.claude\.com/docs|code\.claude\.com/docs)"), "claude"),
    (re.compile(r"ai\.google\.dev"), "gemini"),
    (re.compile(r"antigravity\.google/docs"), "antigravity"),
    (re.compile(r"developers\.openai\.com/(codex|docs)"), "openai"),
    (re.compile(r"opencode\.ai/docs"), "opencode"),
    (re.compile(r"vercel\.com/(docs|blog)"), "vercel"),
]

YOUTUBE_VIDEO_RE = re.compile(r"[?&]v=([a-zA-Z0-9_-]{11})")
YOUTUBE_SHORT_RE = re.compile(r"/shorts/([a-zA-Z0-9_-]{11})")
YOUTUBE_PLAYLIST_RE = re.compile(r"[?&]list=([a-zA-Z0-9_-]+)")
HF_PAPER_RE = re.compile(r"huggingface\.co/papers/(\d{4}\.\d{4,5})")
ARXIV_RE = re.compile(r"arxiv\.org/(abs|pdf)/(\d{4}\.\d{4,5})")
GITHUB_REPO_RE = re.compile(r"github\.com/([^/]+)/([^/?#]+)")


def setup(context: dict):
    global _db, _embedding_gen, _config
    _db = context.get("db")
    _embedding_gen = context.get("embedding_generator")
    _config = context.get("config", {})


def _classify(url: str) -> dict:
    """Classify a URL into a type and extract relevant metadata."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").lower()

    if domain in SKIP_DOMAINS:
        return {"type": "skip", "reason": "personal/junk domain"}

    if domain in YOUTUBE_DOMAINS:
        playlist_m = YOUTUBE_PLAYLIST_RE.search(url)
        if playlist_m and "watch" not in parsed.path:
            return {"type": "youtube_playlist", "playlist_id": playlist_m.group(1)}

        short_m = YOUTUBE_SHORT_RE.search(parsed.path)
        if short_m:
            return {"type": "youtube_short", "video_id": short_m.group(1)}

        video_m = YOUTUBE_VIDEO_RE.search(url)
        if video_m:
            return {"type": "youtube_video", "video_id": video_m.group(1)}

        if "/feed/" in parsed.path or "/playlist" in parsed.path:
            playlist_m2 = YOUTUBE_PLAYLIST_RE.search(url)
            if playlist_m2:
                return {"type": "youtube_playlist", "playlist_id": playlist_m2.group(1)}

        return {"type": "youtube_other", "reason": "unrecognized YouTube URL format"}

    if domain == GIST_DOMAIN:
        return {"type": "github_gist"}

    if domain == GITHUB_DOMAIN:
        repo_m = GITHUB_REPO_RE.search(f"https://{domain}{parsed.path}")
        if repo_m:
            owner, repo = repo_m.group(1), repo_m.group(2)
            if owner not in _GITHUB_NON_REPO_PATHS:
                return {
                    "type": "github_repo",
                    "owner": owner,
                    "repo": repo,
                    "canonical_url": f"https://github.com/{owner}/{repo}",
                }
        return {"type": "article"}

    hf_m = HF_PAPER_RE.search(url)
    if hf_m:
        return {"type": "paper", "arxiv_id": hf_m.group(1)}

    arxiv_m = ARXIV_RE.search(url)
    if arxiv_m:
        return {"type": "paper", "arxiv_id": arxiv_m.group(2)}

    if domain == HF_DOMAIN:
        return {"type": "article"}

    for pattern, platform_name in DOCS_PATTERNS:
        if pattern.search(url):
            return {"type": "docs", "platform": platform_name}

    return {"type": "article"}


async def _check_existing(urls: list[str]) -> set[str]:
    """Return set of URLs already in vault_notes."""
    if not _db:
        return set()
    try:
        with _db.get_cursor() as cur:
            cur.execute("SELECT url FROM vault_notes WHERE url = ANY(%s)", (urls,))
            rows = cur.fetchall()
            return {
                (r[0] if isinstance(r, tuple) else r.get("url", ""))
                for r in rows
            }
    except Exception:
        return set()


async def execute(
    urls: list,
    dry_run: bool = False,
    skip_existing: bool = True,
    youtube_mode: str = "return",
) -> dict:
    if not urls:
        return {"success": False, "error": "urls list is required"}
    if len(urls) > 200:
        return {"success": False, "error": f"Max 200 URLs per call, got {len(urls)}"}

    classified = {}
    for url in urls:
        url = url.strip()
        if not url or not url.startswith("http"):
            continue
        info = _classify(url)
        url_type = info["type"]
        if url_type not in classified:
            classified[url_type] = []
        classified[url_type].append({"url": url, **info})

    type_counts = {t: len(items) for t, items in classified.items()}

    if dry_run:
        return {
            "success": True,
            "mode": "dry_run",
            "total": sum(type_counts.values()),
            "classified": type_counts,
            "details": classified,
        }

    existing_urls = set()
    if skip_existing:
        all_urls = [item["url"] for items in classified.values() for item in items]
        canonical_urls = [
            item.get("canonical_url")
            for items in classified.values()
            for item in items
            if item.get("canonical_url")
        ]
        existing_urls = await _check_existing(all_urls + canonical_urls)

    results = {
        "youtube_videos": [],
        "youtube_shorts": [],
        "youtube_playlists": [],
        "processed": {"created": 0, "updated": 0, "unchanged": 0, "skipped": 0},
        "errors": [],
        "skipped": [],
    }

    if youtube_mode in ("metadata", "audio", "full"):
        from galdr.tools.plugins import video_analyze
        if hasattr(video_analyze, "setup"):
            video_analyze.setup({"config": _config or {}})
        for item in classified.get("youtube_video", []) + classified.get("youtube_short", []):
            vid = item["video_id"]
            if item["url"] in existing_urls:
                results["processed"]["skipped"] += 1
                continue
            try:
                if youtube_mode == "full":
                    r = await video_analyze.execute(
                        video_id=vid, extract_frames=True, transcript_mode="auto",
                    )
                elif youtube_mode == "audio":
                    r = await video_analyze.execute(
                        video_id=vid, extract_frames=False, transcript_mode="auto",
                    )
                else:
                    r = await video_analyze.execute(
                        video_id=vid, extract_frames=False, transcript_mode="captions",
                    )
                if r.get("success"):
                    results["processed"]["created"] += 1
                else:
                    results["errors"].append({"url": item["url"], "error": r.get("error")})
            except Exception as e:
                results["errors"].append({"url": item["url"], "error": str(e)})
            await asyncio.sleep(2)
    else:
        for item in classified.get("youtube_video", []):
            results["youtube_videos"].append(item["video_id"])
        for item in classified.get("youtube_short", []):
            results["youtube_shorts"].append(item["video_id"])

    for item in classified.get("youtube_playlist", []):
        results["youtube_playlists"].append(item["playlist_id"])

    for item in classified.get("skip", []):
        results["skipped"].append(item["url"])
    for item in classified.get("youtube_other", []):
        results["skipped"].append(item["url"])

    from galdr.tools.plugins import github_ingest, paper_ingest, url_ingest

    _ctx = {"db": _db, "embedding_generator": _embedding_gen, "config": _config or {}}
    for _plug in (github_ingest, paper_ingest, url_ingest):
        if hasattr(_plug, "setup"):
            _plug.setup(_ctx)

    seen_repos = set()
    for item in classified.get("github_repo", []):
        canonical = item.get("canonical_url", item["url"])
        if canonical in seen_repos:
            results["processed"]["skipped"] += 1
            continue
        seen_repos.add(canonical)
        if canonical in existing_urls or item["url"] in existing_urls:
            results["processed"]["skipped"] += 1
            continue
        try:
            r = await github_ingest.execute(url=canonical)
            if r.get("success"):
                results["processed"][r.get("status", "created")] += 1
            else:
                results["errors"].append({"url": canonical, "error": r.get("error")})
        except Exception as e:
            results["errors"].append({"url": canonical, "error": str(e)})
        await asyncio.sleep(1)

    for item in classified.get("paper", []):
        if item["url"] in existing_urls:
            results["processed"]["skipped"] += 1
            continue
        try:
            r = await paper_ingest.execute(url=item["url"])
            if r.get("success"):
                results["processed"][r.get("status", "created")] += 1
            else:
                results["errors"].append({"url": item["url"], "error": r.get("error")})
        except Exception as e:
            results["errors"].append({"url": item["url"], "error": str(e)})
        await asyncio.sleep(1)

    for item in classified.get("article", []) + classified.get("github_gist", []):
        if item["url"] in existing_urls:
            results["processed"]["skipped"] += 1
            continue
        try:
            r = await url_ingest.execute(url=item["url"])
            if r.get("success"):
                results["processed"][r.get("status", "created")] += 1
            else:
                results["errors"].append({"url": item["url"], "error": r.get("error")})
        except Exception as e:
            results["errors"].append({"url": item["url"], "error": str(e)})
        await asyncio.sleep(1)

    for item in classified.get("docs", []):
        results["skipped"].append(item["url"])

    return {
        "success": True,
        "mode": "process",
        "total": sum(type_counts.values()),
        "classified": type_counts,
        "youtube_videos": results["youtube_videos"],
        "youtube_shorts": results["youtube_shorts"],
        "youtube_playlists": results["youtube_playlists"],
        "processed": results["processed"],
        "errors": results["errors"][:20],
        "skipped_count": len(results["skipped"]),
        "error_count": len(results["errors"]),
    }
