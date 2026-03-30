"""
galdr - Unified MCP Server with Dynamic Tool Loading

Provides:
- RAG (semantic search over knowledge bases)
- Deep research (Perplexity, Google - NO DuckDuckGo)
- MediaWiki integration
- Template installation for new projects

TRANSPORT MODES:
    - stdio (default): Standard input/output for IDE integration
    - sse: Server-Sent Events over HTTP
    - streamable-http: Full HTTP transport for Docker deployment

    Set MCP_TRANSPORT environment variable to choose transport mode.

DYNAMIC TOOL LOADING:
    Tools are loaded from galdr/tools/plugins/ at startup.
    Each .py file (except those starting with _) is loaded as a plugin.
"""
import os
import sys
import logging
import atexit
from pathlib import Path
from datetime import datetime
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Setup logging before imports
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"GALDR_{datetime.now():%Y%m%d}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("=" * 60)
logger.info("galdr server starting (unified MCP)...")

# Import configuration
from . import __version__
from .config import load_config

# Load configuration
try:
    config = load_config()
    logger.info("Configuration loaded successfully")
except EnvironmentError as e:
    logger.error(f"Configuration error: {e}")
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

# Import database modules (RAG)
from .database.client import RAGDatabase
from .database.embeddings import EmbeddingGenerator
from .database.multi_subject import MultiSubjectDatabase, SubjectAwareDBWrapper
from .subjects import SubjectManager
from .plugin_loader import PluginLoader
from .memory_rest import MEMORY_ROUTES, init_memory_rest
from .admin_db_rest import ADMIN_ROUTES, init_admin_db
from .install_rest import INSTALL_ROUTES, init_install_rest
from .vault_rest import VAULT_ROUTES, init_vault_rest
from .sync_ws import SYNC_ROUTES, init_sync_ws

# Initialize components
db: Optional[RAGDatabase] = None
multi_db: Optional[MultiSubjectDatabase] = None
embedding_generator: Optional[EmbeddingGenerator] = None
subject_manager: Optional[SubjectManager] = None
plugin_loader: Optional[PluginLoader] = None

# RAG components (optional - only if PostgreSQL configured)
if config.get('postgres_host'):
    try:
        subject_manager = SubjectManager()
        multi_db = MultiSubjectDatabase(subject_manager)
        db = RAGDatabase(config)
        embedding_generator = EmbeddingGenerator(config.get('openai_api_key'))

        logger.info("RAG components initialized")
        logger.info(f"Available subjects: {[s.id for s in subject_manager.list_subjects()]}")

        if multi_db.test_connection():
            logger.info("Database connection test successful")
        else:
            logger.warning("Database connection test failed - RAG queries may fail")

    except Exception as e:
        logger.warning(f"RAG initialization failed (optional): {e}")
        subject_manager = None
        multi_db = None
        db = None
        embedding_generator = None
else:
    logger.info("PostgreSQL not configured - RAG features disabled")

# Initialize FastMCP server
mcp = FastMCP(
    "galdr_docker",
    instructions="""
Unified MCP Server - galdr

This server provides multiple tool categories:

**Agent Memory:**
- memory_ingest_session - Tier-1 passive capture (raw turns from file adapters)
- memory_capture_session - Tier-2 active capture (AI self-reports session summary)
- memory_capture_insight - Store structured insight with category/topic for dedup
- memory_search - Semantic search across all stored sessions and captures
- memory_search_combined - Combined search across turns and captures
- memory_sessions - List recent sessions for a project
- memory_context - Token-budgeted context block for session-start injection
- memory_setup_user - Create/update ~/.galdr/user_config.json (cross-platform: Windows/macOS/Linux). Call with action='whoami' to check current identity, action='setup' to configure.

**Oracle Database:**
- oracle_query - Execute read queries (source database)
- oracle_execute - Execute write operations (target database)

**MediaWiki:**
- mediawiki_page - Get, create, or update wiki pages (get/create/update actions)
- mediawiki_search - Search wiki pages

**Template Installer:**
- galdr_install - install galdr to new projects
- galdr_plan_reset - Reset .galdr/ to blank template
- galdr_server_status - Health check

**Platform Documentation:**
- platform_docs_search - Semantic search over weekly-crawled Cursor/Claude/Gemini platform docs (requires Firecrawl profile)

**Project Health:**
- galdr_health_report - Compute health score (0-100) for a galdr-managed project; returns per-subsystem breakdown, stale claims, blocked tasks, and Firecrawl crawl status
- galdr_validate_task - Validate a task against ARCHITECTURE_CONSTRAINTS.md before claiming it; returns pass/fail with violations listed; call before any autonomous task claim

**Service URLs:**
- get_service_url - Returns the correct URL for mediawiki, pgadmin, galdr, or postgres — environment-aware (works across home, work, OKE/Kubernetes)

**Utilities:**
- md_to_html - Convert markdown to styled HTML

Use the appropriate tools based on your task.
"""
)

# Initialize plugin loader and discover plugins
try:
    plugins_dir = Path(__file__).parent / "tools" / "plugins"
    plugin_loader = PluginLoader(plugins_dir)

    # Set context that plugins can access
    plugin_loader.set_context(
        db=db,
        multi_db=multi_db,
        embedding_generator=embedding_generator,
        subject_manager=subject_manager,
        config=config,
        config_path=Path(__file__).parent / "subjects.json"
    )

    # Discover and load plugins
    discovered = plugin_loader.discover_plugins()
    logger.info(f"Discovered {len(discovered)} plugins: {discovered}")

    # Register plugins with FastMCP
    registered_count = plugin_loader.register_all(mcp)
    logger.info(f"Registered {registered_count} dynamic tools with MCP server")

except Exception as e:
    logger.error(f"Plugin loading failed: {e}")
    print(f"WARNING: Plugin loading failed: {e}", file=sys.stderr)


# ========================================
# Server Status Tool (Always Available)
# ========================================

@mcp.tool(
    description="Get server status, loaded plugins, and available features. Use as health check."
)
async def galdr_server_status() -> dict:
    """
    Get server status and list of loaded tools.
    Also serves as a health check endpoint.

    Returns:
        Server status including loaded plugins and available features
    """
    features = []
    if db is not None:
        features.append("rag")
    if config.get('oracle_src_host'):
        features.append("oracle")
    if config.get('gemini_api_key'):
        features.append("gemini")
    if config.get('mediawiki_url'):
        features.append("mediawiki")
    features.append("template_installer")  # Always available

    # Security warnings
    warnings = []
    pgadmin_password = os.environ.get("PGADMIN_PASSWORD", "")
    if pgadmin_password in ("admin", "admin@galdr.local", "", "CHANGE_ME_strong_password"):
        warnings.append(
            "pgAdmin is running with a weak or default password. "
            "Set a strong PGADMIN_PASSWORD in .env before exposing pgAdmin externally."
        )
    mediawiki_admin_pw = os.environ.get("MEDIAWIKI_ADMIN_PASSWORD", "")
    if mediawiki_admin_pw in ("CHANGE_ME", "CHANGE_ME_strong_password", ""):
        warnings.append(
            "MediaWiki MEDIAWIKI_ADMIN_PASSWORD is using a placeholder value. "
            "Set a real password in .env before starting the mediawiki profile."
        )

    return {
        'success': True,
        'status': 'healthy',
        'server': 'galdr_docker',
        'version': __version__,
        'transport': os.getenv('MCP_TRANSPORT', 'stdio'),
        'features': features,
        'plugins': plugin_loader.list_plugins() if plugin_loader else [],
        'subjects': [s.id for s in subject_manager.list_subjects()] if subject_manager else [],
        'default_subject': subject_manager.default_subject_id if subject_manager else None,
        'warnings': warnings if warnings else None,
        'service_urls': {
            'galdr': config.get('GALDR_url', 'http://localhost:8082'),
            'mediawiki': config.get('mediawiki_url') or 'not configured',
            'pgadmin': config.get('pgadmin_url', 'http://localhost:8083'),
        }
    }


# Cleanup handler
@atexit.register
def cleanup():
    """Clean up resources on shutdown."""
    logger.info("Shutting down galdr server...")
    if db:
        db.close()
    if subject_manager:
        subject_manager.close_all_connections()
    logger.info("Shutdown complete")


def main():
    """
    Main entry point for the MCP server.

    Transport mode is controlled by MCP_TRANSPORT environment variable:
    - stdio (default): Standard I/O for IDE integration
    - sse: Server-Sent Events over HTTP
    - streamable-http: Full HTTP transport for Docker
    """
    transport = os.getenv('MCP_TRANSPORT', 'stdio').lower()

    if transport == 'stdio':
        logger.info("Starting galdr MCP server (stdio transport)")
        logger.info(f"Loaded {len(plugin_loader.plugins) if plugin_loader else 0} dynamic tools")
        mcp.run(transport='stdio')

    elif transport in ('sse', 'streamable-http', 'http'):
        host = os.getenv('MCP_HOST', '0.0.0.0')
        port = int(os.getenv('MCP_PORT', '8082'))

        logger.info(f"Starting galdr MCP server ({transport} transport)")
        logger.info(f"Listening on http://{host}:{port}")
        logger.info(f"Loaded {len(plugin_loader.plugins) if plugin_loader else 0} dynamic tools")

        try:
            import uvicorn
        except ImportError:
            logger.error("uvicorn required for HTTP transport. Install with: pip install uvicorn")
            print("ERROR: uvicorn required for HTTP transport", file=sys.stderr)
            sys.exit(1)

        # Initialize REST bridges with shared DB/embedding components
        init_memory_rest(db=db, embedding_generator=embedding_generator, config=config)
        init_admin_db(db=db)
        init_install_rest(config=config)
        init_vault_rest(db=db, embedding_generator=embedding_generator)
        init_sync_ws(db=db)
        from starlette.applications import Starlette
        from starlette.routing import Mount
        from contextlib import asynccontextmanager

        if transport == 'sse':
            mcp_app = mcp.sse_app()
            app = Starlette(
                routes=SYNC_ROUTES + ADMIN_ROUTES + MEMORY_ROUTES + INSTALL_ROUTES + VAULT_ROUTES + [Mount("/", app=mcp_app)],
            )
        else:
            # streamable-http: Starlette does NOT propagate lifespan to mounted
            # sub-apps, so the StreamableHTTPSessionManager task group is never
            # initialized — causing "Task group is not initialized" 500s.
            # Fix: build the mcp app first (which creates _session_manager),
            # then wire that manager's run() into the outer app's lifespan.
            mcp_app = mcp.streamable_http_app()

            @asynccontextmanager
            async def lifespan(app):
                async with mcp._session_manager.run():
                    yield

            app = Starlette(
                lifespan=lifespan,
                routes=SYNC_ROUTES + ADMIN_ROUTES + MEMORY_ROUTES + INSTALL_ROUTES + VAULT_ROUTES + [Mount("/", app=mcp_app)],
            )

        logger.info("MCP server ready")
        logger.info("  /admin/db          — DB Explorer UI")
        logger.info("  /vault             — Vault Knowledge Graph Browser")
        logger.info("  /memory/*          — agent memory REST bridge")
        logger.info("  /sync/{project_id} — WebSocket file sync")
        logger.info("use galdr_server_status tool to check health")
        uvicorn.run(app, host=host, port=port, log_level="info")

    else:
        logger.error(f"Unknown transport mode: {transport}")
        print(f"ERROR: Unknown transport mode '{transport}'", file=sys.stderr)
        sys.exit(1)


def main_http():
    """Convenience entry point for HTTP transport mode."""
    os.environ['MCP_TRANSPORT'] = 'streamable-http'
    main()


def main_sse():
    """Convenience entry point for SSE transport mode."""
    os.environ['MCP_TRANSPORT'] = 'sse'
    main()


if __name__ == "__main__":
    main()
