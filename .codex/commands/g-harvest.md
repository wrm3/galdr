# g-harvest

Analyze external sources for patterns worth adopting — GitHub repos or URLs.

Activates **g-skl-harvest** → HARVEST_REPO, HARVEST_URL, or HARVEST_REVIEW operation.

## Usage

```
@g-harvest https://github.com/owner/repo
@g-harvest https://example.com/article-on-architecture
@g-harvest --review
```

## What it does

**HARVEST_REPO / HARVEST_URL:**
1. Reads key files from the repo (or crawls the URL via `g-skl-crawl`)
2. Extracts patterns, architecture decisions, tooling choices, workflow ideas
3. Writes a structured harvest report to `research/harvests/`
4. **Optionally** posts each suggestion to `IDEA_BOARD.md` — only with explicit user `y`

**HARVEST_REVIEW:**
1. Scans `research/harvests/` for unadopted suggestions
2. Presents them for user triage (promote / shelve / dismiss)

## Zero-change-without-approval guarantee

Harvest **never modifies project files, code, configs, or skills**.  
It only writes vault notes and — only with explicit confirmation — IDEA_BOARD entries.

## Notes

- URL harvest requires `g-skl-crawl` (crawl4ai) — run `@g-crawl SETUP` first
- Repo harvest works from existing `repos_location` mirrors or GitHub web pages
- If a repo isn't mirrored yet, harvest will guide you through the repos.txt flow
