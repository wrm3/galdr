# galdr — First Time Use Guide

> **galdr** gives your AI coding agents structured memory, task management, and specialized skills. This guide walks you from zero to a fully operational galdr project.

---

## What galdr Does

When you open a new chat in Cursor or Claude Code, your AI agent starts fresh — no memory of previous decisions, no awareness of your architecture, no record of what was tried before. galdr fixes this with:

- **Persistent task tracking** in `.galdr/` files that survive across sessions
- **Project context** your agents read at session start (mission, goals, constraints)
- **Specialized skills** so agents know *how* to do things (code review, sprint planning, bug tracking)
- **Named agents** for specific roles (task manager, QA engineer, code reviewer)
- **Cross-IDE parity** — same data and skills in Cursor, Claude Code, Gemini, Codex, and OpenCode

---

## Step 1: Prerequisites

galdr requires:
- **Git** installed (for version control)
- **One of**: Cursor IDE, Claude Code, Gemini CLI, Codex, or OpenCode
- **Python 3.10+** and **uv** (only if you're running the MCP server — optional for basic use)
- **Docker** (only if you want the MCP server with RAG, Oracle, and vault tools — fully optional)

You do NOT need Docker, Python, or the MCP server for the core task management features.

---

## Step 2: Install galdr in Your Project

### Option A: Via galdr MCP Tool (Recommended)

If you have the galdr MCP server running, use the install tool:

```
galdr_install
```

This creates all required files and folders automatically.

### Option B: Manual Install

1. Clone or download galdr:
   ```bash
   git clone https://github.com/wrm3/galdr.git
   ```

2. Copy the template files into your project:
   ```bash
   # From the galdr repo, copy templates into your project
   cp -r galdr/templates/.cursor/ your-project/.cursor/
   cp -r galdr/templates/.claude/ your-project/.claude/
   cp -r galdr/templates/.galdr_template/ your-project/.galdr/
   cp galdr/templates/AGENTS.md your-project/AGENTS.md
   cp galdr/templates/CLAUDE.md your-project/CLAUDE.md
   ```

3. Initialize the `.galdr/` folder:
   ```
   @g-setup
   ```

---

## Step 3: First-Time Setup

After installing, run the setup command in your AI IDE:

### In Cursor:
```
@g-setup
```

### In Claude Code:
```
/g-setup
```

The setup will:
1. Create `.galdr/.identity` with your project's unique ID
2. Create all required `.galdr/` files (`TASKS.md`, `BUGS.md`, `PLAN.md`, etc.)
3. Create folder structure (`tasks/`, `bugs/`, `features/`, etc.)
4. Prompt you for your project name and mission

---

## Step 4: Fill in Your Project Context

Edit `.galdr/PROJECT.md` to describe your project:

```markdown
# PROJECT.md — My Project

## Mission
One sentence describing what this project does and why it exists.

## Goals
- G-01: [Your first goal with a measurable outcome]
- G-02: [Your second goal]

## Non-Goals
- Things explicitly out of scope
```

The more context you provide here, the better your agents will perform. They read this file at the start of every session.

---

## Step 5: Check Project Status

At any time, run:

```
@g-status
```

This shows:
- Active tasks and their status
- Current goals
- Recent ideas
- Any sync issues

---

## Step 6: Create Your First Task

```
@g-task-new
```

The agent will walk you through:
1. Task title and description
2. Acceptance criteria
3. Subsystem classification
4. Priority level

Tasks are stored in two places:
- **`.galdr/TASKS.md`** — the master checklist (quick reference)
- **`.galdr/tasks/taskNNN_title.md`** — the full spec file

---

## The .galdr/ Folder Structure

```
.galdr/
├── .identity          # Project ID, version, user identity (gitignored locally)
├── TASKS.md           # Master task checklist
├── BUGS.md            # Bug tracker
├── PLAN.md            # Project plan and deliverable index
├── FEATURES.md            # PRD index
├── PROJECT.md         # Mission, goals, non-goals
├── CONSTRAINTS.md     # Architectural rules agents must follow
├── IDEA_BOARD.md      # Captured ideas and potential improvements
├── SUBSYSTEMS.md      # System component registry
├── tasks/             # Individual task spec files
├── bugs/              # Individual bug spec files
├── features/              # Individual PRD files
├── subsystems/        # Per-subsystem spec files
├── reports/           # Health reports (date-prefixed, not committed)
└── logs/              # Hook-generated audit logs (not committed)
```

> **Important**: The `.galdr/` folder contains YOUR project's task data. The gitignore policy for this folder is up to you. Many teams commit `TASKS.md`, `PLAN.md`, and `PROJECT.md` but gitignore `logs/`, `.identity`, and reports.

---

## Key Commands Reference

### Daily Use

| Command | What It Does |
|---------|-------------|
| `@g-status` | Show project overview |
| `@g-task-new` | Create a new task |
| `@g-task-update` | Update a task's status |
| `@g-bug-report` | Report a bug |
| `@g-idea-capture` | Capture an idea ("make a note: ...") |
| `@g-code-review` | Review code for quality and security |
| `@g-git-commit` | Create a structured git commit |

### Project Health

| Command | What It Does |
|---------|-------------|
| `@g-medkit` | Full health check and repair of `.galdr/` |
| `@g-medkit apply` | Apply all detected repairs |
| `@g-task-sync-check` | Verify TASKS.md matches tasks/ folder |

### Planning

| Command | What It Does |
|---------|-------------|
| `@g-plan` | Create or update the project plan |
| `@g-idea-review` | Review and promote captured ideas |

---

## Task Status Cheat Sheet

| TASKS.md | Meaning |
|---------|---------|
| `[ ]` | Pending — not started |
| `[📋]` | Ready — spec written, ready to start |
| `[🔄]` | In progress — being worked on |
| `[🔍]` | Awaiting verification |
| `[✅]` | Completed |
| `[❌]` | Failed or cancelled |

---

## Triggering Skills Automatically

galdr agents respond to natural language triggers. You don't always need the `@g-` prefix:

| Say Something Like... | Agent Activates |
|-----------------------|----------------|
| "make a note of this idea" | `g-skl-ideas` → CAPTURE |
| "create a task for X" | `g-skl-tasks` → CREATE TASK |
| "the project is out of sync" | `g-skl-medkit` → REPAIR |
| "review this code" | `g-skl-code-review` |
| "report this bug" | `g-skl-bugs` → REPORT BUG |
| "what's the project status" | `g-skl-status` |

---

## Working with Multiple IDEs

galdr uses identical folder structure across all supported IDEs:

| IDE | Config Folder | Commands | Rules |
|-----|--------------|----------|-------|
| Cursor | `.cursor/` | `@g-{name}` | `.mdc` files |
| Claude Code | `.claude/` | `/g-{name}` | `.md` files |
| Gemini | `.agent/` | `@g-{name}` | `.md` files |
| Codex | `.codex/` | `@g-{name}` | `.md` files |
| OpenCode | `.opencode/` | Uses Claude's skills | `.md` files |

The `.galdr/` task data folder is shared — all IDEs read the same files.

---

## Optional: MCP Server Setup

The MCP server unlocks advanced features:

- **Vault** — cross-project knowledge base with semantic search
- **Session memory** — agents remember previous conversations
- **Oracle SQL** — read/write Oracle databases
- **MediaWiki** — read/write wiki pages
- **Platform docs** — crawl and search Cursor, Claude, Gemini documentation

### Quick Start (Docker)

```bash
cd galdr/docker
cp .env.example .env
# Edit .env with your API keys
docker compose up -d
```

Server starts on:
- MCP API: `http://localhost:8092`
- pgAdmin: `http://localhost:8083`
- Admin DB UI: `http://localhost:8092/admin/db`

Then add to your IDE's MCP config:
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

## Troubleshooting

### "galdr doesn't seem to be doing anything"

Run `@g-medkit` — it will diagnose the `.galdr/` folder and report what's wrong.

### "Tasks are out of sync"

Run `@g-task-sync-check` — it compares `TASKS.md` to the `tasks/` folder and reports mismatches.

### "The agent ignores galdr rules"

Check that:
1. The rules files are in the correct folder (`.cursor/rules/` for Cursor)
2. Rules are numbered and have `.mdc` extension (Cursor) or `.md` (Claude Code)
3. The session start hook ran (`g-hk-session-start.ps1`)

### "I want to start fresh"

```
@g-medkit
```

If the structure is corrupted beyond repair, use the galdr MCP tool:
```
galdr_plan_reset confirm=True
```

> ⚠️ `galdr_plan_reset` wipes `.galdr/` completely. Back up your tasks first.

---

## Next Steps

Once you're up and running:

1. **Read** `.galdr/PROJECT.md` and flesh out your goals
2. **Create** your first few tasks with `@g-task-new`
3. **Set architectural constraints** in `.galdr/CONSTRAINTS.md`
4. **Explore skills** — see `docs/SKILLS.md` for the full list
5. **Run a sprint** — `@g-go` starts an autonomous 2-hour work session (galdr_full only)

---

## Getting Help

- **Docs**: See `docs/` folder in this repo
- **Commands**: `docs/COMMANDS.md`
- **Skills**: `docs/SKILLS.md`
- **Agents**: `docs/AGENTS.md`
- **Hooks**: `docs/HOOKS.md`
- **GitHub**: [https://github.com/wrm3/galdr](https://github.com/wrm3/galdr)
