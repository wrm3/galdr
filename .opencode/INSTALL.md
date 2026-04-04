# galdr — OpenCode Setup

## Quick Install

Clone the galdr repo into your project, or copy the relevant folders:

```bash
git clone https://github.com/wrm3/galdr.git .galdr-system
# Then copy .opencode/, .galdr/, AGENTS.md into your project root
```

Then tell OpenCode to run setup:

```
/g-setup
```

---

## What Gets Installed

galdr gives your OpenCode environment:
- **8 specialized subagents** — task management, QA, planning, code review, ideas, verification, infrastructure
- **24+ slash commands** — `/g-task-new`, `/g-plan`, `/g-code-review`, `/g-sprint`, and more
- **Skills** — loaded via `AGENTS.md` (OpenCode reads this natively)
- **`.galdr/` task system** — persistent file-based task tracking that survives sessions

---

## Manual Bootstrap

If `/g-setup` is not yet available, tell OpenCode:

```
I want to use the galdr task management system. Please:
1. Run /g-setup to initialize the .galdr/ folder structure
2. If /g-setup is unavailable, read AGENTS.md for project rules and conventions
3. Confirm setup complete with a session context summary.
```

---

## Key Conventions

- **Task files**: `.galdr/tasks/taskNNN_name.md` — always created before starting work
- **Task status**: `[ ]` pending  `[📋]` ready  `[🔄]` in-progress  `[🔍]` awaiting-verification  `[✅]` done
- **Bug files**: `.galdr/bugs/bugNNN_name.md` — logged via `/g-bug-report`
- **Never skip the file**: No task is complete without a task file in `.galdr/tasks/`
- **No phases**: galdr v3 uses sequential task IDs, not phase-based numbering

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/g-setup` | Initialize galdr in this project |
| `/g-task-new` | Create a new task |
| `/g-task-update` | Update task status |
| `/g-task-sync-check` | Validate task sync |
| `/g-plan` | Create or update project plan |
| `/g-sprint` | Run a 2-hour autonomous sprint |
| `/g-go` | Run backlog autonomously |
| `/g-code-review` | Code review |
| `/g-status` | Project status overview |
| `/g-bug-report` | Report a bug |
| `/g-bug-fix` | Document a bug fix |
| `/g-medkit` | Health check and repair `.galdr/` |
| `/g-git-commit` | Structured git commit |
| `/g-idea-capture` | Capture an idea |
| `/g-swot-review` | SWOT analysis |

Type `/` in OpenCode to see all available commands.

---

## Subagents

Use `@` to invoke specialized agents:

| Agent | Purpose |
|-------|---------|
| `@g-agnt-task-manager` | Task CRUD and sync |
| `@g-agnt-project` | PRD and project planning |
| `@g-agnt-qa-engineer` | Bug tracking |
| `@g-agnt-code-reviewer` | Code review |
| `@g-agnt-ideas-goals` | Idea capture and goals |
| `@g-agnt-infrastructure` | File organization, scope |
| `@g-agnt-verifier` | Task completion verification |
| `@g-agnt-project-initializer` | First-time galdr setup |

---

## Full Documentation

See `AGENTS.md` in the repo root and [github.com/wrm3/galdr](https://github.com/wrm3/galdr).
