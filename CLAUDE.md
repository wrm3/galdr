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
.galdr/        # Task management (TASKS.md, tasks/, bugs/, prds/)
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

**Commands** (use `/g-` prefix in Claude Code):
- `/g-status` — project overview
- `/g-task-new` — create a task
- `/g-bug-report` — report a bug
- `/g-medkit` — health check and repair
- `/g-code-review` — code review

See `docs/COMMANDS.md` for the full command list.

---

**galdr version**: 1.0.0
**Supported IDEs**: Cursor, Claude Code, Gemini, Codex, OpenCode
