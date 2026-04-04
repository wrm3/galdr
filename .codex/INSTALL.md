# galdr — Codex Setup

## Quick Install

Clone or copy the galdr system files into your project root, then tell Codex:

```
Read AGENTS.md and initialize the galdr task management system.
```

Codex reads `AGENTS.md` natively — that file contains all agent definitions, skills, conventions, and enforcement rules.

---

## What Gets Installed

galdr gives your Codex environment:
- **8 specialized agents** — task management, QA, verification, planning, code review, infrastructure, ideas
- **17 on-demand skills** — explicit workflows for common development tasks
- **`.galdr/` task system** — persistent file-based task tracking that survives sessions

---

## Manual Bootstrap

### Step 1: Create .galdr/ Task System

Tell Codex to run `/g-setup`, or if that's unavailable, ask it to create:

```
Create a .galdr/ folder with these files:
- TASKS.md (master task checklist)
- PLAN.md (product requirements and milestones)
- BUGS.md (bug tracking index)
- PROJECT.md (project mission and goals)
- CONSTRAINTS.md (non-negotiable architectural rules)
- SUBSYSTEMS.md (component registry)
- IDEA_BOARD.md (idea capture)
- tasks/ (individual task spec files)
- bugs/ (individual bug detail files)
- prds/ (PRD files)
- subsystems/ (per-subsystem spec files)
- linking/ (cross-project coordination)
- logs/ (agent audit and shell logs)
- reports/ (cleanup and health reports)
- config/ (sprint and heartbeat config)
```

### Step 2: Review .codex/config.toml

The `.codex/config.toml` in this repo is pre-configured. Verify it matches your environment:

```toml
model = "codex-1"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

### Step 3: Verify Setup

```
Read .galdr/TASKS.md and confirm the galdr system is active.
Display the session context summary.
```

---

## Key Conventions

- **Task files**: `.galdr/tasks/taskNNN_name.md` — always created before starting work
- **Task status**: `[ ]` pending → `[📋]` ready → `[🔄]` in-progress → `[🔍]` awaiting-verification → `[✅]` done
- **Bug files**: `.galdr/bugs/bugNNN_name.md` — logged via `g-bug-report`
- **Never skip the file**: No task is complete without a task file in `.galdr/tasks/`
- **No phases**: galdr v3 uses sequential task IDs, not phase-based numbering

---

## Enforcement Reminders for Codex

When working on tasks:
- Read `.galdr/TASKS.md` first to understand current state
- Create the task file BEFORE writing any code
- Update TASKS.md and task file atomically (both in same response)
- Offer a git commit after every task completion
- Any error or warning mentioned → log it in `.galdr/BUGS.md`
- Never read or write `.galdr/` files without following the galdr skill workflows

---

## Codex-Specific Notes

### Rules
Codex has no native rules folder. All galdr behavioral rules are delivered via `AGENTS.md` in the project root. Read it at session start.

### Skills
Skills are registered in `.codex/config.toml` under `[[skills.config]]` entries.
Each skill is a folder containing `SKILL.md` with workflow instructions.
galdr ships 17 core skills — see `.codex/skills/g-skl-*/SKILL.md`.

### Agents
Agent roles are defined in `.codex/config.toml` under `[agents]`.
Multi-agent support requires `features.multi_agent = true`.

### No Hooks
Codex does not support hooks. Session-start context comes from `AGENTS.md`.

---

## Full Documentation

See `AGENTS.md` in the repo root for the complete agent/skill reference.
See `README.md` for project overview and platform support details.
