# galdr_docker

Unified MCP (Model Context Protocol) server providing RAG, research, MediaWiki, video analysis, and template installation tools.

## Features

| Category | Tools | Description |
|----------|-------|-------------|
| **RAG** | `rag_search`, `rag_ingest_text`, `rag_list_sources`, `rag_stats` | Semantic search over knowledge bases using pgvector |
| **Research** | `research_search`, `research_scrape`, `research_comprehensive`, `research_deep` | Web research via Perplexity/Google (NO DuckDuckGo) |
| **Video** | `video_analyze`, `video_extract_frames`, `video_extract_transcript`, `video_batch_process` | YouTube/video analysis with AI vision |
| **MediaWiki** | `mediawiki_page`, `mediawiki_search` | Wiki page CRUD and search |
| **Template** | `install_galdr` | install galdr to new projects (from GitHub) |
| **Oracle** | `oracle_query`, `oracle_execute` | Oracle database read/write operations |
| **Utility** | `md_to_html` | Convert markdown to styled HTML |

---

## Quick Start (Docker)

### 1. Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- API keys for services you want to use

### 2. Configure Environment

Compose loads **one `.env` from the project root** (parent of `docker/`). Create or edit `.env` there:

```bash
# From repo root
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/Mac

notepad .env   # Windows — set API keys and passwords
```

**Required in `.env` for Docker:**

| Variable | Required | Notes |
|----------|----------|--------|
| `POSTGRES_DB` | Yes | e.g. `rag_knowledge` |
| `POSTGRES_USER` | Yes | e.g. `galdr` |
| `POSTGRES_PASSWORD` | Yes | Used by Postgres, galdr, MediaWiki, Firecrawl |
| `OPENAI_API_KEY` | Yes (RAG) | Embeddings |
| `MEDIAWIKI_*` | If using MediaWiki profile | Admin + bot credentials; set `MEDIAWIKI_SECRET_KEY` and `MEDIAWIKI_UPGRADE_KEY` (e.g. `openssl rand -hex 32`) |
| `PGADMIN_EMAIL` / `PGADMIN_PASSWORD` | If using admin profile | For pgAdmin login |
| `GITHUB_TOKEN` | If using install_galdr | Repo read access |

### 3. Start the Server

From the **docker/** directory, pass the project-root `.env` so Compose gets all variables (no "variable is not set" warnings):

```bash
cd docker
docker compose --env-file ../.env up -d
```

From the **repo root**:

```bash
docker compose -f docker/docker-compose.yml up -d
```

```bash
# View logs
docker compose logs -f galdr
```

### 4. Verify Deployment

```bash
# Check health endpoint
curl http://localhost:8082/health

# Or use PowerShell
Invoke-WebRequest -Uri "http://localhost:8082/health" -UseBasicParsing
```

---

## Deployment Options

### Option A: Docker Compose (Recommended)

Full stack with PostgreSQL and optional pgAdmin.

```bash
# Start core services
docker-compose up -d

# Start with pgAdmin for database management
docker-compose --profile admin up -d

# Stop services
docker-compose down

# Stop and remove data volumes (DESTRUCTIVE — resets DB and MediaWiki)
docker-compose down -v
```

**Reset database and MediaWiki:** To rebuild Postgres and MediaWiki with the credentials and names from your current `.env` (project root):

1. Set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (and MediaWiki vars if you use that profile) in `.env`.
2. From `docker/`: `docker compose down -v` (removes volumes).
3. `docker compose up -d` (and `--profile mediawiki` or `--profile admin` if needed). Init scripts run with the new values; RAG and MediaWiki start clean.

**Services:**
| Service | Port | Description |
|---------|------|-------------|
| `galdr` | 8082 | MCP server (SSE transport) - includes video analysis |
| `postgres` | 5433 | PostgreSQL with pgvector |
| `pgadmin` | 8083 | Database admin UI (optional) |

### Option B: Standalone Container

If you have an external PostgreSQL database:

```bash
# Build the image
docker build -t galdr .

# Run with environment variables
docker run -d \
  --name galdr \
  -p 8082:8082 \
  -e OPENAI_API_KEY=sk-your-key \
  -e POSTGRES_HOST=your-postgres-host \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=rag_knowledge \
  -e POSTGRES_USER=galdr \
  -e POSTGRES_PASSWORD=your-password \
  -e MCP_TRANSPORT=sse \
  galdr
```

### Option C: Local Development (stdio)

For IDE integration without Docker:

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run with stdio transport (for IDE integration)
python -m galdr.server
```

---

## Client Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "galdr": {
      "url": "http://localhost:8082/sse"
    }
  }
}
```

**Config file location:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

### VS Code (Continue Extension)

Add to Continue config:

```json
{
  "models": [...],
  "mcpServers": [
    {
      "name": "galdr",
      "transport": {
        "type": "sse",
        "url": "http://localhost:8082/sse"
      }
    }
  ]
}
```

### Cursor IDE

Add to MCP settings:

```json
{
  "galdr": {
    "transport": "sse",
    "url": "http://localhost:8082/sse"
  }
}
```

---

## Environment Variables

### Required for RAG

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for embeddings | `sk-...` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` or `postgres` |
| `POSTGRES_PASSWORD` | Database password | `your_secure_password` |

### Optional: Research & Video APIs

| Variable | Description |
|----------|-------------|
| `PERPLEXITY_API_KEY` | Perplexity API (best for research) |
| `GOOGLE_SEARCH_API_KEY` | Google Custom Search API |
| `GOOGLE_SEARCH_ENGINE_ID` | Google Search Engine ID |
| `ANTHROPIC_API_KEY` | Anthropic API (for summaries and video vision analysis) |

### Optional: MediaWiki

| Variable | Description |
|----------|-------------|
| `MEDIAWIKI_URL` | Wiki base URL |
| `MEDIAWIKI_USERNAME` | Bot username |
| `MEDIAWIKI_PASSWORD` | Bot password |

### Optional: Oracle Database

| Variable | Description |
|----------|-------------|
| `ORACLE_SRC_HOST` | Source Oracle host (read-only queries) |
| `ORACLE_SRC_PORT` | Source Oracle port (default: 1521) |
| `ORACLE_SRC_USER` | Source database username |
| `ORACLE_SRC_PASSWORD` | Source database password |
| `ORACLE_SRC_SERVICE` | Source service name |
| `ORACLE_TGT_HOST` | Target Oracle host (write operations) |
| `ORACLE_TGT_PORT` | Target Oracle port (default: 1521) |
| `ORACLE_TGT_USER` | Target database username |
| `ORACLE_TGT_PASSWORD` | Target database password |
| `ORACLE_TGT_SERVICE` | Target service name |

---

## Transport Modes

| Mode | Use Case | Command/Config |
|------|----------|----------------|
| `stdio` | IDE integration (local) | Default, or `MCP_TRANSPORT=stdio` |
| `sse` | HTTP with Server-Sent Events | `MCP_TRANSPORT=sse` |
| `streamable-http` | Full HTTP transport | `MCP_TRANSPORT=streamable-http` |

**Docker Compose uses SSE by default** (best for network access).

---

## Common Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Just the MCP server
docker-compose logs -f galdr

# Last 100 lines
docker-compose logs --tail=100 galdr
```

### Restart Services

```bash
# Restart MCP server only
docker-compose restart galdr

# Restart everything
docker-compose restart
```

### Update and Rebuild

```bash
# Pull latest and rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Database Operations

```bash
# Connect to PostgreSQL
docker exec -it galdr_postgres psql -U galdr -d rag_knowledge

# Run SQL file
docker exec -i galdr_postgres psql -U galdr -d rag_knowledge < your_script.sql

# Backup database
docker exec galdr_postgres pg_dump -U galdr rag_knowledge > backup.sql

# Restore database
docker exec -i galdr_postgres psql -U galdr -d rag_knowledge < backup.sql
```

### Reset Everything

```bash
# Stop and remove containers, networks, volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

---

## Health Check

The server provides a health check endpoint and tool:

```bash
# HTTP health check
curl http://localhost:8082/health

# Using the MCP tool (from connected client)
# Call: galdr_server_status
```

Response:
```json
{
  "success": true,
  "status": "healthy",
  "server": "galdr_docker",
  "version": "2.0.0",
  "features": ["rag", "research", "template_installer"],
  "plugins": [...]
}
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs for errors
docker-compose logs galdr

# Common issues:
# - Missing OPENAI_API_KEY
# - PostgreSQL not ready (wait and retry)
# - Port 8082 already in use
```

### Database connection failed

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
docker exec -it galdr_postgres pg_isready -U galdr

# Check PostgreSQL logs
docker-compose logs postgres
```

### MCP client can't connect

1. Verify server is running: `docker-compose ps`
2. Check port is accessible: `curl http://localhost:8082/health`
3. Verify client config uses correct URL: `http://localhost:8082/sse`
4. Check firewall isn't blocking port 8082

### RAG search returns no results

```bash
# Check if data exists
docker exec -it galdr_postgres psql -U galdr -d rag_knowledge -c "SELECT COUNT(*) FROM sources;"

# Check embeddings exist
docker exec -it galdr_postgres psql -U galdr -d rag_knowledge -c "SELECT COUNT(*) FROM content_chunks WHERE embedding IS NOT NULL;"
```

---

## File Structure

```
galdr_docker/
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Container build instructions
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── pyproject.toml         # Python project config
│
├── init_db/               # PostgreSQL initialization
│   ├── 01_extensions.sql  # Enable pgvector
│   ├── 02_schema.sql      # Create tables/indexes
│   ├── 03_multi_subject.sql # Multi-subject support
│   └── 04_grants.sql      # Permissions
│
├── galdr/                 # Main package
│   ├── server.py          # FastMCP server
│   ├── config.py          # Configuration loader
│   ├── plugin_loader.py   # Dynamic tool loading
│   ├── subjects.py        # Multi-subject manager
│   │
│   ├── database/          # Database modules
│   │   ├── client.py      # RAG database client
│   │   ├── embeddings.py  # OpenAI embeddings
│   │   └── multi_subject.py
│   │
│   └── tools/plugins/     # MCP tool plugins
│       ├── rag_*.py       # RAG tools
│       ├── research_*.py  # Research tools
│       ├── mediawiki_*.py # MediaWiki tools
│       ├── oracle_*.py    # Oracle database tools
│       ├── install_*.py   # Template installation tools
│       └── md_to_html.py  # Markdown to HTML converter
│
└── templates/             # Installation templates
```

---

## License

MIT License - See LICENSE file for details.
