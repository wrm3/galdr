<p align="center">
  <img src="logo/Galdr_Logo_Big.jpg" alt="galdr banner" width="800">
</p>

<p align="center">
  <strong>Song magic for your codebase.</strong><br>
  Persistent memory, multi-repo orchestration, and adversarial quality gates for AI coding agents across every major IDE.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.1.0-green.svg" alt="Version"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://github.com/wrm3/galdr/releases"><img src="https://img.shields.io/github/v/release/wrm3/galdr?label=release" alt="Latest Release"></a>
  <a href="https://github.com/wrm3/galdr"><img src="https://img.shields.io/github/stars/wrm3/galdr?style=social" alt="GitHub stars"></a>
</p>

---

## The Problem

You have great AI coding agents. And they forget everything the moment you close the chat.

Session 1: You explain your architecture, your constraints, why you chose Postgres over Mongo.  
Session 12: The agent uses SQLite. Because it doesn't remember session 1.

You're running 4 repos — `api`, `web`, `mobile`, `shared-lib`. When something changes in `shared-lib`, every downstream repo needs to know. There's no mechanism for that. You copy-paste tasks manually. Half the time you forget.

You finish a feature and ask the same agent to verify it. It passes everything — of course it does, it wrote the code and knows what it *meant* to write. The bugs it introduced are invisible to it.

**galdr is the infrastructure layer that fixes all three of these.** It wraps around your AI IDEs and gives agents durable memory, cross-repo coordination, and adversarial quality enforcement — without changing how you code.

---

## What galdr gives your agents

**Persistent memory** — Architectural decisions, learned project conventions, session summaries, and research notes that survive across conversations, machines, and IDE restarts.

**Multi-repo orchestration** — Declare parent/child/sibling relationships between repos. Broadcast tasks that cascade down a project hierarchy. Let child projects request upstream action. Sync shared contracts between siblings. One unified INBOX for cross-project coordination.

**Adversarial quality gates** — The agent that implements code is *structurally prevented* from marking it done. A separate agent session runs verification. Stuck tasks (3+ failed reviews) auto-escalate to human attention with a full audit trail.

**An Obsidian-compatible knowledge vault** — Every research session, architectural decision, platform doc crawl, and YouTube transcript is stored as a properly-tagged Obsidian note. Open the vault folder in Obsidian and get graph view, search, and backlinks over everything your agents have ever learned.

**Architectural constraints** — Rules agents must follow, loaded at every session start. Not suggestions. If an agent's action would violate a constraint, it must flag the conflict before proceeding.

**5-IDE parity** — Cursor, Claude Code, Gemini, Codex, and OpenCode. Same agents, same skills, same memory, same task state. Switch IDEs mid-task and pick up exactly where you left off.

---

## What's Included

| Component | Count | What it covers |
|-----------|-------|----------------|
| **Agents** | 9 | Task manager, code reviewer, QA engineer, project planner, infrastructure, ideas, verifier, project initializer, PCAC coordinator |
| **Skills** | 39 | Tasks, bugs, plan, project, subsystems, vault, constraints, code review, git, crawl, ingest (docs/URL/YouTube), learn, harvest, PCAC (5 skills), medkit, and more |
| **Commands** | 52 | Full `@g-*` command surface — task management, code quality, vault, multi-repo, ideas, constraints, and maintenance |
| **Hooks** | 12 | Session start, agent complete, pre-commit, pre-push, PCAC inbox check, vault operations |
| **Rules** | 12 | Always-apply: documentation, git workflow, error reporting, task completion gates, TODO/stub lifecycle, bug discovery |
| **IDE Platforms** | 5 | Cursor, Claude Code, Gemini, Codex, OpenCode |

---

## How It Works

```
your-project/
├── .galdr/                    # Everything galdr manages
│   ├── TASKS.md               # Master task checklist (YAML + markdown specs)
│   ├── BUGS.md                # Bug index with severity and status
│   ├── PLAN.md                # Strategic milestones and PRD index
│   ├── PROJECT.md             # Mission, vision, goals (plain language)
│   ├── CONSTRAINTS.md         # Architectural rules agents must obey
│   ├── SUBSYSTEMS.md          # Component registry + dependency graph
│   ├── .vault_location        # Path to your knowledge vault (default: local)
│   ├── tasks/                 # Individual task specs (YAML + acceptance criteria)
│   ├── bugs/                  # Individual bug spec files
│   ├── prds/                  # PRD files
│   ├── subsystems/            # Per-subsystem spec files with Activity Logs
│   ├── linking/               # Cross-project topology + INBOX
│   └── vault/                 # Local vault (if .vault_location = {LOCAL})
│
├── .cursor/                   # Cursor IDE
│   ├── agents/                # 9 galdr agents
│   ├── skills/                # 39 skills (g-skl-*)
│   ├── commands/              # 52 @g-* commands
│   ├── hooks/                 # 12 PowerShell automation hooks
│   └── rules/                 # 12 always-apply rules
│
├── .claude/                   # Claude Code  (identical to .cursor/)
├── .agent/                    # Gemini        (identical, adapted format)
├── .codex/                    # Codex         (skills subset)
├── .opencode/                 # OpenCode      (agents + commands)
│
├── AGENTS.md                  # Project context (read at session start by all IDEs)
├── CLAUDE.md                  # Claude Code project instructions
└── GEMINI.md                  # Gemini project instructions
```

---

## Quick Start

```bash
# Clone the galdr template
git clone https://github.com/wrm3/galdr.git

# Copy framework into your project
cd your-project
cp -r ../galdr/.cursor    .cursor
cp -r ../galdr/.claude    .claude
cp -r ../galdr/.agent     .agent
cp -r ../galdr/.codex     .codex
cp -r ../galdr/.opencode  .opencode
cp -r ../galdr/.galdr     .galdr
cp ../galdr/AGENTS.md     AGENTS.md
cp ../galdr/CLAUDE.md     CLAUDE.md
cp ../galdr/GEMINI.md     GEMINI.md
```

On Windows: use `robocopy` or File Explorer. Each project gets its own `.galdr/` — never share task data between projects.

Open your project in Cursor (or any supported IDE) and run:

```
@g-setup
```

That creates your `.galdr/.identity`, seeds the structural files, and registers the project. You're ready.

---

## Key Features

### Multi-Project Orchestration (PCAC)

galdr can model your entire software ecosystem as a graph of related projects — parent services, child microservices, sibling repos sharing contracts. Agents in each project can coordinate across the graph without manual copy-paste.

```
@g-pcac-adopt api-service        # Register api-service as a child of this project
@g-pcac-claim platform-core      # Register platform-core as parent of this project
@g-pcac-status                   # View your position in the topology + open INBOX items
```

**Broadcasting tasks downstream:**
```
@g-pcac-order "Upgrade auth library to v3"
# Creates the task in every child project's .galdr/
# Cascades to grandchildren if cascade_depth > 1
# Child agents pick it up at their next session start
```

**Requesting upstream action:**
```
@g-pcac-ask "Need rate-limiting in the API gateway"
# Writes to parent project's INBOX.md
# Parent agent sees it at session start and can accept, reject, or defer
```

**Sibling contract sync:**
```
@g-pcac-sync shared-auth-schema   # Sync a shared contract spec with all siblings
@g-pcac-notify web-frontend "Deployed new endpoint: /api/v3/users"
```

Every project has an INBOX (`linking/INBOX.md`) that the session-start hook reads. Broadcasts, requests, and sync notifications land there and are surfaced before any other work begins. Conflicts (when two projects disagree on a shared contract) block all session work until resolved.

---

### Adversarial Code Review — Two-Phase Quality Gate

```
# Phase 1 — implement (your current session):
@g-go-code

# Every completed item is marked [🔍] (Awaiting Verification)
# The implementing agent NEVER marks [✅]
```

```
# Phase 2 — verify (a SEPARATE agent session, new window):
@g-go-verify

# Reads only what exists on disk
# Confirms every acceptance criterion independently
# [✅] = all criteria confirmed | [📋] = fail, specific reasons documented
```

An agent that implements and verifies its own work has a systematic blind spot — it knows what it *intended* to write. A separate session reads only what actually exists. This is not optional ceremony; it is the only path to `[✅]`.

**Circuit breaker:** If a task fails verification 3 or more times, it is automatically escalated to `[🚨]` Requires-User-Attention. Automated agents skip it permanently. A Status History table records every state transition with timestamp and reason — complete audit trail.

| Status | Meaning |
|--------|---------|
| `[ ]` | Pending |
| `[📋]` | Ready — task spec created |
| `[🔄]` | Active — being implemented |
| `[🔍]` | Awaiting Verification — implementation complete |
| `[✅]` | Complete — verified by a separate session |
| `[🚨]` | Requires Human — circuit breaker engaged after 3+ failures |

---

### Knowledge Vault (Obsidian-Compatible)

Every project gets a file-based knowledge store. All notes use a standardized YAML frontmatter schema compatible with Obsidian's native indexing — so the same vault that stores your AI's memory is also a proper personal knowledge base.

```
@g-ingest-docs https://docs.cursor.com    # Crawl platform docs (schedule-aware, freshness tracked)
@g-ingest-url  https://example.com/post   # One-time article capture
@g-ingest-youtube https://youtu.be/...    # Extract YouTube transcript (yt-dlp, offline)
@g-learn                                   # Agents self-report insights to vault memory files
```

Open the vault folder directly in **Obsidian** for graph view, tag search, and backlinks over everything your agents have ever learned. The `_INDEX.md` MOC hub files (auto-generated for directories with 10+ notes) create the graph connections.

**Vault configuration** — set `vault_location` in `.galdr/.identity`:

```
vault_location={LOCAL}                # Default: .galdr/vault/ inside this project
vault_location=/path/to/shared        # Shared vault: multiple projects contribute to one knowledge base
```

**What the vault stores:**
- Session summaries captured after each conversation
- Architectural decisions extracted from discussions via `@g-learn`
- Platform documentation crawled for offline reference (Cursor, Claude, Gemini APIs, etc.)
- YouTube transcripts and video research notes
- Harvest reports from external repo analysis

---

### Task Management

Tasks are YAML-frontmatter markdown files with structured specs and acceptance criteria. The master `TASKS.md` checklist syncs with individual files in `tasks/`. Every status change appends to the Status History table.

```
@g-task-new "Implement WebSocket reconnection with exponential backoff"
# Creates tasks/task051_websocket_reconnection.md with:
# - YAML frontmatter (id, priority, subsystems, dependencies)
# - Objective and acceptance criteria
# - Status History table
```

Tasks support dependencies (`blocked_by: [49, 50]`), subsystem tagging, sprint planning, and complexity scoring. The session-start protocol reads all `[📋]` tasks and surfaces any that have a recent FAIL in their history.

---

### Architectural Constraints

```
@g-constraint-add "Never use synchronous HTTP calls in async route handlers"
@g-constraint-check                   # Verify current implementation against all constraints
```

Constraints live in `CONSTRAINTS.md` with enforcement definitions. They load at every session start (Step 0 of the session protocol) and are checked before any task is marked `[🔍]`. An agent that would violate a constraint must flag it and get explicit approval — it cannot silently work around it.

---

### Skills (`g-skl-*`)

Skills are detailed instruction documents that tell agents not just *what* to do but exactly *how* to do it — including operations, file formats, edge cases, and cross-references.

| Skill | What it owns |
|-------|-------------|
| `g-skl-tasks` | TASKS.md, tasks/ — full task lifecycle |
| `g-skl-bugs` | BUGS.md, bugs/ — bug tracking and quality reports |
| `g-skl-plan` | PLAN.md, prds/ — strategy and PRD management |
| `g-skl-project` | PROJECT.md — mission, goals, project identity |
| `g-skl-constraints` | CONSTRAINTS.md — ADD, UPDATE, CHECK, LIST |
| `g-skl-subsystems` | SUBSYSTEMS.md, subsystems/ — component registry |
| `g-skl-vault` | Vault operations, Obsidian compliance, MOC rebuild |
| `g-skl-medkit` | `.galdr/` health check, repair, and version migration |
| `g-skl-code-review` | Security, performance, quality, architectural alignment |
| `g-skl-learn` | Continual learning — agents write insights to vault memory |
| `g-skl-crawl` | Native crawl4ai web crawler (no Docker required) |
| `g-skl-ingest-docs` | Platform docs with schedule-aware freshness tracking |
| `g-skl-ingest-url` | One-time URL capture with deduplication |
| `g-skl-ingest-youtube` | YouTube transcripts via yt-dlp |
| `g-skl-harvest` | Analyze external repos for adoptable patterns |
| `g-skl-knowledge-refresh` | Audit vault freshness, rebuild MOC hubs |
| `g-skl-pcac-order` | Broadcast tasks to child projects |
| `g-skl-pcac-ask` | Request action from parent project |
| `g-skl-pcac-sync` | Sync shared contracts with sibling projects |
| `g-skl-pcac-read` | Review and action cross-project INBOX |
| `g-skl-pcac-notify` | Send lightweight FYI notifications across topology |
| `g-skl-pcac-move` | Transfer files/folders between topology projects |
| `g-skl-pcac-adopt` | Register a child project (bidirectional topology) |
| `g-skl-pcac-claim` | Register a parent project (bidirectional topology) |
| `g-skl-git-commit` | Conventional commits with task references |
| `g-skl-swot-review` | Automated SWOT analysis for current project phase |
| `g-skl-verify-ladder` | Configurable verification gates (lint → full AC check) |
| `g-skl-dependency-graph` | Auto-generate DEPENDENCY_GRAPH.md from task dependencies |
| `g-skl-cursor-cli` | Cursor CLI (agent mode, Cloud Agent, API mode) |
| `g-skl-claude-cli` | Claude Code CLI (headless, MCP config, multi-agent) |
| `g-skl-gemini-cli` | Gemini CLI (checkpointing, extensions, memory patterns) |

---

### Command Reference

**Task & Bug Management**

| Command | What it does |
|---------|-------------|
| `@g-task-new` | Create a task with full spec and acceptance criteria |
| `@g-task-update` | Update task status, priority, or metadata |
| `@g-task-sync-check` | Validate TASKS.md ↔ tasks/ file sync |
| `@g-bug-report` | Log a bug with severity, file, and description |
| `@g-bug-fix` | Fix a reported bug and update BUGS.md |
| `@g-go` | Full autonomous cycle (implement + verify in sequence) |
| `@g-go-code` | Implement-only: marks completed items `[🔍]`, never `[✅]` |
| `@g-go-verify` | Verify-only: run in a new agent session to confirm `[🔍]` items |
| `@g-status` | Project status: active tasks, goals, open bugs, ideas |
| `@g-workflow` | Task expansion and sprint planning |

**Planning & Goals**

| Command | What it does |
|---------|-------------|
| `@g-plan` | Create or update PLAN.md and PRD files |
| `@g-setup` | Initialize galdr in a new project |
| `@g-goal-update` | Update PROJECT_GOALS.md |
| `@g-phase-add` | Add a new project phase |
| `@g-phase-pivot` | Pivot project direction |
| `@g-subsystems` | Sync check, add, update subsystem Activity Logs |

**Knowledge & Vault**

| Command | What it does |
|---------|-------------|
| `@g-ingest-docs` | Crawl platform docs with freshness tracking |
| `@g-ingest-url` | Capture a URL into vault |
| `@g-ingest-youtube` | Extract and save YouTube transcript |
| `@g-vault-ingest` | Manual vault file ingest with frontmatter |
| `@g-vault-search` | Search the vault |
| `@g-vault-status` | Vault health and freshness report |
| `@g-vault-lint` | Audit vault frontmatter compliance |
| `@g-learn` | Capture insights to vault memory files |
| `@g-harvest` | Analyze external repos for adoptable patterns |

**Multi-Project (PCAC)**

| Command | What it does |
|---------|-------------|
| `@g-pcac-adopt` | Register a child project (bidirectional link) |
| `@g-pcac-claim` | Register a parent project (bidirectional link) |
| `@g-pcac-status` | View topology position and open INBOX items |
| `@g-pcac-order` | Broadcast a task to child projects with cascade depth |
| `@g-pcac-ask` | Send a request to the parent project |
| `@g-pcac-sync` | Initiate contract sync with a sibling project |
| `@g-pcac-read` | Review and action all INBOX items |
| `@g-pcac-notify` | Send a lightweight FYI notification across topology |
| `@g-pcac-move` | Transfer files/folders to another project in topology |

**Code Quality & Git**

| Command | What it does |
|---------|-------------|
| `@g-code-review` | Structured review: security, performance, quality, architecture |
| `@g-git-commit` | Conventional commit with task reference and agent footer |
| `@g-git-sanity` | Pre-commit check: staged secrets, large files, sync drift |
| `@g-git-push` | Pre-push gate: regular vs release validation |

**Constraints & Compliance**

| Command | What it does |
|---------|-------------|
| `@g-constraint-add` | Add a new architectural constraint |
| `@g-constraint-check` | Run compliance check against all active constraints |

**Ideas & Discovery**

| Command | What it does |
|---------|-------------|
| `@g-idea-capture` | Capture an idea to IDEA_BOARD.md |
| `@g-idea-review` | Review and evaluate IDEA_BOARD entries |
| `@g-idea-farm` | Proactive codebase scan for improvement opportunities |

**Maintenance**

| Command | What it does |
|---------|-------------|
| `@g-medkit` | `.galdr/` health check, repair, and version migration |
| `@g-swot-review` | SWOT analysis for the current project phase |
| `@g-dependency-graph` | Generate DEPENDENCY_GRAPH.md from task dependencies |

---

### Git Quality Gates

```
@g-git-sanity     # Before committing: detects staged secrets, files over size limits,
                  # and .galdr/ sync drift between TASKS.md and tasks/ files

@g-git-commit     # Conventional commit format (feat/fix/chore) with task reference
                  # and optional agent footer for autonomous commits

@g-git-push       # Pre-push gate: validates task states, CHANGELOG updated,
                  # release-mode checks README version badge
```

---

## Optional: Docker MCP Server

galdr is fully functional without any server infrastructure — the file-first architecture means every feature works with plain files. For teams that want semantic search, session memory across machines, Oracle database access, or server-side crawling, the galdr Docker MCP server adds 42 server-backed tools.

The Docker server is a separate companion component (not included in this template). See the [galdr Docker server repository](https://github.com/wrm3/galdr_full) for setup instructions.

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

---

## Configuration

### Identity

`@g-setup` creates `.galdr/.identity` with your project details:

```
project_id=<generated-uuid>
project_name=my-project
user_id=<your-user-id>
user_name=YourName
galdr_version=1.1.0
```

### Vault Location

`vault_location` in `.galdr/.identity` controls where knowledge is stored:

```
vault_location={LOCAL}                  # Default: .galdr/vault/ inside this project
vault_location=/path/to/shared/vault    # Shared vault: multiple projects write here
```

A shared vault is opt-in. One-off or client projects should use `{LOCAL}` to keep knowledge isolated.

### Environment Variables (Docker only)

Only needed if you run the optional Docker MCP server. Copy `.env.example` to `.env`:

```bash
POSTGRES_DB=rag_knowledge
POSTGRES_USER=galdr
POSTGRES_PASSWORD=your_password_here
OPENAI_API_KEY=your-key-here
```

---

## Design Principles

1. **File-first** — Every feature works without Docker or any external service. MCP tools enhance, never gate.
2. **Platform parity** — 10 IDE targets stay synchronized (5 root + 5 template). Cursor, Claude Code, Gemini, Codex, and OpenCode get identical skills, agents, and commands.
3. **Adversarial quality** — Implementation and verification are structurally separated. The same agent cannot do both.
4. **Memory is durable** — Session history, decisions, and research survive across conversations, machines, and IDE switches.
5. **Single source of truth** — Task state lives in files, not in agent memory. Any agent opening the project sees the same state.
6. **Constraints over conventions** — Rules are enforced at session start and at every task completion gate, not suggested once and forgotten.
7. **Topology-aware** — Projects are not islands. The PCAC system treats a multi-repo codebase as a first-class entity with discoverable structure.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs, requesting features, and contributing to the framework.

galdr is built with galdr. The framework develops itself — task specs, acceptance criteria, two-phase review, and all.

## License

[MIT](LICENSE)

---

**galdr** — *Norse for "song magic." Because the best code is indistinguishable from incantation.*
