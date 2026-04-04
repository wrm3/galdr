# GEMINI.md - {project_name}

> Gemini / Google Antigravity-specific context for this project.
> See `agents.md` for universal instructions shared across all IDEs.
> Run `@g-setup` to initialize galdr and auto-fill the placeholders below.

---

## Project Overview

**{project_name}** — {one sentence description}

---

## Gemini-Specific Configuration

### IDE Folders

```
.agent/
├── rules/       # Always-on rules (loaded automatically)
├── skills/      # Reusable skill packages
└── workflows/   # /slash-command automations
```

### Invoking Workflows

Use `/g-wkflw-name` syntax in Gemini for workflows, `/g-name` for commands:

| Workflow | Description |
|----------|-------------|
| `/g-wkflw-setup` | Initialize galdr |
| `/g-wkflw-status` | Project status overview |
| `/g-wkflw-task-new` | Create a new task |
| `/g-wkflw-task-update` | Update task status |
| `/g-wkflw-bug-report` | Report a bug |
| `/g-wkflw-code-review` | Code review |
| `/g-wkflw-plan` | Create or update project plan |
| `/g-wkflw-medkit` | Health check and repair `.galdr/` |
| `/g-wkflw-git-commit` | Structured git commits |
| `/g-wkflw-idea-capture` | Capture an idea |

See `docs/COMMANDS.md` for the full list. Workflows (`g-wkflw-`) live in `.agent/workflows/`; commands (`g-`) live in `.agent/commands/`.

---

## Gemini Agent Notes

### Mode Selection
- Use **Planning mode** for complex, multi-step tasks
- Use **Fast mode** for simple edits and renames
- Set Artifact Review Policy to "Request Review" for critical features

### Workflows
Workflows support `// turbo` for steps that should auto-execute without user approval. Use only for safe, idempotent operations.

### Rules
Rules in `.agent/rules/` are loaded automatically. Keep individual rule files under ~300 lines to avoid consuming excessive context.

### GUARDRAILS.md
Update `GUARDRAILS.md` when the agent encounters repeated failure patterns. This file accumulates learned constraints that prevent repeat mistakes.

### MCP Configuration
MCP servers are configured in `.mcp.json` at the project root.

```json
{
  "mcpServers": {
    "galdr": {
      "url": "http://localhost:8092/mcp"
    }
  }
}
```

---

## Task Management

### Direct Edit Policy
Edit these files directly without asking for permission:
- `.galdr/TASKS.md`, `.galdr/BUGS.md`, `.galdr/PLAN.md`, `.galdr/PROJECT.md`
- All files in `.galdr/tasks/`, `.galdr/bugs/`, `.galdr/prds/`

### Atomic Updates
Always update BOTH in the same response:
1. Task file YAML: `status: completed`
2. TASKS.md entry: `[🔄]` → `[✅]`

Never update one without the other.

---

## Security

- Never commit API keys, tokens, or passwords
- Use environment variables for secrets
- Always use parameterized queries

---

**galdr version**: 1.0.0
**Platform**: Gemini / Google Antigravity
**Universal instructions**: See `agents.md`
