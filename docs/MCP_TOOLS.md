# galdr MCP Tools Reference

The galdr Docker server exposes these MCP tools via streamable-http on port 8082.

## galdr System

| Tool | Description |
|------|-------------|
| `galdr_install` | Install galdr framework into a new project |
| `galdr_plan_reset` | Reset .galdr/ to blank template (requires confirm=True) |
| `galdr_server_status` | Health check |
| `galdr_health_report` | Compute health score (0-100) for a galdr-managed project |
| `galdr_validate_task` | Validate a task against ARCHITECTURE_CONSTRAINTS.md |

## RAG (Retrieval-Augmented Generation)

| Tool | Description |
|------|-------------|
| `rag_search` | Semantic search in knowledge base |
| `rag_ingest_text` | Add content to knowledge base |
| `rag_list_subjects` | List available knowledge bases |

## Agent Memory

| Tool | Description |
|------|-------------|
| `memory_ingest_session` | Tier-1 passive capture (raw turns from file adapters) |
| `memory_capture_session` | Tier-2 active capture (AI self-reports session summary) |
| `memory_capture_insight` | Store structured insight with category/topic |
| `memory_search` | Semantic search across stored sessions |
| `memory_search_combined` | Combined search across turns and captures |
| `memory_sessions` | List recent sessions for a project |
| `memory_context` | Token-budgeted context block for session-start injection |
| `memory_setup_user` | Create/update user config |

## Vault (Knowledge Store)

| Tool | Description |
|------|-------------|
| `vault_sync` | Index a vault .md file into the database |
| `vault_search` | Semantic/keyword search against vault_notes |
| `vault_search_all` | Unified search across vault + platform_docs + memory |
| `vault_read` | Read full note content from DB by path |
| `vault_list` | Browse/filter vault notes by type, project, tags |
| `vault_export_sessions` | Export session summaries as vault-ready .md content |

## Oracle Database

| Tool | Description |
|------|-------------|
| `oracle_query` | Execute read queries (SELECT, DESCRIBE) |
| `oracle_execute` | Execute write operations (INSERT, UPDATE, DDL) |

## MediaWiki

| Tool | Description |
|------|-------------|
| `mediawiki_page` | Get, create, or update wiki pages |
| `mediawiki_search` | Search wiki pages |

## Platform Documentation

| Tool | Description |
|------|-------------|
| `platform_docs_search` | Semantic search over crawled platform docs |
| `check_crawl_freshness` | Check if platform docs need re-crawling |
| `update_crawl_registry` | Record completed crawl in registry |

## Utilities

| Tool | Description |
|------|-------------|
| `md_to_html` | Convert markdown to styled HTML |
| `config_reload` | Hot-reload API keys without Docker rebuild |
| `get_service_url` | Get correct URL for services (environment-aware) |
