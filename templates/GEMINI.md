# GEMINI.md - galdr

## Project Overview

galdr is a comprehensive AI-powered task management and development system. This file provides Google Antigravity-specific context. See `agents.md` for universal instructions.

## Tech Stack

- **Rules**: `.agent/rules/*.md` — standard Markdown with YAML frontmatter
- **Skills**: `.agent/skills/*/SKILL.md` — reusable knowledge modules
- **Workflows**: `.agent/workflows/*.md` — slash-command automations (`/workflow-name`)
- **Task Files**: `.galdr/tasks/*.md` — Markdown with YAML frontmatter
- **MCP Server**: Python with FastMCP, PostgreSQL/pgvector for RAG
- **Package Management**: UV for Python

## Key Directories

```
.agent/           # Antigravity IDE configuration
├── rules/        # Always-on and glob-activated rules
├── skills/       # Reusable skill packages
└── workflows/    # /slash-command automations

.galdr/           # Task management data (portable across all IDEs)
├── TASKS.md      # Master task checklist (source of truth)
├── PLAN.md       # Product Requirements Document
├── tasks/        # Individual task files
└── phases/       # Phase documentation

docker/           # MCP server (Docker)
├── galdr/        # Main server code
└── docker-compose.yml
```

## Available Workflows

Invoke these with `/workflow-name` in the Antigravity agent:

| Workflow | Description |
|----------|-------------|
| `/g-setup` | Initialize galdr system |
| `/g-status` | Project status overview |
| `/g-task-new` | Create a new task |
| `/g-task-update` | Update task status |
| `/g-plan` | Create PRD and project planning |
| `/g-review` | Comprehensive code review |
| `/g-git-commit` | Create well-structured commits |
| `/g-bug-report` | Report/document a bug |
| `/g-phase-add` | Add new project phase |

## Antigravity-Specific Notes

### Agent Mode

- Use **Planning mode** for complex tasks (enables Artifacts)
- Use **Fast mode** for simple edits and renames
- Set Artifact Review Policy to "Request Review" for critical features

### Workflows

Workflows support `// turbo` for steps that should auto-execute without approval. Use for safe, idempotent operations only.

### Skills

Skills in `.agent/skills/` are loaded on relevance. Reference heavy documentation via `@filename` in rules to stay under the 12,000 character rule limit.

### GUARDRAILS.md

Update `GUARDRAILS.md` when the agent encounters repeated failure patterns. This file accumulates learned constraints.

### MCP Configuration

MCP servers are configured in `mcp_config.json` at the project root. See `docker/docker-compose.yml` for available MCP services.

```json
{
  "mcpServers": {
    "galdr_docker": {
      "url": "http://localhost:8765/sse"
    }
  }
}
```

## CRITICAL: Task Management Rules

<!-- galdr system CONTEXT -->
### Direct Edit Policy

Edit these files directly without asking for permission:
- `.galdr/PLAN.md`, `.galdr/TASKS.md`, `.galdr/BUGS.md`
- `.galdr/PROJECT_CONTEXT.md`, `.galdr/SUBSYSTEMS.md`
- All files in `.galdr/tasks/` and `.galdr/phases/`

### Task Status Indicators

- `[ ]` — Pending (no task file) — **BLOCKED**
- `[📝]` — Speccing (agent writing spec, TTL: 1 hour)
- `[📋]` — Ready (file created) — **CAN PROCEED**
- `[🔄]` — In Progress (TTL: 2 hours)
- `[✅]` — Completed
- `[❌]` — Failed/Cancelled
- `[⏸️]` — Paused

### Atomic Updates

Always update BOTH files in the same response:
1. Task file YAML: `status: completed`
2. TASKS.md entry: `[🔄]` → `[✅]`

Never update one without the other.
<!-- END galdr system CONTEXT -->

---

## Security

- Never commit API keys, tokens, or passwords
- Oracle credentials passed per-query (not stored)
- Use environment variables for secrets
- Always use parameterized queries

---

**Version**: 1.0.0
**Last Updated**: 2026-02-19
**Platform**: Google Antigravity IDE
**Universal Instructions**: See `agents.md`
