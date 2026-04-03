# galdr — OpenCode Setup

## Quick Install

Tell OpenCode to fetch and follow these instructions:

```
Fetch and follow instructions from: https://raw.githubusercontent.com/wrm3/galdr/main/.opencode/INSTALL.md
```

## What Gets Installed

galdr gives your OpenCode environment:
- **9 specialized subagents** — task management, QA, planning, code review, ideas, verification
- **24 slash commands** — `/g-task-new`, `/g-plan`, `/g-review`, `/g-sprint`, and more
- **Skills** — auto-discovered from `.claude/skills/` (OpenCode reads these natively)
- **`.galdr/` task system** — persistent file-based task tracking that survives sessions

## Manual Bootstrap

If you prefer manual setup, tell OpenCode:

```
I want to use the galdr task management system. Please:
1. Create a .galdr/ folder with: TASKS.md, PLAN.md, BUGS.md, SUBSYSTEMS.md,
   project/ (PROJECT_CONTEXT.md, PROJECT_GOALS.md, PROJECT_CONSTRAINTS.md),
   tracking/ (IDEA_BOARD.md, INBOX.md), subsystems/, tasks/, phases/
2. Read AGENTS.md for project rules
3. Available commands start with /g- (e.g. /g-setup, /g-task-new, /g-plan)
4. Confirm setup complete with a session context summary.
```

## Key Conventions

- **Task files**: `.galdr/tasks/taskNNN_name.md` — always created before starting work
- **Task status**: `[ ]` pending  `[📋]` ready  `[🔄]` in-progress  `[✅]` done
- **Phase numbering**: Phase 0 = tasks 1-99, Phase 1 = tasks 100-199, etc.
- **Never skip the file**: No task is complete without a task file in `.galdr/tasks/`

## Available Commands

| Command | Description |
|---------|-------------|
| `/g-setup` | Initialize galdr in this project |
| `/g-task-new` | Create a new task |
| `/g-task-update` | Update task status |
| `/g-plan` | Create or update project plan |
| `/g-sprint` | Run a 2-hour autonomous sprint |
| `/g-review` | Code review |
| `/g-status` | Project status overview |
| `/g-bug-report` | Report a bug |
| `/g-cleanup` | Health check and sync fix |

Type `/` in OpenCode to see all 24 available commands.

## Subagents

Use `@` to invoke specialized agents:

| Agent | Purpose |
|-------|---------|
| `@g-task-manager` | Task CRUD and sync |
| `@g-planner` | PRD and phase planning |
| `@g-qa-engineer` | Bug tracking |
| `@g-code-reviewer` | Code review |
| `@g-ideas-goals` | Idea capture and goals |
| `@g-project-manager` | Galdr setup and grooming |
| `@g-verifier` | Task completion verification |

## Full Documentation

See `AGENTS.md` in the repo root and [github.com/wrm3/galdr](https://github.com/wrm3/galdr).
