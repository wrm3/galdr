<p align="center">
  <img src="logo/Galdr_Logo_Big.jpg" alt="galdr banner" width="800">
</p>

<p align="center">
  <strong>Song magic for your codebase.</strong> An AI-powered development system that gives your coding agents structured memory, task management, and specialized skills across every major AI IDE.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.1.0-green.svg" alt="Version"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://github.com/wrm3/galdr/releases"><img src="https://img.shields.io/github/v/release/wrm3/galdr?label=release" alt="Latest Release"></a>
  <a href="https://github.com/wrm3/galdr"><img src="https://img.shields.io/github/stars/wrm3/galdr?style=social" alt="GitHub stars"></a>
</p>

---

## Why galdr?

AI coding agents are powerful — but they forget everything the moment you close the chat. No memory of the architectural decision you made last Tuesday. No awareness of the constraint you established in session 3. No record that the same bug appeared and was solved twice before. You end up repeating yourself, re-explaining your project structure, and watching agents confidently make mistakes that were already documented.

**galdr fixes this.** It wraps around your AI IDE and gives agents:

- **Persistent memory** — decisions, constraints, and learned facts that survive across sessions and machines
- **Task tracking** — agents know what has been done, what is in progress, and what comes next
- **Architectural constraints** — rules agents must respect and cannot silently ignore
- **A knowledge vault** — research, session summaries, and platform docs indexed for offline retrieval
- **Specialized skills** — agents know *how* to do things like code review, sprint planning, and vault ingestion, not just that they should

It works with **Cursor, Claude Code, Gemini, Codex, and OpenCode** simultaneously. Same tasks, same constraints, same memory — regardless of which IDE you open.

## What's Included

| Component | Count | Examples |
|-----------|-------|---------|
| **Agents** | 9 | Task manager, code reviewer, QA engineer, project planner, infrastructure, ideas, verifier, project initializer, PCAC coordinator |
| **Skills** | 39 | Tasks, bugs, plan, project, subsystems, vault, code review, medkit, constraints, git, harvest, crawl, ingest-docs, ingest-url, ingest-youtube, learn, and more |
| **Commands** | 52 | `@g-task-new`, `@g-go-code`, `@g-go-verify`, `@g-plan`, `@g-medkit`, `@g-status`, `@g-bug-report`, `@g-git-commit` |
| **MCP Tools** | 42 | RAG search, Oracle SQL, MediaWiki, vault indexing, session memory, video analysis, platform crawling, health reports |
| **Hooks** | 12 | Session start, agent complete, pre-commit, pre-push, user setup, shell validation |
| **Rules** | 12 | Always-apply: documentation standards, git workflow, error reporting, task completion gates, TODO lifecycle |
| **IDE Platforms** | 5 | Cursor, Claude Code, Gemini, Codex, OpenCode |

## How It Works

```
your-project/
├── .galdr/                  # Task management (shared across all IDEs)
│   ├── TASKS.md             # Master task checklist
│   ├── BUGS.md              # Bug index
│   ├── PLAN.md              # Strategy and milestones
│   ├── PROJECT.md           # Vision, mission, goals (plain language)
│   ├── CONSTRAINTS.md       # Architectural rules agents must follow
│   ├── SUBSYSTEMS.md        # Component registry
│   ├── tasks/               # Individual task specs (YAML + markdown)
│   ├── bugs/                # Individual bug files
│   └── prds/                # PRD files
│
├── .cursor/                 # Cursor IDE configuration
│   ├── agents/              # 9 galdr system agents
│   ├── skills/              # 39 skills (g-skl-*)
│   ├── commands/            # 52 @g-* commands
│   ├── hooks/               # 12 automation hooks (PowerShell)
│   └── rules/               # 12 always-apply rules (g-rl-*)
│
├── .claude/                 # Claude Code (identical to .cursor/)
├── .agent/                  # Gemini (identical, adapted format)
├── .codex/                  # Codex (skills subset)
├── .opencode/               # OpenCode (agents + commands)
│
├── AGENTS.md                # Project context (read by all IDEs)
├── CLAUDE.md                # Claude Code project instructions
└── GEMINI.md                # Gemini project instructions
```

When you open your project in any supported IDE, the agents automatically have access to your tasks, constraints, memory, and skills. No configuration needed beyond the initial install.

## Quick Start

### Option A: Clone and Copy (Recommended for solo developers)

```bash
# Clone the galdr template
git clone https://github.com/wrm3/galdr.git

# Copy framework into your project
cd your-project
cp -r ../galdr/.cursor .cursor
cp -r ../galdr/.claude .claude
cp -r ../galdr/.agent .agent
cp -r ../galdr/.codex .codex
cp -r ../galdr/.opencode .opencode
cp -r ../galdr/.galdr .galdr
cp ../galdr/AGENTS.md AGENTS.md
cp ../galdr/CLAUDE.md CLAUDE.md
cp ../galdr/GEMINI.md GEMINI.md
```

On Windows, use `robocopy` or File Explorer to copy the folders. Each project gets its own `.galdr/` directory — do not share task data between projects.

Then open your project in Cursor (or any supported IDE) and run:

```
@g-setup
```

### Option B: Install via MCP Tool (for team deployments)

If someone on your team already runs the galdr Docker server:

1. Add the MCP server URL to your IDE config (`.cursor/mcp.json` or `.claude/settings.local.json`)
2. Ask your agent: *"Run galdr_install on this project"*
3. Done. Your project now has `.galdr/`, agents, skills, commands, and hooks.

## Key Features

### Adversarial Code Review — Two-Phase Quality Gate

galdr enforces a strict separation between **implementation** and **verification** — intentionally designed so the same agent that wrote the code can never mark it done.

```
# Phase 1 — in your current session:
@g-go-code          # Implement tasks. Every completed item is marked [🔍] (Awaiting Verification).
                    # Runs full AC gate before handing off. Never marks [✅].

# Phase 2 — in a NEW agent session (different window or invocation):
@g-go-verify        # Adversarial review only. Checks every acceptance criterion against actual files.
                    # Marks [✅] on pass, returns to [📋] on fail with documented failure reason.
```

**Why two sessions?** An agent that implements and verifies its own work has an inherent blind spot — it knows what it intended to write, which masks gaps between intent and reality. A fresh agent reads only what actually exists on disk.

**What `@g-go-code` enforces before marking `[🔍]`:**
- All acceptance criteria verified against actual files (not intent)
- Every `TODO` or stub annotated with `TODO[TASK-X→TASK-Y]` and a follow-up task created
- Pre-existing bugs discovered during implementation logged to `BUGS.md`
- `CHANGELOG.md` and `README.md` updated if user-facing behavior changed

**What `@g-go-verify` checks:**
- Each acceptance criterion independently confirmed against files on disk
- Any bug found during review is logged, not silently ignored
- `[✅]` is only set after all criteria pass — no partial credit

**Circuit breaker:** If a task fails verification 3 times in a row, it is automatically escalated to `[🚨]` Requires-User-Attention status. Automated agents skip it and it stays visible in the backlog until a human reviews and resets it.

### Task Management

Create tasks with structured specs, track status across phases, and let agents pick up where you (or they) left off.

```
@g-task-new "Add user authentication with JWT"
@g-status
```

Tasks use YAML frontmatter for metadata (priority, dependencies, subsystems) and markdown for specs and acceptance criteria. Every status change is recorded in a Status History table, creating a full audit trail.

| Status | Meaning |
|--------|---------|
| `[ ]` | Pending — not yet started |
| `[📋]` | Ready — task spec created, ready to implement |
| `[🔄]` | Active — being implemented |
| `[🔍]` | Awaiting Verification — implementation complete, pending independent review |
| `[✅]` | Complete — all criteria verified by a separate agent session |
| `[🚨]` | Requires Human — failed verification 3+ times, circuit breaker engaged |

### Skills (`g-skl-*`)

All galdr skills use the `g-skl-*` prefix. Use them directly or let agents invoke them:

| Skill | Purpose |
|-------|---------|
| `g-skl-tasks` | Task lifecycle (create, update, sync, sprint plan) |
| `g-skl-bugs` | Bug tracking and quality reports |
| `g-skl-plan` | PLAN.md and PRD management |
| `g-skl-project` | PROJECT.md and mission |
| `g-skl-constraints` | CONSTRAINTS.md (add, check, list — enforced at session start) |
| `g-skl-subsystems` | Subsystem registry and spec files |
| `g-skl-vault` | Vault ingest, search, and Obsidian compatibility |
| `g-skl-medkit` | `.galdr/` health check, repair, and migration |
| `g-skl-code-review` | Code review (security, performance, quality) |
| `g-skl-learn` | Continual learning — agents write insights to vault memory files |
| `g-skl-crawl` | Native web crawler (crawl4ai — no Docker needed) |
| `g-skl-ingest-docs` | Platform doc crawling with freshness tracking |
| `g-skl-ingest-url` | One-time URL capture into vault |
| `g-skl-ingest-youtube` | YouTube transcript ingestion into vault |
| `g-skl-harvest` | Analyze external repos for adoptable patterns |
| `g-skl-pcac-order` | Push tasks to child projects |
| `g-skl-pcac-ask` | Request action from parent project |
| `g-skl-pcac-sync` | Sync shared contracts with siblings |
| `g-skl-pcac-read` | Review and action cross-project INBOX |
| `g-skl-pcac-move` | Transfer files between topology projects |

### Knowledge Vault

A file-based knowledge store that persists across sessions, projects, and machines.

- **Session summaries** captured automatically after each conversation
- **Research notes** from web crawls, video analysis, and deep dives
- **Architectural decisions** extracted from conversations via continual learning
- **Platform documentation** crawled and indexed for offline reference

Vault notes use standardized YAML frontmatter (type, topics, date, source) for indexing and freshness tracking. Projects can share a vault (team knowledge) or keep one isolated (client work).

The vault is **Obsidian-compatible** — open the vault folder directly in Obsidian for graph view, tag browsing, and search.

```
@g-knowledge-refresh           # Check what docs are stale
@g-platform-crawl              # Crawl platform docs (Cursor, Claude, Gemini)
@g-ingest-url https://...      # Capture a URL into the vault
@g-ingest-youtube <url>        # Extract and save YouTube transcript
```

### Architectural Constraints

Define rules that agents **cannot** silently ignore. Constraints load at every session start and are checked before any task is marked complete.

```markdown
### C-004: UV for Python Virtual Environments
**Non-negotiable**: yes
**What this means**: Use `uv venv`, `uv pip install`, `uv run`. Never bare `pip` or `python -m venv`.
```

```
@g-constraint-add "Never use synchronous database calls in async routes"
@g-constraint-check                # Run compliance check now
```

### Code Review

Not a linter — a structured review covering security, performance, maintainability, and architectural alignment.

```
@g-code-review src/auth/
```

Generates a severity-classified report with specific file/line references and actionable recommendations.

### Cross-Project Topology (PCAC)

Projects can declare parent/child/sibling relationships. Parents broadcast tasks to children. Children request actions from parents. Siblings sync shared contracts.

```
@g-pcac-status                   # View topology role + open INBOX items
@g-pcac-order "Update API v2"    # Push task to child projects
@g-pcac-ask "Need auth service"  # Request from parent
@g-pcac-sync                     # Sync shared contracts with siblings
```

### Git Quality Gates

galdr hooks into your git workflow to prevent bad commits from reaching the remote:

```
@g-git-sanity     # Pre-commit check: staged secrets, large files, .galdr sync drift
@g-git-commit     # Conventional commit with task reference
@g-git-push       # Pre-push gate: regular push vs release validation
```

## MCP Server

The optional Docker-based MCP server provides tools that require infrastructure (database, embeddings, external APIs). The file-first architecture means everything works without it — MCP tools are enhancements, not gates.

| Category | Tools |
|----------|-------|
| **Memory** | `memory_search`, `memory_capture_session`, `memory_context`, `memory_ingest_session`, `memory_sessions`, `memory_capture_insight`, `memory_search_combined`, `memory_setup_user` |
| **Vault** | `vault_search`, `vault_search_all`, `vault_sync`, `vault_read`, `vault_list`, `vault_export_sessions` |
| **Install** | `galdr_install`, `galdr_plan_reset`, `galdr_health_report`, `galdr_validate_task`, `galdr_server_status` |
| **Crawling** | `platform_docs_search`, `platform_crawl_trigger`, `platform_crawl_status`, `crawl_add_target`, `crawl_list_targets`, `check_crawl_freshness` |
| **Oracle** | `oracle_query`, `oracle_execute` |
| **MediaWiki** | `mediawiki_page`, `mediawiki_search` |
| **Video** | `video_analyze`, `video_batch_process`, `video_extract_frames`, `video_extract_transcript`, `video_extract_metadata`, `video_get_playlist` |
| **Utility** | `md_to_html`, `config_reload`, `get_service_url` |

### Docker Services

| Service | Port | Description |
|---------|------|-------------|
| galdr (MCP) | 8092 | Main MCP server (streamable-http) |
| PostgreSQL | 5433 | RAG database with pgvector |
| pgAdmin | 8083 | Database management UI (optional) |
| MediaWiki | 8880 | Private knowledge base (optional) |

```bash
cd docker && docker compose up -d
```

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
```

### Vault Location

Edit `.galdr/.vault_location` to control where knowledge is stored:

```
{LOCAL}              # Default: .galdr/vault/ inside the project
/path/to/shared      # Shared vault: all projects share knowledge
```

## Design Principles

1. **File-first** — Every feature works without Docker or MCP. Agents read and write `.galdr/` files directly. MCP tools enhance but never gate functionality.
2. **Platform parity** — Reusable framework content stays aligned across all 10 IDE targets (5 root + 5 template). Cursor, Claude Code, Gemini, Codex, and OpenCode all get the same skills, agents, commands, and rules.
3. **Constraints over conventions** — Architectural rules are enforced, not suggested. Agents flag violations before proceeding, not after.
4. **Memory is durable** — Session history, learned facts, and research survive across conversations, machines, and IDE switches.
5. **Single source of truth** — Task status lives in files, not in agent memory. Two agents opening the same project see the same state.
6. **Adversarial quality** — The agent that implements code never verifies it. Independent verification is the only path to `[✅]`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs, requesting features, and contributing code.

## License

[MIT](LICENSE)

---

**galdr** — *Norse for "song magic." Because the best code is indistinguishable from incantation.*
