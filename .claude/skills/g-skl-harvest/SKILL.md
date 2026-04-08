---
name: g-skl-harvest
description: Analyze external sources (GitHub repos, URLs) for adoptable patterns and improvements. Produces structured harvest reports and optional IDEA_BOARD suggestions. Zero-change-without-approval — never modifies project files. No Docker, no MCP.
---
# g-harvest

**Vault output**: `research/harvests/`

**Activate for**: "harvest ideas from", "analyze this repo for patterns", "what can we learn from", "review past harvests", any request to borrow ideas from external sources.

---

## Principle

> Analyze external sources. Present selective improvement suggestions.
> **User approves what to adopt — nothing changes without approval.**

Harvest is NOT vault ingestion (that stores knowledge for RAG). It is specifically about looking *outward* at other codebases and articles to find patterns worth borrowing. It writes vault notes and suggests IDEA_BOARD entries. It never modifies project code, configs, or skills.

---

## Operation: HARVEST_REPO

Analyze a GitHub repository for adoptable patterns.

**Step 1 — Resolve repo:**
- Check `.galdr/.identity` for `repos_location`
- If `repos_location` is set, look for the repo under that path
- If not mirrored: inform the user and offer to add to `repos.txt` via `g-skl-vault` GitHub Repo flow, then re-run after sync

**Step 2 — Read key files** (no binary files, no node_modules, no .git):
- `README.md` and top-level docs
- Skill/command/rule/hook files (`.cursor/`, `.claude/`, etc.)
- Config files (`pyproject.toml`, `package.json`, `CONSTRAINTS.md`, etc.)

**Step 3 — Generate structured harvest report:**
For each notable pattern found, produce:
- What the pattern is
- Where it appears in the source (file reference)
- Why it's worth considering
- Complexity estimate: `low` (add a file/field) | `medium` (new subsystem) | `high` (multi-task refactor)
- A draft IDEA_BOARD entry

**Step 4 — Write harvest note** to `research/harvests/{YYYY-MM-DD}_{slug}.md`

**Step 5 — For each suggestion:**
Ask the user: "Post this to IDEA_BOARD? (y/n/skip-all)". Only post on explicit `y`.

---

## Operation: HARVEST_URL

Analyze a URL for architectural decisions, tooling choices, and workflow patterns.

**Step 1 — Crawl** the URL using `g-skl-crawl` FETCH. (Requires crawl4ai setup.)

**Step 2 — Extract from the crawled Markdown:**
- Technology/tooling choices mentioned
- Architectural decisions documented
- Workflow patterns described
- Constraints or lessons learned

**Step 3 — Same report + IDEA_BOARD flow as HARVEST_REPO**

Note: URL harvest is about idea extraction, not content storage. If you also want to store the content, run `@g-ingest-url` separately.

---

## Operation: HARVEST_REVIEW

Review past harvest notes and surface unadopted suggestions.

1. Scan `research/harvests/` for notes where `harvest_status: reviewed` (not `fully_adopted`)
2. For each unadopted suggestion, present:
   - Source: `{title}` from `{date}`
   - Suggestion text + complexity
   - Current IDEA_BOARD status
3. User can: promote to IDEA_BOARD, shelve, or dismiss each

---

## Harvest Note Schema

```yaml
---
date: 2026-04-06
type: harvest
ingestion_type: harvest_analysis
source: https://github.com/owner/repo
title: "Harvest: owner/repo"
topics: []
harvest_status: reviewed      # reviewed | partially_adopted | fully_adopted
suggestions_total: 5
suggestions_adopted: 0
---

## Source Overview
{1-2 sentences: what was analyzed and why}

## Suggestions

### 1. {Suggestion Title} [complexity: low]
**Pattern found in**: `path/to/file.md`
**What it does**: ...
**Why adopt**: ...
**IDEA_BOARD status**: pending | posted as IDEA-042 | shelved
```

---

## GitHub Repo Coordination

When `@g-harvest {github_url}` targets an unmirrored repo:

1. Check `repos_location` from `.galdr/.identity`
2. If `repos_location` is set but repo not found:
   - Suggest: "Add `{github_url}` to `{repos_location}/repos.txt` and run `@g-vault-ingest` to mirror it, then re-run harvest"
3. If `repos_location` is not set:
   - Suggest using HARVEST_URL instead (crawl GitHub web pages)

---

## Hard Constraints

- **Never modify project files** — harvest only writes vault notes and IDEA_BOARD entries
- **IDEA_BOARD posting requires explicit user confirmation per suggestion**
- **Zero scope creep** — if a suggestion would take >2 days to implement, mark complexity `high` and let the user decide whether to create a task
