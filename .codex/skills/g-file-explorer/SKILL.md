---
name: g-file-explorer
description: >
  Full filesystem visibility for the AI agent — bypasses Cursor's Glob/Grep
  .gitignore limitation. Use whenever you need to find or read files that
  Glob/Grep cannot see (.galdr/, research/, gitignored projects, linked projects).
triggers:
  - "can't find the file"
  - "glob won't let you"
  - "gitignored"
  - ".galdr/ files"
  - "find in research/"
  - "look at Maestro2"
  - "file_index"
  - "g-file-explorer"
---

# g-file-explorer — Full Filesystem Visibility Skill

## Why This Exists

Cursor's `Glob` and `Grep` tools respect `.gitignore`. Any file excluded from git
is **invisible** to those tools. This includes:

- `.galdr/` task files (gitignored in this repo)
- `research/` notes and downloads
- `G:\Maestro2`, `P:\hieroglyphics`, `G:\CatchTheFraqUp`, etc.
- Any file the user wants to keep private/local

The `file_index` MCP tool solves this. It indexes the raw filesystem, stores
results in PostgreSQL, and exposes 4 actions that work regardless of `.gitignore`.

---

## Quick Reference

### When to use this skill

| Situation | Action |
|-----------|--------|
| Can't find a file via Glob | `file_index(action='find', pattern='*.md')` |
| Need to search inside gitignored files | `file_index(action='grep', pattern='TODO')` |
| Know exact path but Read fails | `file_index(action='read', path='...')` |
| Starting new session | `file_index(action='rebuild')` first |
| Searching across all active projects | Use `path_prefix` to scope |

### Session start checklist

1. The `session-start.ps1` hook calls `file-index-rebuild.ps1 -Silent` automatically
2. The rebuild runs at most once per 12 hours (cooldown stamped in `hooks/state/`)
3. If you need a fresh index mid-session: call `file_index(action='rebuild')`

---

## Tool Reference

### `file_index(action='rebuild')`

Walk all active project roots and build the index.

```
file_index(action='rebuild')
```

With custom roots:
```
file_index(
  action='rebuild',
  roots=['G:\\galdr', 'G:\\Maestro2', 'P:\\hieroglyphics']
)
```

Force full rebuild (drops + recreates):
```
file_index(action='rebuild', force_rebuild=True)
```

**Returns**: `files_added`, `files_updated`, `files_ignored`, `roots_indexed`, `roots_skipped`

---

### `file_index(action='find')`

Find files by name glob or path prefix. Fast — queries the DB index.

Find all markdown files:
```
file_index(action='find', pattern='*.md')
```

Find task files:
```
file_index(action='find', pattern='task*.md', path_prefix='G:\\galdr\\.galdr')
```

Find files in Hieroglyphics:
```
file_index(action='find', pattern='EXP-*.md', path_prefix='P:\\hieroglyphics')
```

Find by partial name:
```
file_index(action='find', pattern='*TASKS*')
```

**Returns**: list of `{path, filename, ext, size_bytes, modified, root}`

---

### `file_index(action='grep')`

Search file CONTENTS by regex. Reads actual files from disk.

Search for a string across all `.md` files:
```
file_index(action='grep', pattern='C-011', file_types='.md')
```

Search in a specific project:
```
file_index(
  action='grep',
  pattern='def setup',
  file_types='.py',
  path_prefix='G:\\galdr\\docker'
)
```

Search with context lines:
```
file_index(action='grep', pattern='TODO.*TASK', context_lines=3)
```

**Returns**: per-file matches with line numbers and context

---

### `file_index(action='read')`

Read any file from disk — including gitignored files.

```
file_index(action='read', path='G:\\galdr\\.galdr\\TASKS.md')
```

Read a large file in chunks:
```
file_index(action='read', path='...', max_bytes=20000)
# Then use next_offset_bytes from response to paginate
file_index(action='read', path='...', max_bytes=20000, offset_bytes=20147)
```

**Returns**: `content`, `size_bytes`, `truncated`, `next_offset_bytes` (if truncated)

---

## .galdrignore Control

Each indexed root can have a `.galdrignore` file — same syntax as `.gitignore`.
The galdr source repo ships a default at `G:\galdr\.galdrignore`.

**What gets excluded by default:**
- Binary files (`.exe`, `.dll`, `.so`, images, videos, archives)
- Package manager artifacts (`node_modules/`, `.venv/`, `dist/`)
- Lock files (`package-lock.json`, `uv.lock`)
- Database files (`.db`, `.sqlite`, `.csv`, `.parquet`)
- **Secrets** (`.env`, `*.pem`, `*.key`) — NEVER indexed

**To expose more files**: remove or comment out patterns in `.galdrignore`  
**To hide more files**: add patterns to `.galdrignore` in the project root

---

## Common Workflows

### "Find all task files for Maestro2"
```
file_index(action='find', pattern='task*.md', path_prefix='G:\\Maestro2\\.galdr\\tasks')
```

### "What's in the research folder?"
```
file_index(action='find', path_prefix='G:\\galdr\\research', max_results=100)
```

### "Find where C-011 is referenced"
```
file_index(action='grep', pattern='C-011', file_types='.md')
```

### "Read the Hieroglyphics TASKS.md"
```
file_index(action='read', path='P:\\hieroglyphics\\.galdr\\TASKS.md')
```

### "Find all Python files in the MCP server that import a plugin"
```
file_index(
  action='grep',
  pattern='from.*plugins import',
  file_types='.py',
  path_prefix='G:\\galdr\\docker'
)
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `file_find` returns 0 results | Run `file_index(action='rebuild')` first |
| Root skipped in rebuild | Check the path exists on disk |
| MCP server not reachable | `cd G:\galdr\docker && docker compose up -d` |
| File not found in `read` | Use exact absolute path with double backslashes |
| Index stale after file changes | Call `file_index(action='rebuild')` — it does incremental updates |

---

## Notes

- The index is stored in PostgreSQL `file_index` table in the galdr Docker container
- Rebuilds are **incremental by default** — only new/changed files are upserted
- `force_rebuild=True` drops the full index and rewrites from scratch (~30-60s for all projects)
- The `session-start.ps1` hook runs rebuild silently, max once per 12 hours
- No Cursor license required — entirely server-side via MCP
