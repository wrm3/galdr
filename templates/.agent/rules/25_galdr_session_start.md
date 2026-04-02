---
description: "Session start protocol — quick sync validation and context display"
globs:
alwaysApply: true
---

# Session Start Protocol

## .galdr/ Folder Layout (v2)
```
.galdr/
├── .project_id, .user_id, .vault_location   # Identity (root)
├── TASKS.md, PRD.md, SUBSYSTEMS.md           # Core files (root)
├── config/     # HEARTBEAT.md, SPRINT.md, KPI_DEFINITIONS.md, SWARM_STATUS.md, WAKEUP_QUEUE.md
├── project/    # PROJECT_CONTEXT.md, PROJECT_GOALS.md, PROJECT_TOPOLOGY.md, PROJECT_CONSTRAINTS.md
├── experiments/ # HYPOTHESIS.md, SYSTEM_EXPERIMENTS.md, EXPERIMENT_TEMPLATE.md
├── reports/    # CLEANUP_REPORT.md
├── tracking/   # BUGS.md, IDEA_BOARD.md, INBOX.md
├── subsystems/ # Per-subsystem spec files (subsystem_name.md)
├── tasks/      # Individual task files
├── phases/     # Phase definition files
├── contracts/, examples/, experiments/, reference/, templates/, vault/, logs/
```

## Display at Session Start (when .galdr/ exists)
```
📌 SESSION CONTEXT
Mission: [from project/PROJECT_CONTEXT.md, 1 line]
Goals: G-01: [name] | G-02: [name]
Phase: [current phase]
Ideas: [N] active (from tracking/IDEA_BOARD.md)
Subsystems: [N] registered (from SUBSYSTEMS.md + subsystems/)
```

## Subsystem Awareness (MANDATORY)
At session start, read `.galdr/SUBSYSTEMS.md` for the registry and interconnection graph.
For any subsystem you're about to modify, read its spec file at `.galdr/subsystems/{name}.md`.
This prevents architectural drift and ensures changes respect subsystem boundaries.

## Sync Validation (Run When User Mentions Tasks/Phases/Status)

**Step 1: Goals Check**
- No `project/PROJECT_GOALS.md` or has `{Goal name}` placeholders → auto-generate from `project/PROJECT_CONTEXT.md`

**Step 2: Task Sync**
- Compare TASKS.md entries to `.galdr/tasks/` AND `.galdr/phases/phase*/` files
- Active tasks ([📋][🔄][🔍]): look in tasks/ only
- Completed tasks ([✅]): look in tasks/ AND phases/phase*/
- Phantom = in TASKS.md but file not found in either location

**Step 3: Phase Sync**
- Every TASKS.md phase header → check `phases/phaseN_*.md` exists (definition file, not archive folder)

**Step 4: SUBSYSTEMS.md Staleness**
- Collect `subsystems:` values from task files → compare to SUBSYSTEMS.md
- Missing entries → flag and offer to add stubs in `subsystems/`
- For each subsystem in SUBSYSTEMS.md, verify a spec file exists in `subsystems/`
- Spec files missing `locations:` in frontmatter → flag as incomplete

**Step 5: ACTIVE_BACKLOG.md**
- Older than 26 hours → flag as stale, offer regeneration

**Step 6: Cross-Project INBOX Check** (if `.galdr/tracking/INBOX.md` exists)
- Read `.galdr/tracking/INBOX.md`
- If any `[CONFLICT]` items exist → surface immediately as `⚠️ WARNING` before any other work
- Otherwise: count open items by type (requests/broadcasts/syncs) and note in session context
- Format: `INBOX: N open (N requests, N broadcasts, N syncs)` or `INBOX: clear`

**Step 7: Cascade Forward Check** (if `.galdr/project/PROJECT_TOPOLOGY.md` has children declared)
- Scan `.galdr/tasks/` for any task with `cascade_depth_remaining > 0` AND `cascade_forwarded: false`
- If found: forward cascades to children listed in topology (follow `g-broadcast` skill pattern but using the cascade chain metadata from the task)
- Mark forwarded tasks as `cascade_forwarded: true`
- Report: `Forwarded N cascade task(s) to: [child names]`
- If no children have `cascade_forward: true` or depth is 0: skip silently

**Fix issues BEFORE proceeding with user request.**

## Idea Capture Triggers (IMMEDIATE, any time)
Capture to `tracking/IDEA_BOARD.md` when user says:
`"make a note"` | `"remember this"` | `"idea:"` | `"what if we"` | `"someday"` | `"for later"` | `"eventually"`
