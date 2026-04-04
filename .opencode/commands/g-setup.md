---
description: "Initialize the galdr v3 system in a new or existing project"
---

Initialize the galdr system: $ARGUMENTS

## What This Command Does

Initializes or reinitializes the galdr v3 task management system in the current project.
Activates the **g-skl-setup** skill which handles the full initialization workflow.

---

## Step 1: Project Type Selection (MANDATORY FIRST QUESTION)

**Ask the user:**

> "What type of project is this?
> 1. **delivery** — building a defined product with features and milestones
> 2. **research** — exploring unknown solutions, running experiments, testing hypotheses
>
> (Default: delivery)"

Set `Project Type` in `PROJECT.md` based on their answer. This affects:
- Whether `HYPOTHESIS.md` is created (research only)
- Whether sprint templates use milestone or experiment format

---

## Step 2: Create Directory Structure (v3 Layout)

Create these folders if they don't exist:
- `.galdr/` — Main working directory
- `.galdr/tasks/` — Individual task files (sequential IDs)
- `.galdr/prds/` — PRD files
- `.galdr/bugs/` — Individual bug detail files
- `.galdr/subsystems/` — Per-subsystem spec files
- `.galdr/logs/` — Evidence and audit logs
- `.galdr/reports/` — Cleanup and health reports
- `.galdr/linking/` — Cross-project contracts
- `docs/` — Project documentation
- `temp_scripts/` — Scratch scripts (gitignored)

**v3 does NOT use**: `phases/`, `tracking/`, `project/` subdirectories — these are legacy v2 paths.

---

## Step 3: Create Core Files (v3)

Create these template files:
- `.galdr/TASKS.md` — Master task checklist (sequential task IDs)
- `.galdr/PLAN.md` — Master strategy and PRD index
- `.galdr/PROJECT.md` — Mission, vision, goals, project linking
- `.galdr/CONSTRAINTS.md` — Non-negotiable architectural constraints
- `.galdr/BUGS.md` — Bug index (root level)
- `.galdr/SUBSYSTEMS.md` — Component registry with mermaid graph
- `.galdr/IDEA_BOARD.md` — Ideas parking lot
- `.galdr/.identity` — Project and user identity

**Research projects also get:**
- `.galdr/experiments/HYPOTHESIS.md` — Hypothesis tracker
- `.galdr/experiments/EXPERIMENTS.md` — Experiment index

---

## Step 4: Generate .identity

```
project_id={new-uuid}
project_name={project_name}
user_id={user_id_from_appdata_or_ask}
user_name={user_name}
galdr_version=1.0.0
vault_location={LOCAL}
```

---

## Step 5: Gather Architecture Constraints

Ask the user:
> "Are there any non-negotiable technical constraints? (e.g., database technology, deployment target, public API stability, cost limits)
> I'll document these in CONSTRAINTS.md so every agent session loads them automatically."

Add each constraint as a `C-NNN` entry in `.galdr/CONSTRAINTS.md`.

---

## Step 6: Scan Existing Codebase (if applicable)

For existing projects:
- Analyze current file structure
- Identify existing components/subsystems
- Create spec files in `.galdr/subsystems/`
- Populate SUBSYSTEMS.md with index and mermaid graph

---

## Task Status Indicators (v3)
- `[ ]` — Pending (no task file yet)
- `[📋]` — Ready (task file created, spec written)
- `[🔄]` — In Progress (claimed by agent, has TTL)
- `[🔍]` — Awaiting Verification (different agent required)
- `[✅]` — Completed (verified by different agent)
- `[❌]` — Failed/Cancelled
- `[⏸️]` — Paused

---

## When to Use
- Starting a new project
- Adding galdr to an existing project
- Reinitializing after major structural changes

Let me set up the galdr v3 system for you!
