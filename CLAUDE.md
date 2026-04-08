# CLAUDE.md - {project_name}

> Replace this file with your project's Claude Code instructions.
> Run `@g-setup` to initialize galdr and auto-fill the placeholders below.

---

## Project Overview

**{project_name}** — {one sentence description of what this project does}

## Tech Stack

- **Language**: {e.g. Python 3.11, TypeScript, Go}
- **Framework**: {e.g. FastAPI, Next.js, Django}
- **Database**: {e.g. PostgreSQL, SQLite, MySQL}
- **Package Manager**: {e.g. uv, npm, pip}

## Key Directories

```
.galdr/        # Task management — TASKS.md, tasks/, bugs/, prds/, subsystems/,
               #   specifications_collection/ (incoming specs/PRDs from stakeholders)
.claude/       # Claude Code configuration (rules, skills, agents, commands)
src/           # {main source folder}
docs/          # Documentation
```

## Development Commands

```bash
# {Add your project's setup/run commands here}
# e.g.:
# uv sync          # Install dependencies
# uv run dev       # Start dev server
# uv run test      # Run tests
```

## MCP Tools Available

{List MCP tools configured in .mcp.json — or delete this section if not using MCP}

## Security

- Never commit API keys, tokens, or passwords
- Use environment variables for secrets (.env, never committed)
- Always use parameterized queries for database access

## galdr Task Management

This project uses galdr for AI-assisted task tracking.

- **Tasks**: `.galdr/TASKS.md` (index) + `.galdr/tasks/` (individual specs)
- **Bugs**: `.galdr/BUGS.md` (index) + `.galdr/bugs/` (individual specs)
- **Plan**: `.galdr/PLAN.md`
- **Project context**: `.galdr/PROJECT.md`
- **Constraints**: `.galdr/CONSTRAINTS.md`
- **Incoming specs**: `.galdr/specifications_collection/` (PRDs, wireframes, contracts from stakeholders)

**Commands** (use `/g-` prefix in Claude Code):
- `/g-status` — project overview
- `/g-task-new` — create a task
- `/g-bug-report` — report a bug
- `/g-medkit` — health check and repair
- `/g-code-review` — code review
- `/g-vault-ingest` — ingest or refresh vault knowledge
- `/g-vault-search` — search the file-first vault
- `/g-vault-lint` — lint vault structure and freshness
- `/g-vault-status` — show vault status and recent activity

See `docs/COMMANDS.md` for the full command list.

## Vault Knowledge System

This template includes a file-first vault designed to work cleanly with Obsidian.

- Default vault path: `.galdr/vault/`
- Shared override: `vault_location` in `.galdr/.identity`
- Raw repo mirror override: `repos_location` in `.galdr/.identity`
- Raw mirrored repos never belong inside the Obsidian-indexed vault
- Curated repo notes belong in `research/github/`

When working with the vault:

- use `g-skl-vault` for ingest and search workflows
- use `g-skl-knowledge-refresh` for lint and freshness workflows
- read `VAULT_SCHEMA.md` before changing vault structure
- rebuild `index.md` and `_index.yaml` after major vault updates

## Parity Model

This project doubles as a live galdr workspace and a source of installable framework files.

- Preserve self-hosting parity between the live project and the shipped templates
- Treat these as the reusable IDE parity set: `.cursor/`, `.claude/`, `.agent/`, `.codex/`, `.opencode/`, `templates/.cursor/`, `templates/.claude/`, `templates/.agent/`, `templates/.codex/`, `templates/.opencode/`
- Include the install surface in parity reviews: `templates/.galdr/`, `templates/.galdr_template/`, `templates/AGENTS.md`, `templates/CLAUDE.md`, `templates/GEMINI.md`, `templates/.gitignore`
- Reusable framework changes must stay bidirectionally aligned between root and `templates/`
- Keep root and template trees as independent real copies, never junctions or symlinks
- Defer parity automation until the canonical tree is stable; enforce parity manually during the rebuild

---

## Enforcement Rules (All IDEs)

### Stub/TODO Lifecycle (Zero Tolerance)
When writing any stub, placeholder, or TODO comment — **immediately**:
1. Format as `TODO[TASK-{original_id}→TASK-{follow_up_id}]: {description} — fix in follow-up task`
2. Create the follow-up task via `/g-task-new` before moving to the next line
Bare `# TODO` or `pass` stubs that ship without a linked task are violations.

### Bug Discovery (Zero-Ignore Policy)
When you encounter a bug during any coding or review session:
- Bug introduced by **your current task's changes** → fix inline before marking `[🔍]`
- **Pre-existing bug** → create BUG entry via `/g-bug-report`, add `BUG[BUG-{id}]: {desc}` comment at the bug site, note in session summary. Never silently ignore a bug.

### Task Completion Gate
When marking a task `[✅]`: if implementation contains any TODO, stub, `pass`, `NotImplementedError`, or empty catch block — annotate with `TODO[TASK-{original}→TASK-{followup}]: {what is stubbed}` and create a follow-up task before marking complete.

### Code Change Gate
If code files were modified and no task or bug is referenced — create a retroactive task via `/g-task-new` before ending the response.

---

**galdr version**: 1.1.0
**Supported IDEs**: Cursor, Claude Code, Gemini, Codex, OpenCode
