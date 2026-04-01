# galdr — OpenCode Installation

## Quick Install

Tell OpenCode to fetch and follow these instructions:

```
Fetch and follow instructions from: https://raw.githubusercontent.com/galdr/galdr/main/.opencode/INSTALL.md
```

## What Gets Installed

galdr gives your OpenCode environment:
- **19 specialized agents** — task management, QA, verification, planning, code review
- **25 on-demand skills** — explicit workflows for common development tasks
- **`.galdr/` task system** — persistent file-based task tracking that survives sessions

## Manual Bootstrap

If you prefer manual setup, tell OpenCode:

```
I want to use the galdr task management system. Please:
1. Create a .galdr/ folder with: TASKS.md, PLAN.md, BUGS.md, PROJECT_CONTEXT.md, SUBSYSTEMS.md, tasks/, phases/
2. Read the agent definitions from: https://github.com/galdr/galdr/tree/main/.claude/agents/
3. Read the skill definitions from: https://github.com/galdr/galdr/tree/main/.claude/skills/
4. Apply the rules from: https://github.com/galdr/galdr/tree/main/.claude/rules/
5. Confirm setup complete with a session context summary.
```

## Key Conventions

- **Task files**: `.galdr/tasks/taskNNN_name.md` — always created before starting work
- **Task status**: `[ ]` pending → `[📋]` ready → `[🔄]` in-progress → `[✅]` done
- **Phase numbering**: Phase 0 = tasks 1-99, Phase 1 = tasks 100-199, etc.
- **Never skip the file**: No task is complete without a task file in `.galdr/tasks/`

## Enforcement Reminders for OpenCode

When working on tasks:
- Read `.galdr/TASKS.md` first to understand current state
- Create the task file BEFORE writing any code
- Update TASKS.md and task file atomically (both in same response)
- Offer a git commit after every task completion
- Any error or warning mentioned → log it in `.galdr/tracking/BUGS.md`

## Full Documentation

See `README.md` in the repo root for the complete agent/skill reference.
