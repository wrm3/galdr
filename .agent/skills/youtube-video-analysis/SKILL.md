---
name: youtube-video-analysis
description: YouTube URLs—MCP download, metadata, transcript, frames, vision analysis, playlists, batch.
mcp_tools:
  - user-galdr_mcp_video_analyzer-video_analyze
  - user-galdr_mcp_video_analyzer-video_extract_metadata
  - user-galdr_mcp_video_analyzer-video_extract_transcript
  - user-galdr_mcp_video_analyzer-video_extract_frames
  - user-galdr_mcp_video_analyzer-video_get_playlist
  - user-galdr_mcp_video_analyzer-video_check_new
  - user-galdr_mcp_video_analyzer-video_batch_process
---

# YouTube Video Analysis Skill

Extract knowledge from YouTube videos through automated downloading, transcription, and analysis. Transform video content into actionable summaries, code templates, requirements documents, and structured data.

## Overview

This skill provides end-to-end YouTube video processing via MCP tools:

1. **Download**: Fetch YouTube videos by URL or ID
2. **Metadata**: Extract title, description, channel, duration, tags
3. **Transcribe**: Get video transcript/captions
4. **Frames**: Extract key frames at intervals
5. **Vision**: Analyze frames with Claude vision
6. **Batch**: Process multiple videos efficiently

## MCP Tools Available

### Core Analysis
| Tool | Description |
|------|-------------|
| `video_analyze` | Full analysis pipeline (metadata + transcript + frames + vision) |
| `video_extract_metadata` | Get video title, description, channel, duration, etc. |
| `video_extract_transcript` | Get video transcript/captions |
| `video_extract_frames` | Extract key frames from video |

### Playlist Operations
| Tool | Description |
|------|-------------|
| `video_get_playlist` | Get list of videos from a YouTube playlist |
| `video_check_new` | Check for new videos since last check |
| `video_batch_process` | Process multiple videos efficiently |

### Server Status
| Tool | Description |
|------|-------------|
| `video_server_status` | Get server status and loaded plugins |

## When to Use This Skill

### Automatic Triggers
- User provides a YouTube URL
- User mentions "analyze this video"
- User asks to "extract information from video"
- User wants to "learn from tutorial video"
- User requests "video summary" or "video transcript"

## Workflow Examples

### Example 1: Full Video Analysis

**User**: "Analyze this video: https://youtu.be/example"

**Action**: Use `video_analyze` tool

```
Call: video_analyze(video_url="https://youtu.be/example")

Returns:
- metadata (title, channel, duration, etc.)
- transcript (full text + segments)
- frames (extracted frame paths)
- vision_analysis (Claude analysis of frames)
```

### Example 2: Quick Transcript Only

**User**: "Get the transcript from this video"

**Action**: Use `video_extract_transcript` tool

```
Call: video_extract_transcript(video_url="https://youtu.be/example")

Returns:
- transcript (full text)
- segments (timestamped segments)
- word_count, character_count
- source (manual or auto-generated)
```

### Example 3: Playlist Monitoring

**User**: "Check this playlist for new videos"

**Action**: Use `video_check_new` tool

```
Call: video_check_new(playlist_url="https://youtube.com/playlist?list=...")

Returns:
- new_videos (list of videos added since last check)
- new_count
- total_in_playlist
- state_updated (tracking for next check)
```

### Example 4: Batch Processing

**User**: "Analyze all videos in this playlist"

**Action**: 
1. Use `video_get_playlist` to get video IDs
2. Use `video_batch_process` to analyze them

```
# Step 1: Get playlist
playlist = video_get_playlist(playlist_url="...")

# Step 2: Batch process
results = video_batch_process(
    video_ids=",".join([v['video_id'] for v in playlist['videos']]),
    concurrency=3
)
```

## Supported Video Types

### 1. Trading Strategy Videos
Extract structured trading information:
- Strategy name and overview
- Entry and exit criteria
- Technical indicators used
- Risk management rules

### 2. Framework/Tool Tutorials
Extract technical documentation:
- Tool/framework name and purpose
- Installation steps
- Code examples
- Best practices

### 3. General Educational Content
Extract key insights:
- Content summary
- Main topics covered
- Key points and takeaways
- Action items

## Technical Details

### Dependencies (Docker Service)
- `yt-dlp` - YouTube downloading
- `opencv-python` - Frame extraction
- `anthropic` - Vision analysis
- `aiofiles` - Async file operations

### Docker Service
The video analyzer runs as a Docker service on port 8084:

```yaml
# In docker-compose.yml
video_analyzer:
  container_name: GALDR_video_analyzer
  ports:
    - "8084:8084"
```

### Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required for vision analysis
FRAME_INTERVAL=30              # Seconds between frame captures
MAX_FRAMES=10                  # Maximum frames to extract
```

## Best Practices

### Video Selection
- ✅ Choose high-quality audio (clear speech)
- ✅ Prefer shorter videos (<30 minutes) for faster processing
- ❌ Avoid videos with heavy music or sound effects
- ❌ Avoid videos with multiple simultaneous speakers

### Performance Tips
- Use `video_extract_transcript` for quick text extraction
- Use `video_analyze` for comprehensive analysis
- Use `video_batch_process` for multiple videos
- Results are cached - subsequent calls return cached data

### Frame Analysis
- Vision analysis requires `ANTHROPIC_API_KEY`
- Default: 10 frames at 30-second intervals
- Adjust `frame_interval` and `max_frames` as needed

## Limitations

### Current Limitations
- **Language**: Best results with English audio
- **Speed**: Frame extraction requires video download
- **Video Length**: Very long videos may take time
- **Private Videos**: Cannot access private/age-restricted content

### Not Supported
- ❌ Live streams (must be recorded first)
- ❌ Age-restricted videos
- ❌ Private videos
- ❌ DRM-protected content

## Vault Integration

After `video_analyze` returns, **always** write a vault summary note. The agent writes this directly — no MCP needed.

### Post-Analysis Vault Write

After receiving the analysis result, write a file to the vault:

**Path**: `{vault}/research/videos/{date}_{safe_title}.md`

**Template**:
```markdown
---
date: YYYY-MM-DD
project: {project_name}
project_id: {from .galdr/.project_id}
source: {video_url}
type: video_analysis
ingestion_type: video_analysis
topics: [video, {channel}, {topic}]
url: {video_url}
title: "{video_title}"
channel: "{channel_name}"
duration: "{duration}"
refresh_policy: none
---

# {video_title}

## Key Takeaways
- {bullet points from analysis}

## Transcript Summary
{condensed summary of transcript}

## Visual Analysis
{summary of frame analysis if available}

## Timestamps
- 0:00 - {topic}
- {more timestamps from segments}

## Relevance
{how this relates to current projects}
```

### Vault Path Resolution

Read `.galdr/.project_id` to get the project UUID. Resolve the vault path (check `.env` for `GALDR_KNOWLEDGE_WELL_PATH`, else use `.galdr/vault/`).

Write one file under `{vault}/research/videos/{date}_{safe_title}.md`. All vault content is global; `project` / `project_id` in frontmatter tie the note to the active project.

### Safe Filename

Convert the video title to a safe filename:
- Lowercase, replace spaces with hyphens
- Remove special characters
- Truncate to 80 characters
- Prefix with date: `2026-03-20_how-to-build-mcp-servers.md`

## Integration with Other Skills

### RAG Storage
Combine with `youtube-rag-storage` skill to:
- Store transcripts in vector database
- Enable semantic search across videos
- Build knowledge base from video content

### Specialized Analysis
Combine with `hanx-youtube-researcher` skill for:
- Trading strategy extraction
- Framework documentation
- Domain-specific analysis

---

**Version**: 1.0.0
**MCP Server**: galdr_mcp_video_analyzer
**Docker Port**: 8084
**Status**: Production Ready
