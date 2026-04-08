---
description: "Session start protocol — quick sync validation and context display"
globs:
alwaysApply: true
---

# Session Start Protocol

## .galdr/ Folder Layout (v3)

**SLIM layout** (galdr base — what g-skl-setup creates):
```
.galdr/
├── .identity             # project_id, project_name, user_id, user_name, galdr_version, vault_location
├── .gitignore
├── TASKS.md, PLAN.md, PROJECT.md, CONSTRAINTS.md, BUGS.md, SUBSYSTEMS.md, IDEA_BOARD.md, PRDS.md
├── prds/       # Individual PRD files
├── bugs/       # Individual bug detail files (optional; index in BUGS.md)
├── reports/
├── logs/
├── subsystems/ # Per-subsystem spec files (subsystem_name.md)
├── specifications_collection/  # Incoming specs, PRDs, wireframes from stakeholders (README.md index)
└── tasks/      # Individual task files (sequential task IDs)
```

**FULL layout additions** (galdr_full only — do NOT create in slim projects):
```
├── config/      # HEARTBEAT.md, SPRINT.md, AGENT_CONFIG.md
├── experiments/ # EXPERIMENTS.md, SELF_EVOLUTION.md, HYPOTHESIS.md, EXP-NNN.md
├── linking/     # README.md, INBOX.md — cross-project coordination
├── vault/       # encrypted/sensitive context
└── phases/      # Legacy v2 only — phase defs / archives
```

## Display at Session Start (when .galdr/ exists)
```
📌 SESSION CONTEXT
Mission: [from PROJECT.md, 1 line]
Goals: G-01: [name] | G-02: [name] (from PROJECT.md)
Plan focus: [current milestone or theme from PLAN.md]
Ideas: [N] active (from IDEA_BOARD.md)
Subsystems: [N] registered (from SUBSYSTEMS.md + subsystems/)
Specs: [N] in specifications_collection/ (newest: YYYY-MM-DD) [or "none"]
⚠️ Unreviewed: {spec_filename}  ← only if spec mtime > date of last [✅] task
🧠 Learned Facts: [N] project facts | [M] global facts  (run /g-learn review to see them)
Experiments: [summary from experiments/EXPERIMENTS.md if it has active entries]
🛡️ Constraints: [N] active — run @g-constraint-check before completing any task
```

Learned fact counts: count `-` bullet points in `.galdr/learned-facts.md` (skip headers and empties).
Global fact count: count bullets in `{vault_location}/projects/{project_name}/memory.md` if it exists.

## Subsystem Awareness (MANDATORY)
At session start, read `.galdr/SUBSYSTEMS.md` for the registry and interconnection graph.
For any subsystem you're about to modify, read its spec file at `.galdr/subsystems/{name}.md`.
This prevents architectural drift and ensures changes respect subsystem boundaries.

## Sync Validation (Run When User Mentions Tasks/Phases/Status)

**Step 0: Constraints Load**
- Read `.galdr/CONSTRAINTS.md`
- Count active constraints from the `## Constraint Index` table (Status = active)
- Display the LIST output from `g-skl-constraints` (compact one-liner per constraint)
- If any constraint definition block is missing the `**Enforcement**:` field → flag: `⚠️ C-{ID} has no enforcement definition`

**Step 1: Goals Check**
- PROJECT.md missing goals content or has `{Goal name}` placeholders → auto-generate from PROJECT.md mission / PLAN.md

**Step 2: Task Sync**
- Compare TASKS.md entries to `.galdr/tasks/` (v3 source of truth; sequential task IDs)
- Legacy v2: completed tasks may still be under `.galdr/phases/phase*/` until migrated
- Phantom = in TASKS.md but no matching `tasks/task{id}_*.md` (and not found in legacy archive if applicable)
- **Re-work Surface**: for each `[📋]`/pending task, check if its `## Status History` table has a FAIL row as the last entry (a row where the `To` column is `pending` and `Message` starts with `FAIL:`). If so, surface:
  ```
  ⚠️ Re-work: Task {id} previously failed verification on {Timestamp}: {Message}
  ```
  This alerts the implementing agent that prior attempts failed and what to watch for.

**Step 3: Plan / PRD / Legacy Phase Sync**
- Verify `.galdr/PLAN.md` and `.galdr/prds/` exist for delivery projects
- Legacy v2: if TASKS.md still has phase headers → check `phases/phaseN_*.md` exists until migrated off phases

**Step 4: SUBSYSTEMS.md Staleness**
- Collect `subsystems:` values from task files → compare to SUBSYSTEMS.md
- Missing entries → flag and offer to add stubs in `subsystems/`
- For each subsystem in SUBSYSTEMS.md, verify a spec file exists in `subsystems/`
- Spec files missing `locations:` in frontmatter → flag as incomplete

**Step 5: ACTIVE_BACKLOG.md**
- Older than 26 hours → flag as stale, offer regeneration

**Step 6: Cross-Project INBOX Check** (if `.galdr/linking/INBOX.md` exists)
- Read `.galdr/linking/INBOX.md`
- If any `[CONFLICT]` items exist → surface immediately as `⚠️ WARNING` before any other work
  - **Agent MUST acknowledge and resolve/defer CONFLICT items before proceeding** — conflicts gate all session work
  - Run `@g-pcac-read` to review and resolve; do not skip or defer conflicts silently
- Otherwise: count open items by type (requests/broadcasts/syncs) and note in session context
- Format: `INBOX: N open (N requests, N broadcasts, N syncs)` or `INBOX: clear`
- `g-hk-pcac-inbox-check.ps1` runs this check automatically at session start

**Step 7: Cascade Forward Check** (if `.galdr/PROJECT.md` **Project Linking** section lists children with cascade)
- Scan `.galdr/tasks/` for any task with `cascade_depth_remaining > 0` AND `cascade_forwarded: false`
- If found: forward cascades to children listed in topology (follow `g-broadcast` skill pattern but using the cascade chain metadata from the task)
- Mark forwarded tasks as `cascade_forwarded: true`
- Report: `Forwarded N cascade task(s) to: [child names]`
- If no children have `cascade_forward: true` or depth is 0: skip silently

**Step 8: Experiment Staleness Check** (if `.galdr/experiments/EXPERIMENTS.md` exists)
- Read EXPERIMENTS.md for active experiments
- For each active experiment: read EXP file, check if any stage is `[🔄]` for >48h without update
- Stale experiments → flag: `⚠️ EXP-NNN has a running stage with no update for >48h`
- Display active experiment summary: `EXP-NNN (Stage M/N — status)`

**Step 9: Documentation Staleness Check** (if vault is configured and `research/platforms/_index.yaml` exists)
- Read `.galdr/.identity` → get `vault_location`
- Read `{vault_location}/research/platforms/_index.yaml`
- Count entries where `next_refresh` field is earlier than today's date
- If any stale entries found → display: `📚 N documentation note(s) overdue for refresh — run @g-ingest-docs REFRESH_STALE`
- Skip silently if `_index.yaml` does not exist or vault is not configured

**Fix issues BEFORE proceeding with user request.**

## Idea Capture Triggers (IMMEDIATE, any time)
Capture to `IDEA_BOARD.md` when user says:
`"make a note"` | `"remember this"` | `"idea:"` | `"what if we"` | `"someday"` | `"for later"` | `"eventually"`
