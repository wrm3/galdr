# Changelog

All notable changes to **galdr** are documented here.

---

## [1.1.0] — 2026-04-05 · *galdr slim — first stable release*

This release marks the first stable, public-ready version of **galdr slim** — a clean, lightweight rewrite designed to work standalone without the Docker MCP backend. The goal: clone it, drop it into any project, and get to work immediately.

### Added
- **Local chat logging** — minimal session transcript logging that works without the MCP server. At the end of each agent session, a `.galdr/logs/*_chat.log` file is written using the project's own Cursor transcript files (or `state.vscdb` as fallback). Implemented for Cursor, Claude Code, Gemini/Agent, and Codex.
- **Ecosystem context in README** — galdr is now documented as the foundation of a larger suite of projects (`galdr_full`, `galdr_mcp`, `galdr_forge`, `galdr_agent`, `galdr_cli`, `galdr_ide`, `galdr_desktop`, `galdr_vault`, `galdr_master_control`).

### Fixed
- Corrected agent count in README (9 → 8) and file tree comment to match actual files.
- Corrected skill count in README (17 → 16) and file tree comment to match actual files.
- Corrected command count in file tree comment (25 → 24; table was already correct).
- Cross-Project Topology section now correctly labels `@g-topology`, `@g-broadcast`, `@g-request` as planned features for `galdr_master_control`, not currently available commands.
- Reset `.galdr/.identity` to blank template state (`project_id={project_id}`) — was accidentally committed with a live UUID.
- Removed `g-sprint` command and `g-skl-sprint` skill (full-version features not included in slim).
- Removed full-version folder references from `g-setup` command and corrected slim layout in `g-skl-setup` and session-start rule.
- Fixed `g-agnt-project-initializer` and blocked premature verify logs.
- Mandated PRD file creation when `PLAN.md` references PRDs.

### Removed
- MCP memory ingestion adapters (`cursor_adapter.py`, `claude_adapter.py`, heartbeat scheduler, vault sync, WebSocket sync, audit logger) — these require the Docker backend and are not part of galdr slim. See `galdr_mcp` (in development) for the full server stack.

---

## [1.0.0] — 2025 · *galdr full (deprecated)*

Initial release based on `fstrent_rules` / `trent_rules` lineage. Included full MCP Docker integration, vault sync, WebSocket real-time sync, and audit logging. This version was functional but complex — the bloat led to the slim rewrite above.

> This release is no longer maintained. Use `galdr` (slim) for new projects, or watch `galdr_full` for the next iteration of the full-featured version.

---

*galdr — Norse for "song magic." Because the best code is indistinguishable from incantation.*
