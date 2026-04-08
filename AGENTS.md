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
├── prds/                # PRD files
└── specifications_collection/  # Incoming specs, PRDs, wireframes from stakeholders

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
| `g-agnt-pcac-coordinator` | Cross-project coordination — topology, inbox, broadcast, sync |

---

## Available Commands

Commands use `@g-` in Cursor, `/g-` in Claude Code.

### Core galdr Commands

| Command | Description |
|---------|-------------|
| `g-setup` | Initialize galdr in a project |
| `g-status` | Project status overview |
| `g-subsystems` | Subsystem registry sync check, add, update Activity Log |
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
| `g-go` | Run autonomously through the backlog (self-review mode — both phases) |
| `g-go-code` | Implementation-only run — marks tasks `[🔍]`, never `[✅]` |
| `g-go-verify` | Verification-only run — run in a **new agent session** from the coder |
| `g-harvest` | Harvest improvements from external sources |
| `g-vault-ingest` | Ingest or refresh vault knowledge |
| `g-vault-search` | Search the file-first vault |
| `g-vault-lint` | Lint vault structure and freshness |
| `g-vault-status` | Show vault status and recent activity |

### Cross-project coordination

| Command | Description |
|---------|-------------|
| `g-pcac-adopt` | Register a project as a **child** of this project (bidirectional topology update) |
| `g-pcac-ask` | Send a request to the parent project |
| `g-pcac-claim` | Register a project as the **parent** of this project (bidirectional topology update) |
| `g-pcac-move` | Transfer files/folders to another project in the topology |
| `g-pcac-order` | Push a task to child projects (with configurable cascade depth) |
| `g-pcac-read` | Review and action the cross-project INBOX (CONFLICTs first) |
| `g-pcac-status` | Show topology role, open INBOX items, linked project health |
| `g-pcac-sync` | Initiate or respond to sibling contract sync (advisory) |

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

## Vault Knowledge System

This template includes a file-first vault designed for Obsidian compatibility.

- Primary path: `.galdr/vault/`
- Optional shared override: `vault_location` in `.galdr/.identity`
- Optional raw repo mirror override: `repos_location` in `.galdr/.identity`
- Fallback behavior: if shared vault writes fail, write locally and log the event
- Raw GitHub repo mirrors belong in `repos_location`, not inside the Obsidian-indexed vault

Vault operations should use `g-skl-vault` and `g-skl-knowledge-refresh`.

- Read `VAULT_SCHEMA.md` before making structural vault changes
- Use `[[wikilinks]]` for durable internal references
- Keep curated repo notes in `research/github/`
- Rebuild `index.md` and `_index.yaml` after major vault updates

---

## Parity Model

This project is both a live galdr workspace and a source of installable framework files.

- Reusable framework content must preserve self-hosting parity between the live project and the shipped templates
- The parity target set is 10 IDE trees: `.cursor/`, `.claude/`, `.agent/`, `.codex/`, `.opencode/`, `templates/.cursor/`, `templates/.claude/`, `templates/.agent/`, `templates/.codex/`, `templates/.opencode/`
- Template install files also belong to the parity surface: `templates/.galdr/`, `templates/.galdr_template/`, `templates/AGENTS.md`, `templates/CLAUDE.md`, `templates/GEMINI.md`, `templates/.gitignore`
- Reusable changes flow both directions between root and `templates/`; local or proprietary workspace content stays out of `templates/`
- Root and template IDE trees must remain independent real copies, never symlinks or junctions
- Automated parity propagation is deferred until the canonical tree stabilizes; during the rebuild, parity is enforced manually

---

## Security

- Never commit API keys, tokens, or passwords
- Use environment variables for secrets (`.env`, never committed)
- Always use parameterized queries for database access
- Validate all user input

---

## galdr Version

**galdr version**: 1.1.0
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

### Stub/TODO Lifecycle (Zero Tolerance)
When writing any stub, placeholder, or TODO comment — **immediately**:
1. Format as `TODO[TASK-{original_id}→TASK-{follow_up_id}]: {description} — fix in follow-up task`
2. Create the follow-up task via `g-task-new` before moving to the next line
Bare `# TODO` or `pass` stubs that ship without a linked task are violations of `g-rl-34`.

### Bug Discovery (Zero-Ignore Policy)
When you encounter a bug during any coding or review session:
- Bug was introduced by **your current task's changes** → fix it inline before marking `[🔍]`
- Bug is **pre-existing** → create a BUG entry via `g-skl-bugs` REPORT, add `BUG[BUG-{id}]: {desc}` comment at the bug site, note it in the session summary. Never silently ignore a bug.
See `g-rl-35-bug-discovery-gate.mdc` for full decision tree and format examples.

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
