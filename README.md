# galdr

> AI task management for any IDE — file-based, no backend required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/wrm3/galdr?style=social)](https://github.com/wrm3/galdr)

## What Is galdr?

galdr gives your AI agent structured task management, project planning, and code review — working identically across **Cursor**, **Claude Code**, **Gemini**, **Codex**, and **OpenCode** using only markdown files.

No Docker. No servers. No credentials. Just clone and go.

```
clone → copy templates/ into your project → start working
```

## What You Get

| Feature | Description |
|---------|-------------|
| Task management | Create, track, and complete tasks with phase-based numbering |
| Project planning | PRDs, phases, goals, constraints |
| Code review | Structured review with severity ratings |
| Bug tracking | BUGS.md with severity classification |
| Idea board | Capture ideas without derailing work |
| Multi-IDE parity | Same workflow in Cursor, Claude Code, Gemini, Codex, OpenCode |
| Cross-project linking | Parent/child/sibling project coordination |

## Quick Start

```bash
# Option 1: Install via galdr_install (if you have the MCP server)
# Call galdr_install MCP tool in your IDE

# Option 2: Manual install
git clone https://github.com/wrm3/galdr.git galdr_tmp
cp -r galdr_tmp/templates/.cursor     your-project/
cp -r galdr_tmp/templates/.claude     your-project/
cp -r galdr_tmp/templates/.galdr      your-project/
cp -r galdr_tmp/templates/AGENTS.md  your-project/
rm -rf galdr_tmp
```

Then open your project in your AI IDE and type `@g-setup` (Cursor) or `/g-setup` (Claude Code).

## File Structure

```
your-project/
├── .cursor/          # Cursor IDE config (skills, agents, rules, commands, hooks)
├── .claude/          # Claude Code config (same content, .md format)
├── .agent/           # Gemini config
├── .codex/           # OpenAI Codex config
├── .opencode/        # OpenCode config
└── .galdr/           # Task management (TASKS.md, tasks/, phases/, etc.)
```

## Core Commands

| Cursor | Claude Code | Description |
|--------|-------------|-------------|
| `@g-setup` | `/g-setup` | Initialize galdr in a project |
| `@g-task-new` | `/g-task-new` | Create a new task |
| `@g-status` | `/g-status` | Project status overview |
| `@g-plan` | `/g-plan` | Create/update PRD |
| `@g-review` | `/g-review` | Code review |
| `@g-qa` | `/g-qa` | Bug tracking |
| `@g-sprint` | `/g-sprint` | Autonomous 2-hour sprint |

## Ecosystem Add-ons

galdr is the lightweight base. Add more when you need it:

| Repo | Description |
|------|-------------|
| [galdr_full](https://github.com/wrm3/galdr_full) | Full skill set — 90+ skills including AI/ML, video, startup, 3D |
| [galdr_mcp](https://github.com/wrm3/galdr_mcp) | Docker MCP backend — memory, RAG, vault, file search |
| galdr_forge | Private dev workspace (unreleased features) |

## License

MIT — see [LICENSE](LICENSE)
