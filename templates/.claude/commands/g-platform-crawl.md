# @g-platform-crawl — Crawl Platform Docs with Crawl4AI

**Purpose**: Crawl platform documentation or arbitrary web pages using the free, open-source crawl4ai library. Saves to `.platforms/` and the vault with proper frontmatter.

**Safe to run**: Yes — incremental by default (only saves changed pages).

---

## Usage

- `@g-platform-crawl` — List all configured targets and their freshness status
- `@g-platform-crawl cursor` — Crawl Cursor IDE docs
- `@g-platform-crawl all` — Crawl all configured platforms
- `@g-platform-crawl --diff cursor` — Preview changes without saving
- `@g-platform-crawl --url https://example.com/docs` — Crawl an arbitrary URL

---

## What It Does

1. **Reads the `g-platform-crawl` skill** for configuration and workflow
2. **Checks prerequisites** (crawl4ai installed, Playwright available)
3. **Runs `scripts/platform_crawl.py`** with the appropriate arguments
4. **Reports results** (new/updated/unchanged page counts)
5. **Runs `vault-reindex.ps1`** to update `_index.yaml`

---

## Configured Targets

| Name | URL | Max Pages |
|------|-----|-----------|
| cursor | cursor.com/en-US/docs | 300 |
| claude | docs.anthropic.com/en/docs | 300 |
| claude-api | docs.anthropic.com/en/api | 300 |
| claude-platform | platform.claude.com/docs | 300 |
| claude-code | code.claude.com/docs | 300 |
| gemini | ai.google.dev/gemini-api/docs | 300 |
| antigravity | antigravity.google/docs | 300 |
| openai-api | developers.openai.com/api/docs | 600 |
| openai-codex | developers.openai.com/codex/ | 300 |
| opencode | opencode.ai/docs/ | 300 |

---

## Prerequisites

```bash
pip install crawl4ai
crawl4ai-setup
python -m playwright install chromium
```

---

## Integration

- Works with `@g-knowledge-refresh` for freshness audits
- Called by `@g-cleanup` when platform docs are flagged as stale
- Works with `@g-knowledge-refresh` for freshness audits
