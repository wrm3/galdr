# galdr Commands Reference

Commands use the `@g-` prefix in Cursor, `/g-` in Claude Code, OpenCode, and Gemini.

All commands are thin wrappers — they activate the underlying skill. See `docs/SKILLS.md` for the full skill reference.

---

## Task Management

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-task-new` | `g-skl-tasks` → CREATE TASK | Create a new task with spec |
| `g-task-update` | `g-skl-tasks` → UPDATE STATUS | Update task status |
| `g-task-sync-check` | `g-skl-tasks` → SYNC CHECK | Validate task synchronization |
| `g-workflow` | `g-skl-tasks` → EXPAND / SPRINT PLAN | Task expansion and sprint planning |
| `g-status` | `g-skl-status` | Project status overview |

---

## Bugs & Quality

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-bug-report` | `g-skl-bugs` → REPORT BUG | Report / document a bug |
| `g-bug-fix` | `g-skl-bugs` → FIX BUG | Document a bug fix |
| `g-qa` | `g-skl-bugs` → QUALITY REPORT | Quality assurance activation |
| `g-code-review` | `g-skl-code-review` | Comprehensive code review |

---

## Planning

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-plan` | `g-skl-plan` → CREATE / UPDATE PLAN | Create or update project plan |
| `g-goal-update` | `g-skl-project` → UPDATE PROJECT.MD | Create or update project goals |

---

## Ideas & Knowledge

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-idea-capture` | `g-skl-ideas` → CAPTURE | Capture an idea to IDEA_BOARD.md |
| `g-idea-review` | `g-skl-ideas` → REVIEW | Review and evaluate ideas |
| `g-idea-farm` | `g-skl-ideas` → FARM | Proactive codebase scan for ideas |
| `g-harvest` | `g-skl-harvest` | Harvest ideas from external sources |

---

## Project Health

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-medic` | `g-skl-medic` | Health check, repair, or upgrade `.galdr/` |
| `g-setup` | `g-skl-setup` | Initialize galdr in a project |
| `g-report` | `g-skl-report` | Generate a project health report |
| `g-swot-review` | `g-skl-swot-review` | Run SWOT analysis on the project |

> **Deprecated** (now route to `g-medkit`):
> - `@g-cleanup` → use `@g-medic` instead
> - `@g-grooming` → use `@g-medic` instead

---

## Cross-Project

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-inbox` | `g-skl-inbox` | Review cross-project coordination items |
| `g-broadcast` | `g-skl-broadcast` | Push tasks to child projects |
| `g-peer-sync` | `g-skl-peer-sync` | Sync contracts with sibling projects |
| `g-graph` | `g-skl-graph` | Display project ecosystem graph |

---

## Utilities

| Command | Activates Skill | Description |
|---------|----------------|-------------|
| `g-git-commit` | `g-skl-git-commit` | Create well-structured commits |
| `g-go` | `g-skl-tasks` → AUTONOMOUS RUN | Work through the task backlog autonomously |
| `g-review` | **Deprecated** → use `g-code-review` | (redirects to g-skl-code-review) |

---

## Usage Notes

- **Cursor**: `@g-task-new`, `@g-medic`, `@g-status`
- **Claude Code**: `/g-task-new`, `/g-medic`, `/g-status`
- **OpenCode**: `/g-task-new`, `/g-medic`, `/g-status`
- **Gemini (.agent/workflows/)**: `/g-task-new`, `/g-medic`, `/g-status`

All platforms use the same `g-` command names. In Gemini, commands are backed by workflow files in `.agent/workflows/` rather than `.agent/commands/`, but the user-facing slash invocation is identical.
