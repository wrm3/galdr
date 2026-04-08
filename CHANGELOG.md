# Changelog

All notable changes to galdr are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
galdr uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
### Changed
### Removed

---

## [1.1.0] - 2026-04-08

### Added

- **Task circuit breaker** (`[🚨]` Requires-User-Attention): tasks that fail verification 3 or more times are automatically escalated for human review. Automated agents skip them and they remain visible in the backlog until a human resets or cancels.
- **Status History table** on all task and bug files: every state transition records a timestamp, from-state, to-state, and reason. Creates a full audit trail for every item in the backlog.
- **Re-work surface at session start**: if a task's last Status History entry is a FAIL, it is flagged at session start so the implementing agent knows what to watch for before starting.
- **Pre-push gate** (`@g-git-push`, `scripts/galdr_push_gate.ps1`): validates that tasks are in the correct state, CHANGELOG is updated, and no staged secrets are present before allowing a push to reach the remote.
- **Pre-commit sanity check** (`@g-git-sanity`): detects staged secrets, files over size limits, and `.galdr/` sync drift before a commit is created.
- **Architectural constraints skill** (`g-skl-constraints`): dedicated ADD, UPDATE, CHECK, and LIST operations for `CONSTRAINTS.md`. Constraints are validated at session start and before marking any task complete.
- **Knowledge vault Obsidian compliance**: standardized frontmatter schema (type, topics, date, source), type registry, tag taxonomy, and encoding rules. All vault notes now comply with Obsidian's native indexing format.
- **MOC hub generation** (`gen_vault_moc.py`): automatically generates `_INDEX.md` navigation files for vault directories with 10 or more notes. Creates wikilinks that show connections in Obsidian graph view.
- **Platform documentation crawling** (`g-skl-ingest-docs`): schedule-aware ingestion with per-platform freshness tracking. Stale docs are flagged at session start.
- **Native web crawler** (`g-skl-crawl`): crawl4ai integration for clean LLM-optimized markdown extraction without Docker. Shared primitive used by ingest-docs, ingest-url, and harvest.
- **URL ingestion** (`g-skl-ingest-url`): one-time article and page capture into the vault with frontmatter and deduplication by source URL.
- **YouTube transcript ingestion** (`g-skl-ingest-youtube`): offline transcript extraction via yt-dlp. Stores in `research/videos/` with full frontmatter compliance.
- **Vault management skill** (`g-skl-vault`): unified vault operations including Obsidian compatibility tools, MOC rebuild, frontmatter linting, and GitHub repo summaries.
- **Continual learning skill** (`g-skl-learn`): agents self-report insights to vault memory files after each session. No external services required — file-only persistence.
- **Health and repair skill** (`g-skl-medkit`): single skill that detects what a `.galdr/` directory needs (version migration, structural repair, or routine maintenance) and performs it. Replaces the separate g-cleanup, g-grooming, and g-upgrade skills.
- **Platform crawl skill** (`g-platform-crawl`): dedicated skill for crawling Cursor, Claude Code, Gemini, and other platform documentation with configurable targets.
- **Dependency graph** (`g-skl-dependency-graph`): auto-generates `.galdr/DEPENDENCY_GRAPH.md` from task file dependencies. Shows blocked and blocking relationships.
- **SWOT review skill** (`g-skl-swot-review`): automated SWOT analysis for the current project phase. Reviewsprogress, architectural compliance, code quality, and technical debt.
- **Verify ladder skill** (`g-skl-verify-ladder`): configurable multi-level verification gates from minimal (lint only) to thorough (tests + acceptance + hallucination guard).
- **Knowledge refresh skill** (`g-skl-knowledge-refresh`): audit vault freshness, rebuild compiled pages, detect broken links and stale notes.

### Changed

- `g-go-code` now requires a Status History entry before marking any item `[🔍]`. The b3 step is mandatory.
- `g-go-verify` FAIL path now counts FAIL rows in Status History to determine whether to reset to `[📋]` or escalate to `[🚨]`.
- `g-go-code` skips `[🚨]` items entirely — logs them in the Skipped section as Requires-User-Attention.
- Session start protocol (step 2) now surfaces re-work tasks when the last Status History entry is a FAIL.
- `g-skl-tasks` and `g-skl-bugs` templates include Status History section. Every status transition appends a row.

### Fixed

- Session hook (`g-hk-agent-complete.ps1`): `$input` pipeline variable does not capture external-process stdin in PowerShell. Fixed to use `[Console]::In.ReadToEnd()`. Status mapping corrected from `"success"` to `"completed"` per Cursor hook schema.
- `pending_reflection.json` was never written when the session hook ran in a non-interactive terminal. Fixed `[Console]::IsInputRedirected` guard to prevent blocking on `ReadToEnd()`.

---

## [1.0.0] - 2026-04-04

### Added

- **Task management system**: YAML frontmatter task specs with sequential IDs, priority, dependencies, and subsystem tracking. Master `TASKS.md` checklist with per-file status sync.
- **Two-phase adversarial code review** (`@g-go-code` / `@g-go-verify`): implementation and verification are separated into distinct agent sessions. The implementing agent marks `[🔍]`; a separate agent marks `[✅]`. Neither can do both.
- **Five-IDE parity**: identical agents, skills, commands, and rules across Cursor (`.cursor/`), Claude Code (`.claude/`), Gemini (`.agent/`), Codex (`.codex/`), and OpenCode (`.opencode/`).
- **PCAC cross-project topology**: projects declare parent, child, and sibling relationships. Parents broadcast tasks (`@g-pcac-order`). Children request actions (`@g-pcac-ask`). Siblings sync shared contracts (`@g-pcac-sync`). Cross-project INBOX tracks all coordination items.
- **Knowledge vault**: file-based knowledge store for session summaries, research notes, architectural decisions, and platform documentation. Vault notes use standardized YAML frontmatter.
- **Session start protocol**: reads `.galdr/` state at session start, validates task sync, surfaces open bugs, checks for specification files, and displays project context in a structured summary.
- **Bug tracking**: sequential BUG-NNN IDs, severity classification (Critical/High/Medium/Low), `BUGS.md` index, individual bug spec files, and code annotation format (`BUG[BUG-NNN]: description`).
- **Architectural constraints** (`CONSTRAINTS.md`): non-negotiable project rules loaded at every session start. Agents flag violations before proceeding.
- **Subsystem registry** (`SUBSYSTEMS.md`, `subsystems/`): each subsystem has a spec file with locations, dependencies, dependents, and an Activity Log. Agents update the Activity Log on task completion.
- **9 galdr system agents**: task-manager, qa-engineer, code-reviewer, project, infrastructure, ideas-goals, verifier, project-initializer, pcac-coordinator.
- **Docker MCP server** (42 tools): RAG search, Oracle SQL, MediaWiki, vault indexing, session memory capture and retrieval, video analysis, platform crawling, and project health reports.
- **Continual learning**: agents extract durable facts from conversation transcripts and persist them in `AGENTS.md`. Agents remember preferences, project conventions, and past decisions across sessions.
- **TODO lifecycle enforcement**: stubs and TODOs must be annotated with `TODO[TASK-X→TASK-Y]` format and a follow-up task created before the implementing task can be marked complete.
- **Bug discovery gate**: pre-existing bugs encountered during implementation must have a BUG entry and code annotation before the task is marked `[🔍]`.
- **Git commit skill** (`g-skl-git-commit`): conventional commit format with task references and agent footers.
- **Project planning** (`g-skl-plan`, `g-skl-project`): PLAN.md (milestones and deliverables), PROJECT.md (mission, vision, goals), PRD files, and CONSTRAINTS.md.
- **Code review** (`g-skl-code-review`): structured review covering security, performance, maintainability, and architectural alignment. Severity-classified output with file/line references.
- **Harvest skill** (`g-skl-harvest`): analyze external repositories for adoptable patterns and improvements. Zero-change-without-approval output.

---

*galdr is built with galdr. The development history of this framework lives in the galdr_full source repository.*
