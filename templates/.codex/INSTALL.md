# galdr — Codex Installation

## Quick Install

Tell Codex to fetch and follow these instructions:

```
Fetch and follow instructions from: https://raw.githubusercontent.com/galdr/galdr/main/.codex/INSTALL.md
```

## What Gets Installed

galdr gives your Codex environment:
- **19 specialized agents** — task management, QA, verification, planning, code review
- **78 on-demand skills** — explicit workflows for common development tasks
- **`.galdr/` task system** — persistent file-based task tracking that survives sessions
- **MCP server integration** — RAG, Oracle, MediaWiki, video analysis, vault tools

## Automated Bootstrap (Preferred)

If the galdr MCP server is running, use:

```
Call the galdr_install MCP tool with the path to your project directory.
```

This creates all `.galdr/` files, `.codex/config.toml`, and registers skills automatically.

## Manual Bootstrap

### Step 1: Create .galdr/ Task System

```
Create a .galdr/ folder with these files:
- TASKS.md (master task checklist)
- PLAN.md (product requirements)
- BUGS.md (bug tracking)
- PROJECT_CONTEXT.md (project mission and goals)
- PROJECT_GOALS.md (strategic goals with metrics)
- SUBSYSTEMS.md (component registry)
- ARCHITECTURE_CONSTRAINTS.md (non-negotiable constraints)
- PROJECT_TOPOLOGY.md (cross-project relationships)
- INBOX.md (cross-project coordination queue)
- tasks/ (individual task files)
- phases/ (phase documentation)
- contracts/ (shared API contracts)
```

### Step 2: Create .codex/config.toml

Create `.codex/config.toml` in your project root:

```toml
#:schema https://developers.openai.com/codex/config-schema.json

model = "gpt-5-codex"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
model_reasoning_effort = "high"

[windows]
sandbox = "elevated"

[sandbox_workspace_write]
network_access = true

[features]
multi_agent = true
shell_tool = true

# MCP Server (if running galdr Docker)
[mcp_servers.galdr]
url = "http://localhost:8082/sse"
tool_timeout_sec = 600
enabled = true
```

### Step 3: Read AGENTS.md

Codex natively reads `AGENTS.md` from the project root. This file contains:
- All agent definitions and their responsibilities
- Available skills and commands
- Task management conventions
- Project structure documentation

### Step 4: Verify Setup

```
Read .galdr/TASKS.md and confirm the galdr system is active.
Display the session context summary.
```

## Key Conventions

- **Task files**: `.galdr/tasks/taskNNN_name.md` — always created before starting work
- **Task status**: `[ ]` pending -> `[📋]` ready -> `[🔄]` in-progress -> `[✅]` done
- **Phase numbering**: Phase 0 = tasks 1-99, Phase 1 = tasks 100-199, etc.
- **Never skip the file**: No task is complete without a task file in `.galdr/tasks/`

## Enforcement Reminders for Codex

When working on tasks:
- Read `.galdr/TASKS.md` first to understand current state
- Create the task file BEFORE writing any code
- Update TASKS.md and task file atomically (both in same response)
- Offer a git commit after every task completion
- Any error or warning mentioned -> log it in `.galdr/BUGS.md`
- Never read or write `.galdr/` files without following the galdr skill workflows

## Codex-Specific Notes

### Rules
Codex uses `.codex/rules/*.rules` (Starlark format) for command execution policies.
These are NOT the same as galdr's behavioral rules — galdr rules are delivered via AGENTS.md.

### Skills
Skills are registered in `.codex/config.toml` under `[[skills.config]]` entries.
Each skill is a folder containing `SKILL.md` with workflow instructions.

### Agents
Agent roles are defined in `.codex/config.toml` under `[agents]`.
Multi-agent support requires `features.multi_agent = true`.

### MCP
MCP servers are configured in `.codex/config.toml` under `[mcp_servers]` (TOML format).
the galdr MCP server provides RAG search, Oracle queries, vault operations, and more.

## Full Documentation

See `AGENTS.md` in the repo root for the complete agent/skill reference.
See `README.md` for project overview and platform support details.
