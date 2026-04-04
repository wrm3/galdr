# agents.md - {project_name}

> This file follows the agents.md format for AI agent instructions.
> Compatible with Cursor (`.cursor/`), Claude Code (`.claude/`), Gemini (`.agent/`), Codex (`.codex/`), and OpenCode (`.opencode/`).
> Run `@g-setup` to initialize galdr and auto-fill the placeholders below.

---

## Project Overview

**{project_name}** — {one sentence description of what this project does and who it's for}

**Tech Stack**: {e.g. Python / FastAPI / PostgreSQL}

---

## Project Structure

```
.galdr/                  # Task management data (shared across all IDEs)
├── TASKS.md             # Master task checklist
├── BUGS.md              # Bug index
├── PLAN.md              # Strategy and milestones
├── PROJECT.md           # Vision, mission, goals
├── CONSTRAINTS.md       # Architectural rules agents must follow
├── SUBSYSTEMS.md        # Component registry
├── tasks/               # Individual task spec files
├── bugs/                # Individual bug files
└── prds/                # PRD files

.cursor/                 # Cursor IDE configuration
├── agents/              # galdr system agents (g-agnt-*)
├── skills/              # Skills (g-skl-*)
├── commands/            # @g-* commands
├── hooks/               # PowerShell automation hooks
└── rules/               # Always-apply rules (g-rl-*)

.claude/                 # Claude Code (same content as .cursor/)
.agent/                  # Gemini / Antigravity
.codex/                  # Codex
.opencode/               # OpenCode
```

---

## galdr System Agents

| Agent | Description |
|-------|-------------|
| `g-agnt-task-manager` | Task lifecycle — create, update, track |
| `g-agnt-project` | Project init, grooming, planning, PRDs |
| `g-agnt-qa-engineer` | Bug tracking and quality assurance |
| `g-agnt-code-reviewer` | Code quality and security review |
| `g-agnt-infrastructure` | File organization, scope boundaries |
| `g-agnt-ideas-goals` | Idea capture and goal management |
| `g-agnt-verifier` | Verify completed task work |
| `g-agnt-project-initializer` | First-time project scaffolding |

---

## Available Commands

Commands use `@g-` in Cursor, `/g-` in Claude Code.

| Command | Description |
|---------|-------------|
| `g-setup` | Initialize galdr in a project |
| `g-status` | Project status overview |
| `g-task-new` | Create a new task |
| `g-task-update` | Update task status |
| `g-task-sync-check` | Validate task synchronization |
| `g-bug-report` | Report a bug |
| `g-bug-fix` | Document a bug fix |
| `g-code-review` | Code review (security, quality, performance) |
| `g-plan` | Create or update the project plan |
| `g-idea-capture` | Capture an idea to IDEA_BOARD.md |
| `g-idea-review` | Review and promote ideas |
| `g-medkit` | Health check, repair, or upgrade `.galdr/` |
| `g-dependency-graph` | Generate task dependency graph |
| `g-git-commit` | Create structured commit messages |
| `g-sprint` / `g-go` | Run an autonomous sprint |
| `g-broadcast` | Push task to child projects |
| `g-inbox` | Review cross-project coordination |
| `g-harvest` | Harvest improvements from external sources |

See `docs/COMMANDS.md` for the full list.

---

## Task Management

### Task Status Indicators

| TASKS.md | YAML status | Meaning |
|---------|-------------|---------|
| `[ ]` | (no file yet) | Pending — not started |
| `[📋]` | `pending` | Spec written, ready to start |
| `[🔄]` | `in-progress` | Being worked on (TTL: 2 hours) |
| `[🔍]` | `awaiting-verification` | Done, needs review |
| `[✅]` | `completed` | Done |
| `[❌]` | `failed` | Failed or cancelled |

### Direct Edit Policy

Edit these files directly without asking for permission:

- `.galdr/TASKS.md` — task checklist
- `.galdr/BUGS.md` — bug index
- `.galdr/PLAN.md` — project plan
- `.galdr/PROJECT.md` — project identity
- All files in `.galdr/tasks/`, `.galdr/bugs/`, `.galdr/prds/`

---

## Security

- Never commit API keys, tokens, or passwords
- Use environment variables for secrets (`.env`, never committed)
- Always use parameterized queries for database access
- Validate all user input

---

## galdr Version

**galdr version**: 1.0.0
**Supported IDEs**: Cursor, Claude Code, Gemini, Codex, OpenCode

---

## Enforcement Rules (All IDEs — including Codex)

These rules apply in every session, on every response. Codex enforces these via this AGENTS.md since it has no native rules folder.

### Error Reporting (Zero Tolerance)
If any response mentions "error", "warning", "lint error", "exception", or "pre-existing" — create a `.galdr/BUGS.md` entry immediately. There are no exemptions. Pre-existing errors must still be logged.

### Task Completion Gate
When marking a task `[✅]` completed: if the implementation contains any TODO, stub, `pass`, `NotImplementedError`, hardcoded mock data, or empty catch block — you MUST:
1. Annotate with `TODO[TASK-{original}→TASK-{followup}]: {what is stubbed}`
2. Create a follow-up task before marking complete

### Code Change Gate
If code files were modified and no task or bug is referenced — create a retroactive task via `g-task-new` before ending the response. Exceptions: `.galdr/` housekeeping, docs-only changes, git operations.

### Session Start Sync (v3)
At session start, display:
```
📌 SESSION CONTEXT
Mission: [from PROJECT.md]
Plan focus: [current milestone from PLAN.md]
Active tasks: [in-progress count from TASKS.md]
```

Read `.galdr/CONSTRAINTS.md` — load all constraints into active context. Constraints cannot be silently overridden.

### Commit Offer
After completing any task, always offer a git commit before ending the response.

### .galdr/ Folder Gate
Never read or write `.galdr/` files without following the appropriate skill workflow. Use `g-skl-tasks` for task operations, `g-skl-qa` for bugs, `g-skl-plan` for planning files.

### Documentation Placement
All `.md` documentation files go in `docs/` — never in the project root. Exceptions: `AGENTS.md`, `README.md`, `LICENSE`, `CLAUDE.md`, `CHANGELOG.md`, `GEMINI.md`, `GUARDRAILS.md`.

### PowerShell (Windows)
- Use `;` as command separator (NOT `&&`)
- Use `curl.exe` or `Invoke-WebRequest`, never bare `curl`
- Use `uv` for Python virtual environments, never bare `pip` or `python -m venv`
