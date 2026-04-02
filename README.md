<p align="center">
  <img src="logo/Galdr_Logo_Big.jpg" alt="galdr banner" width="800">
</p>

<p align="center">
  <strong>Song magic for your codebase.</strong> An AI-powered development system that gives your coding agents structured memory, task management, and specialized skills across every major AI IDE.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="docker/docker-compose.yml"><img src="https://img.shields.io/badge/docker-compose-blue.svg" alt="Docker"></a>
  <a href="https://github.com/wrm3/galdr"><img src="https://img.shields.io/github/stars/wrm3/galdr?style=social" alt="GitHub stars"></a>
</p>
---

## Why galdr?

AI coding agents are powerful but forgetful. Every new chat starts from zero -- no memory of your preferences, no awareness of your project's architecture, no record of what was tried before. You end up repeating yourself, re-explaining constraints, and watching agents make the same mistakes across sessions.

**galdr fixes this.** It's a file-based framework that wraps around your AI IDE and gives agents:

- **Persistent memory** that survives across sessions and machines
- **Task tracking** so agents know what's been done, what's in progress, and what's next
- **Architectural constraints** that agents must follow (and can't silently ignore)
- **A knowledge vault** for cross-project research, decisions, and learned facts
- **Specialized skills** so agents know *how* to do things like code review, sprint planning, or video analysis -- not just that they should

It works with **Cursor, Claude Code, Gemini, Codex, and OpenCode** simultaneously. Same skills, same agents, same task data -- regardless of which IDE you open.

## What's Included

| Component | Count | Examples |
|-----------|-------|---------|
| **Agents** | 41 | Task manager, code reviewer, QA engineer, planner, sprint runner, memory manager, infrastructure, workflow, multi-agent orchestrator |
| **Skills** | 83 | Task management, code review, video production, 3D optimization, database standards, patent filing, startup ops, Kubernetes, CI/CD, web3, manim animation |
| **Commands** | 39 | `@g-task-new`, `@g-review`, `@g-plan`, `@g-sprint`, `@g-harvest`, `@g-vault-search`, `@g-platform-crawl`, `@g-status` |
| **MCP Tools** | 42 | RAG search, Oracle SQL, MediaWiki, vault indexing, session memory, video analysis, platform crawling, server-side crawl, custom crawl targets, web UI URLs, health reports |
| **Hooks** | 12 | Session start, agent complete, vault sync, log sanitization, shell validation, platform doc enrichment |
| **Rules** | 9 | Always-apply rules for documentation, git workflow, error reporting, task completion gates |
| **IDE Platforms** | 5 | Cursor, Claude Code, Gemini, Codex, OpenCode |

## How It Works

```
Your Project/
├── .galdr/                  # Task management (per-project, gitignored)
│   ├── TASKS.md             # Master task checklist
│   ├── PRD.md               # Product Requirements Document
│   ├── SUBSYSTEMS.md        # Component registry + interconnection diagram
│   ├── config/              # HEARTBEAT.md, SPRINT.md, KPI_DEFINITIONS.md
│   ├── project/             # PROJECT_CONTEXT.md, PROJECT_CONSTRAINTS.md, PROJECT_GOALS.md
│   ├── experiments/         # HYPOTHESIS.md, SYSTEM_EXPERIMENTS.md
│   ├── reports/             # CLEANUP_REPORT.md
│   ├── tracking/            # BUGS.md, IDEA_BOARD.md, INBOX.md
│   ├── subsystems/          # Per-subsystem spec files
│   ├── tasks/               # Individual task specs (YAML + markdown)
│   └── phases/              # Phase documentation and archives
│
├── .cursor/                 # Cursor IDE configuration
│   ├── agents/              # 41 specialized agent definitions
│   ├── skills/              # 83 skill files with workflows and knowledge
│   ├── commands/            # 39 @g-* commands
│   ├── hooks/               # 12 automation hooks (PowerShell)
│   └── rules/               # 9 always-apply rules
│
├── .claude/                 # Claude Code (identical to .cursor/)
├── .agent/                  # Gemini (identical, adapted format)
├── .codex/                  # Codex (skills subset)
├── .opencode/               # OpenCode (minimal)
│
├── AGENTS.md                # Learned workspace facts (read by all IDEs)
└── CLAUDE.md                # Claude-specific context + same facts
```

When you open your project in any supported IDE, the agents automatically have access to your tasks, constraints, memory, and skills. No configuration needed beyond the initial install.

## Quick Start

### Option A: Install via MCP Tool

If someone in your team already runs the galdr Docker server:

1. Add the MCP server URL to your IDE config (`.cursor/mcp.json` or `.claude/settings.local.json`)
2. Ask your agent: *"Run galdr_install on this project"*
3. Done. Your project now has `.galdr/`, agents, skills, commands, and hooks.

### Option B: Clone and Deploy

```bash
git clone https://github.com/wrm3/galdr.git
cd galdr
cp .env.example .env          # Edit with your API keys
cd docker && docker compose up -d
```

Then use the `galdr_install` MCP tool to deploy the framework into any project.

### Option C: Symlink Mode (Power Users)

Clone once, symlink into every project:

```bash
git clone https://github.com/wrm3/galdr.git ~/galdr
cd ~/galdr && cd docker && docker compose up -d

# In your project directory:
ln -s ~/galdr/templates/.cursor .cursor
ln -s ~/galdr/templates/.claude .claude
ln -s ~/galdr/templates/.agent .agent
cp -r ~/galdr/templates/.galdr .galdr    # Copy, don't link (project-specific data)
```

On Windows, use `mklink /J` for junction links instead of `ln -s`.

## Key Features

### Task Management

Create tasks with structured specs, track status across phases, and let agents pick up where you (or they) left off.

```
@g-task-new "Add user authentication with JWT"
@g-status
@g-sprint          # Agent autonomously works through the backlog
```

Tasks use YAML frontmatter for metadata (priority, dependencies, subsystems) and markdown for specs and acceptance criteria. Status syncs between individual task files and the master `TASKS.md` checklist.

### Knowledge Vault

A file-based knowledge store that persists across sessions, projects, and machines.

- **Session summaries** captured automatically after each conversation
- **Research notes** from web crawls, video analysis, and deep dives
- **Architectural decisions** extracted from conversations via continual learning
- **Platform documentation** crawled and indexed for offline reference

Vault notes use standardized YAML frontmatter for indexing and freshness tracking. Projects can share a vault (team knowledge) or keep one isolated (client work).

### Code Review

Not a linter -- a structured review covering security, performance, maintainability, and architectural alignment.

```
@g-review src/auth/
```

Generates a severity-classified report with specific file/line references and actionable recommendations.

### Architectural Constraints

Define rules that agents **cannot** silently ignore. Constraints are loaded at every session start and enforced across all agent interactions.

```markdown
### C-004: UV for Python Virtual Environments
**Non-negotiable**: yes
**What this means**: Use `uv venv`, `uv pip install`, `uv run`. Never bare `pip` or `python -m venv`.
```

If an agent's action would violate a constraint, it must flag the conflict and get explicit approval before proceeding.

### Cross-Project Topology

Projects can declare parent/child/sibling relationships. Parents can broadcast tasks to children. Children can request actions from parents. Siblings can sync shared contracts.

```
@g-topology                    # View project graph
@g-broadcast "Update API v2"   # Push task to child projects
@g-request "Need auth service" # Request from parent
```

### Platform Documentation Crawling

Automated crawling of IDE and platform docs using crawl4ai (free, open-source). Keeps your agents current on Cursor, Claude Code, Gemini, and other platform APIs.

```
@g-platform-crawl --target cursor
@g-knowledge-refresh           # Check what's stale
```

Crawling can run locally (personal use) or server-side (team sharing). Custom targets let you crawl internal docs (Confluence, company wikis) — one person crawls, everyone benefits.

### WebSocket Sync & Web UI

For team deployments, galdr syncs `.galdr/` files and vault content to the server via WebSocket. This enables:

- **Task dashboards** at `/projects/{project_id}/tasks` — view task status in a browser
- **Session history** at `/users/{user_id}/sessions` — review past agent conversations
- **Cross-machine vault sync** — research and crawled docs propagate across your machines
- **Server-side crawling** — Docker runs crawl4ai and broadcasts results to all connected clients

```
# Agent returns the URL instead of dumping data into the chat
get_project_url(project_id="abc-123", page="tasks")
```

### Continual Learning

Agents automatically extract durable facts from conversation transcripts and persist them in `AGENTS.md`. This means agents remember your preferences, project conventions, and past decisions across sessions — without you repeating yourself.

### User Identity & Memory Segregation

Each user gets a unique `user_id` stored on their machine. All memory queries (sessions, captures, search) are filtered by `user_id`, ensuring privacy in shared server deployments. Multiple machines share the same identity.

## MCP Server

The Docker-based MCP server provides tools that require infrastructure (database, embeddings, external APIs):

| Category | Tools |
|----------|-------|
| **Memory** | `memory_search`, `memory_capture_session`, `memory_context`, `memory_ingest_session`, `memory_sessions`, `memory_capture_insight`, `memory_search_combined`, `memory_setup_user` |
| **Vault** | `vault_search`, `vault_search_all`, `vault_sync`, `vault_read`, `vault_list`, `vault_export_sessions` |
| **Install** | `galdr_install`, `galdr_plan_reset`, `galdr_health_report`, `galdr_validate_task`, `galdr_server_status` |
| **Crawling** | `platform_docs_search`, `platform_crawl_trigger`, `platform_crawl_status`, `crawl_add_target`, `crawl_list_targets`, `crawl_remove_target`, `check_crawl_freshness`, `update_crawl_registry` |
| **Oracle** | `oracle_query`, `oracle_execute` |
| **MediaWiki** | `mediawiki_page`, `mediawiki_search` |
| **Video** | `video_analyze`, `video_batch_process`, `video_extract_frames`, `video_extract_transcript`, `video_extract_metadata`, `video_get_playlist`, `video_check_new` |
| **Web UI** | `get_project_url`, `get_service_url` |
| **Utility** | `md_to_html`, `config_reload` |

### Docker Services

| Service | Port | Profile | Description |
|---------|------|---------|-------------|
| galdr (MCP) | 8092 | default | Main MCP server (streamable-http) |
| PostgreSQL | 5433 | default | RAG database with pgvector |
| pgAdmin | 8083 | `admin` | Database management UI |
| MediaWiki | 8880 | `mediawiki` | Private knowledge base |

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required for Docker
POSTGRES_DB=rag_knowledge
POSTGRES_USER=galdr
POSTGRES_PASSWORD=your_password_here

# API Keys (for embeddings and research tools)
OPENAI_API_KEY=your-key-here

# Task visualizer — set to your local clone path
GALDR_PROJECT_HOST_PATH=/path/to/your/galdr
```

### Vault Configuration

Edit `.galdr/.vault_location` to control where knowledge is stored:

```
{LOCAL}              # Default: .galdr/vault/ inside the project
/path/to/shared      # Shared vault: all projects share knowledge
```

## Design Principles

1. **File-first** -- Every feature works without Docker or MCP. Agents read/write `.galdr/` files directly. MCP tools enhance but never gate functionality.
2. **Platform parity** -- Skills, agents, commands, and hooks are identical across all 5 supported IDEs. Change one, propagate to all.
3. **Constraints over conventions** -- Architectural rules are enforced, not suggested. Agents must flag violations, not silently work around them.
4. **Memory is durable** -- Session history, learned facts, and research survive across conversations, machines, and IDE switches.
5. **Single source of truth** -- Task status lives in files, not in agent memory. Two agents opening the same project see the same state.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)

---

**galdr** -- *Norse for "song magic." Because the best code is indistinguishable from incantation.*
