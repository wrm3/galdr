---
name: g-platform-crawl
description: Crawl docs and web with crawl4ai; write .platforms/ and vault markdown with frontmatter. For platform docs, knowledge refresh, web ingest.
---

# galdr-platform-crawl

Crawl platform documentation and arbitrary web pages using **crawl4ai** — a free, open-source web crawler. Produces LLM-ready markdown and writes to both `.platforms/` (local snapshots) and the vault (`research/platforms/`) with proper frontmatter.

## Architecture

```
Agent calls platform_crawl.py (host-side Python script)
        │
        ├── .platforms/{platform_dir}/   ← raw snapshots + JSON sidecar
        └── {vault}/research/platforms/{platform_dir}/  ← frontmatter-enriched .md
                                                           (searchable via _index.yaml)
```

**C-001 Compliant**: The script runs on the host machine, not inside Docker. Docker never touches the vault.

## Script Location

Scripts live inside the skill folder per C-007 (skill scripts must live inside the skill's own folder):

```
.cursor/skills/g-platform-crawl/scripts/platform_crawl.py
.cursor/skills/g-platform-crawl/scripts/platform_crawl_scheduled.ps1
```

Identical copies exist in `.claude/`, `.agent/`, and their `templates/` counterparts (6 total locations). When updating, edit one copy and propagate to all 6.

## Prerequisites

crawl4ai is listed in the project's `pyproject.toml` and `requirements.txt`. Install with:

```bash
uv sync                                    # recommended
# or: pip install -r requirements.txt

crawl4ai-setup                             # one-time browser setup
python -m playwright install chromium      # if browser issues
```

## Usage

### From the command line

```bash
# List all configured targets
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --list-targets

# Crawl a specific platform
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --target cursor

# Crawl all platforms
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --target all

# Preview changes without saving
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --target claude --diff-only

# Crawl an arbitrary URL
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --url https://example.com/docs --name my-docs --platform-dir MyDocs/docs

# Crawl without vault writes (platforms dir only)
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --target cursor --no-vault
```

### From an AI agent

When the user asks to crawl or refresh platform docs:

1. **Check freshness first**: Read `_index.yaml` or check `refresh_after` dates
2. **Run the script**: Execute `python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --target {name}`
3. **Report results**: Show new/updated/unchanged counts
4. **Reindex**: Run `vault-reindex.ps1` to update `_index.yaml`

### Ad-hoc URL crawling

For one-off URLs (articles, repos, etc.):

```bash
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py \
  --url https://example.com/interesting-article \
  --name article-name \
  --platform-dir articles/misc \
  --max-pages 1 \
  --max-depth 1
```

## Configured Targets

| Name | URL | Max Pages | Depth |
|------|-----|-----------|-------|
| cursor | cursor.com/en-US/docs | 300 | 4 |
| claude | docs.anthropic.com/en/docs | 300 | 4 |
| claude-api | docs.anthropic.com/en/api | 300 | 4 |
| claude-platform | platform.claude.com/docs | 300 | 4 |
| claude-code | code.claude.com/docs | 300 | 4 |
| gemini | ai.google.dev/gemini-api/docs | 300 | 4 |
| antigravity | antigravity.google/docs | 300 | 4 |
| openai-api | developers.openai.com/api/docs | 600 | 5 |
| openai-codex | developers.openai.com/codex/ | 300 | 4 |
| opencode | opencode.ai/docs/ | 300 | 4 |

## Output Format

### .platforms/ (raw snapshots)

Each page produces two files:
- `{safe_url}.md` — raw markdown content
- `{safe_url}.json` — metadata sidecar (URL, title, hash, crawl timestamp)

### Vault (research/platforms/)

Each page produces one file with YAML frontmatter:

```yaml
---
date: 2026-03-12
type: platform_doc
ingestion_type: crawl4ai
title: "Page Title"
source: "https://original-url.com/page"
topics: [AI, Platform, Cursor, documentation]
refresh_policy: weekly
refresh_after: 2026-03-19
expires_after: 2026-06-10
source_volatility: high
project_id: null
---

# Page content in markdown...
```

## Scheduled Crawling

Automated crawling uses `{vault}/.crawl_schedule.json` to prevent duplicate crawls across projects sharing a vault.

### Check freshness
```bash
python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --check-freshness --max-age-days 7
```

### Run the scheduled wrapper (checks freshness, crawls only stale targets)
```powershell
powershell -ExecutionPolicy Bypass -File .cursor/skills/g-platform-crawl/scripts/platform_crawl_scheduled.ps1
powershell -File .cursor/skills/g-platform-crawl/scripts/platform_crawl_scheduled.ps1 -MaxAgeDays 14
powershell -File .cursor/skills/g-platform-crawl/scripts/platform_crawl_scheduled.ps1 -Target cursor
```

### Register as Windows Scheduled Task (daily at 3 AM)
```powershell
$skillScripts = "G:\galdr\.cursor\skills\g-platform-crawl\scripts"
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File $skillScripts\platform_crawl_scheduled.ps1" `
    -WorkingDirectory "G:\galdr"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -TaskName "galdr-platform-crawl" -Action $action -Trigger $trigger
```

The schedule file lives at the vault root so all projects sharing the same vault see the same crawl state — no redundant crawls.

## Freshness Integration

Works with the `g-knowledge-refresh` skill:
- Platform docs have `refresh_policy: weekly` and `source_volatility: high`
- `g-cleanup` nightly audit flags stale platform docs
- Run `@g-knowledge-refresh` to see what needs re-crawling
- Then run `python .cursor/skills/g-platform-crawl/scripts/platform_crawl.py --target {name}` to refresh

## Notes

- **Free**: No API keys, no credits, no rate limits
- **Cached**: crawl4ai caches pages locally, subsequent runs are faster
- **Incremental**: Only saves pages whose content hash has changed
- **Headless**: Uses Playwright Chromium in headless mode
- **Anti-bot**: crawl4ai v0.8.5+ includes automatic anti-bot detection
