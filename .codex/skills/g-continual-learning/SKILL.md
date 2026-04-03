---
name: g-continual-learning
version: 1.0.0
description: Incremental transcript scanning to extract durable facts and update AGENTS.md, CLAUDE.md, and vault
globs: ["**/agent-transcripts/**/*.jsonl", "**/AGENTS.md", "**/agents.md"]
---

# Continual Learning

Scan agent transcripts incrementally, extract high-signal durable facts, and persist them to three destinations:
1. **AGENTS.md** — read by Cursor, Codex, Copilot, Gemini natively
2. **CLAUDE.md** — read by Claude Code natively
3. **Vault** — searchable via MCP across all platforms

## Architecture

```
agent-complete.ps1          session-start.ps1
       │                           │
       ▼                           ▼
  pending_reflection.json    reflection banner
  session stubs (.md)        (reminds to run this skill)
       │                           │
       └───────────┬───────────────┘
                   ▼
        galdr-continual-learning
                   │
           ┌───────┼───────┐
           ▼       ▼       ▼
      AGENTS.md  CLAUDE.md  vault/projects/{name}/decisions/
```

## Index File

**Path**: `.cursor/hooks/state/continual-learning-index.json`

```json
{
  "version": 1,
  "transcripts": {
    "<full-path-to-transcript.jsonl>": {
      "mtimeMs": 1774715482108.0
    }
  }
}
```

## Workflow

### Step 1: Load Index

Read `.cursor/hooks/state/continual-learning-index.json`. If missing, start with `{"version": 1, "transcripts": {}}`.

### Step 2: Discover Transcripts

List all `.jsonl` files in the agent-transcripts directory. The path is platform-dependent:
- **Windows**: `C:\Users\{user}\.cursor\projects\{project-slug}\agent-transcripts\`
- Transcripts live in `{uuid}/{uuid}.jsonl` subdirectories
- **Skip** subagent transcripts (nested deeper than `{uuid}/{uuid}.jsonl`)

### Step 3: Diff Against Index

For each transcript:
- **New**: not in index → needs processing
- **Changed**: current `mtimeMs` > indexed `mtimeMs` → needs processing
- **Unchanged**: skip
- **Deleted**: in index but file no longer exists → remove from index

### Step 4: Extract High-Signal Patterns

Search each new/changed transcript for **recurring user corrections and durable workspace facts**:

**INCLUDE** (high-signal, durable):
- Recurring corrections: "no, do it this way", "always use X", "never do Y"
- Workflow preferences stated 2+ times across sessions
- Architectural decisions and constraints
- Tool/library preferences (e.g., "use UV not pip")
- Naming conventions and code style rules
- Project structure facts that won't change often

**EXCLUDE** (low-signal, transient):
- One-off debugging details
- Specific file contents or line numbers
- Secrets, API keys, tokens, passwords
- Task-specific implementation steps
- Single-occurrence preferences (must recur to be durable)
- Anything already captured in AGENTS.md

**Search patterns** (grep in user messages):
- `always`, `never`, `don't`, `do not`
- `make sure`, `remember`, `from now on`, `going forward`
- `instead of`, `not X, use Y`, `the correct way`
- `important:`, `rule:`, `convention:`

### Step 5: Update AGENTS.md

Read `AGENTS.md` (may be lowercase `agents.md` on disk — check with glob).

If new durable facts were found that are NOT already present:
1. Find the `## Learned Workspace Facts` section (create it if missing, before the final `---` separator)
2. Append new facts as numbered entries with a date stamp
3. Keep entries concise (1-2 sentences each)

Format:
```markdown
## Learned Workspace Facts

1. **UV for Python** — Always use UV for virtual environment management, never pip or venv directly. _(2026-02-15)_
2. **Template parity** — Three .galdr template dirs are equal peers; must use {placeholders}. _(2026-03-12)_
```

If no meaningful updates exist, respond exactly: `No high-signal memory updates.`

### Step 6: Update CLAUDE.md

Read `CLAUDE.md` from the project root.

If new facts were added to AGENTS.md in Step 5:
1. Find the `## Learned Workspace Facts` section in CLAUDE.md (create it if missing, before the final `---` separator)
2. Keep this section **identical** to the one in AGENTS.md — same numbered entries, same format
3. This ensures Claude Code sees the same durable facts that Cursor/Codex/Copilot see via AGENTS.md

### Step 7: Write to Vault

If new facts were extracted in Step 4, write a vault note so the knowledge is searchable via MCP.

**Resolve vault path**: Source `vault-resolve.ps1` or use `GALDR_KNOWLEDGE_WELL_PATH` env var, falling back to `.galdr/vault/`.

**Path**: `{vault}/projects/{project_name}/decisions/{date}_continual_learning.md`

If a file for today's date already exists, append the new facts to it rather than creating a duplicate.

**Frontmatter**:
```yaml
---
date: {YYYY-MM-DD}
type: decision
ingestion_type: continual_learning
source: agent-transcripts
title: "Continual Learning — {project_name} ({date})"
topics: [continual-learning, workspace-facts, {project_name}]
project_id: {from .galdr/.project_id}
refresh_policy: none
---
```

**Body**: List each new fact with the same format as AGENTS.md, plus which transcript(s) it was extracted from.

### Step 8: Update Index

Write the updated index back to `.cursor/hooks/state/continual-learning-index.json`:
- Add/update entries for all processed transcripts with current `mtimeMs`
- Remove entries for deleted transcripts
- Preserve entries for unchanged transcripts

### Step 9: Clean Up Reflection Hint

If `.galdr/logs/pending_reflection.json` exists, remove it — the learning pass satisfies the reflection.

## When to Run

| Trigger | Source |
|---------|--------|
| User runs `@g-continual-learning` | Manual command |
| `session-start.ps1` shows reflection banner | User follows the prompt |
| End of a long session (10+ turns) | Best practice |
| After pulling changes from another machine | Catch up on remote work |

## Notes

- This skill reads transcripts read-only — it never modifies them
- Mutable outputs: index file, AGENTS.md, CLAUDE.md, vault note
- AGENTS.md and CLAUDE.md `## Learned Workspace Facts` sections must stay identical
- Platform parity: the skill definition exists in `.cursor/`, `.claude/`, `.agent/` but the index file is IDE-specific (`.cursor/hooks/state/`)
- Vault notes go under `projects/{name}/decisions/` because learned facts are architectural decisions
- If vault path is unavailable (no env var, no `.galdr/vault/`), skip the vault write — AGENTS.md and CLAUDE.md are sufficient
