# g-ingest-youtube

Ingest a YouTube video transcript into the vault knowledge store.

Activates **g-skl-ingest-youtube** → INGEST_YOUTUBE operation.

## Usage

```
@g-ingest-youtube https://www.youtube.com/watch?v=VIDEO_ID
```

## What it does

1. Fetches video metadata (title, channel, duration, upload date) via yt-dlp
2. Downloads transcript/captions (manual → auto-generated → translated, in priority order)
3. Parses VTT captions to clean text (no timestamps, deduplicated rolling lines)
4. Generates summary and key points from transcript
5. Writes vault note to `research/videos/` with `analysis_depth: transcript_only`
6. Updates `vault/log.md` and `vault/_index.yaml`

## Notes

- No video download — transcript only
- No Docker, no MCP required (uses yt-dlp locally)
- Notes include `analysis_depth: transcript_only` — a future task can upgrade to full vision analysis
- If no captions are available, creates a metadata-only note with a warning
- First-time setup: `pip install yt-dlp`

## Check setup

```
@g-ingest-youtube --check-setup
```
