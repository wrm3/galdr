# CLAUDE.md - galdr

## Project Overview
galdr is an AI-powered task management and development system for Cursor IDE, Claude Code, Gemini, Codex, and OpenCode. It provides structured task tracking, project planning, quality assurance, and workflow management through a file-based system with enforced synchronization.

## This Repository's Purpose
This is the **source repository** for the galdr system. It contains:
- The complete rule set for task management
- 19+ specialized galdr agents (agents/skills architecture — 95% context reduction)
- 32+ skills covering task management, QA, planning, video/3D, and more
- 8 slim always-apply rules per platform
- Templates for installing galdr in other projects
- MCP server for RAG, research, Oracle, and video analysis tools

When making changes here, consider:
1. Parity: Changes to `.cursor/` must also apply to `.agent/`, `.claude/`, `.codex/`, `.opencode/` and vice versa
2. Does this affect the `docker/templates/` files?
3. Does this need to update `AGENTS.md` galdr section?
4. Should this trigger a version bump?

## Tech Stack
- **Rules**: `.claude/rules/*.md` (Claude Code) / `.cursor/rules/*.mdc` (Cursor)
- **Skills**: Markdown with YAML frontmatter in `.claude/skills/` and `.cursor/skills/`
- **MCP Server**: Python with FastMCP, PostgreSQL/pgvector for RAG, Oracle support
- **Task Files**: Markdown with YAML frontmatter
- **Package Management**: UV for Python

## Key Directories
```
.cursor/       # Cursor IDE configuration
.claude/       # Claude Code configuration (rules, skills, agents)
.agent/        # Gemini/Antigravity configuration
.codex/        # OpenAI Codex configuration
.galdr/        # Task management data (TASKS.md, tasks/, phases/)
docker/        # MCP server (Docker)
templates/     # Install templates for new projects
docs/          # Project documentation
```

## MCP Tools Available
| Tool | Description |
|------|-------------|
| `rag_search` | Semantic search in knowledge base |
| `rag_ingest_text` | Add content to knowledge base |
| `rag_list_subjects` | List available knowledge bases |
| `research_deep` | Comprehensive research with Perplexity |
| `research_search` | Web search for research |
| `oracle_query` | Read-only SQL on Oracle |
| `oracle_execute` | Write SQL on Oracle |
| `mediawiki_page` | MediaWiki CRUD operations |
| `mediawiki_search` | Search MediaWiki |
| `galdr_install` | Install full galdr environment |
| `galdr_plan_reset` | Reset .galdr/ to blank template |
| `galdr_server_status` | Health check |
| `galdr_health_report` | Compute health score for a galdr project |
| `platform_docs_search` | Search crawled platform docs |
| `md_to_html` | Convert markdown to HTML |
| `memory_ingest_session` | Ingest raw turns from file adapters |
| `memory_capture_session` | AI self-reports session summary |
| `memory_search` | Semantic search over session memory |
| `memory_sessions` | List recent sessions for a project |
| `memory_context` | Token-budgeted context block |
| `vault_search_all` | Unified search across vault + platform_docs + memory |
| `vault_sync` | Index a vault .md file into the database |
| `vault_search` | Semantic/keyword search against vault_notes |
| `vault_read` | Read full note content from DB by path |
| `vault_list` | Browse/filter vault notes |

## Development Commands
```bash
cd docker && docker compose up -d                          # Start MCP server
docker ps | grep galdr_docker                              # Check status
docker logs galdr_docker -f                                # View logs
cd docker && docker-compose up -d --build galdr_docker     # Rebuild
```

## Rules & Configuration
**Hybrid architecture** — agents/skills replace monolithic rules:

- **Always-apply rules** (8 files): `00_always`, `01_documentation`, `02_git_workflow`, `08_powershell`, `09_python_venv`, `25_galdr_session_start`, `33_enforcement_catchall`, `norse_personality`
- **Galdr agents** (19 files): `g-task-manager`, `g-planner`, `g-qa-engineer`, `g-workflow-manager`, `g-infrastructure`, `g-autonomous`, `g-verifier`, `g-self-improvement`, `g-project-files`, `g-platform-parity`, `g-multi-agent`, `g-memory`, `g-cursor-cli`, `g-claude-cli`, `g-codebase-analyst`, `g-ideas-goals`, `g-code-reviewer`, `g-python-dev`, `g-project-manager`
- **Skills** (32+ files): `g-task-new`, `g-plan`, `g-review`, `g-sprint`, + 13 video/3D skills

## Security
- Never commit API keys, tokens, or passwords
- Use environment variables for secrets
- Always use parameterized queries
- Oracle credentials passed per-query via tool parameters

## Architecture Notes

- **Docker NEVER touches the vault** — agents, hooks, and humans read/write vault files directly on the host. Docker is a compute service only.
- **File-first fallback**: All vault features have a file-first fallback path (local grep/glob for search, direct file write for storage). MCP-dependent features are enhancements, never the sole path.
- **8-target propagation**: When syncing skills, commands, hooks, or rules, there are now 9 targets: `.cursor/`, `.claude/`, `.agent/`, `.codex/`, `.opencode/`, `templates/.cursor/`, `templates/.claude/`, `templates/.agent/`, `templates/.codex/`.
- **OpenCode skills discovery** — OpenCode natively reads `.claude/skills/` and `.agents/skills/`. No `.opencode/skills/` copy needed. `.cursor/skills/` is NOT auto-discovered by OpenCode.
- **OpenCode rules via opencode.json** — `opencode.json` `instructions` field accepts `.cursor/rules/*.mdc` glob, referencing rules directly from `.cursor/` without any copy.
- **OpenCode has no hooks** — `.opencode/` supports `agents/`, `commands/`, `skills/`, and `opencode.json` only. PowerShell hooks are Cursor/Claude-only.
- **Template parity**: The `.galdr_template/` directories are equal peers with no single canonical source. All must stay identical with `{placeholders}`.
- `templates/` contains **real file copies** (not symlinks). New skills/hooks/commands must be manually propagated.
- `galdr_install` deploys from the `templates/` subfolder in the GitHub repo (not repo root).
- `config_reload` MCP tool hot-reloads API keys without Docker rebuild.
- Vault `_index.yaml` at vault root is an auto-generated master catalog. Enables offline browsing without Docker/MCP.
- Knowledge cards (`knowledge/` folder) consolidate multiple source notes into authoritative references.

49. **`.galdr/.identity` replaces 4 separate dotfiles** — `.project_id`, `.user_id`, `.vault_location`, and `.galdr_version` were consolidated into a single `.galdr/.identity` INI file with keys: `project_id`, `project_name`, `user_id`, `user_name`, `galdr_version`, `vault_location`. `project_name` is the root folder name (human-readable). `project_id` is the stable UUID PK that survives renames. All 9 active projects migrated 2026-04-03. _(2026-04-03)_
---
**Version**: 1.0.0
**Last Updated**: 2026-03-28
**Supported IDEs**: Cursor, Claude Code, Gemini, Codex, OpenCode
