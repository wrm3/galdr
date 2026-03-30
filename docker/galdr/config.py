"""
Configuration management for galdr Unified MCP Server.

Loads environment variables from secrets file or local .env.
Supports multiple configuration sources for different tool modules.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Default secrets file location (Windows path)
DEFAULT_SECRETS_PATH = Path(r"C:\secrets\galdr_docker.env")

# Allow override via environment variable for multi-project isolation
SECRETS_PATH = Path(os.getenv('GALDR_ENV_PATH', str(DEFAULT_SECRETS_PATH)))

# Also check for command line --env-file argument
for i, arg in enumerate(sys.argv):
    if arg == '--env-file' and i + 1 < len(sys.argv):
        SECRETS_PATH = Path(sys.argv[i + 1])
        break
    elif arg.startswith('--env-file='):
        SECRETS_PATH = Path(arg.split('=', 1)[1])
        break


def load_config() -> dict:
    """
    Load configuration from secrets file or local .env.

    Priority:
    1. C:\\secrets\\galdr_docker.env (Docker deployment)
    2. Local .env file (development)
    3. Environment variables already set

    Returns:
        dict: Configuration dictionary with all values

    Raises:
        EnvironmentError: If critical variables are missing
    """
    # Try secrets file first
    if SECRETS_PATH.exists():
        load_dotenv(SECRETS_PATH)
        logger.info(f"Loaded configuration from {SECRETS_PATH}")
    else:
        # Fall back to local .env
        local_env = Path(__file__).parent / ".env"
        if local_env.exists():
            load_dotenv(local_env)
            logger.info(f"Loaded configuration from {local_env}")
        else:
            # Try project root .env
            root_env = Path(__file__).parent.parent / ".env"
            if root_env.exists():
                load_dotenv(root_env)
                logger.info(f"Loaded configuration from {root_env}")
            else:
                logger.warning(
                    f"No .env file found. Expected at {SECRETS_PATH} or local .env. "
                    "Using environment variables."
                )

    # Build configuration from all sources
    config = {

        # === Oracle Database ===
        'oracle_src_host': os.getenv('ORACLE_SRC_HOST'),
        'oracle_src_port': os.getenv('ORACLE_SRC_PORT', '1521'),
        'oracle_src_user': os.getenv('ORACLE_SRC_USER'),
        'oracle_src_password': os.getenv('ORACLE_SRC_PASSWORD'),
        'oracle_src_service': os.getenv('ORACLE_SRC_SERVICE'),
        'oracle_src_schema': os.getenv('ORACLE_SRC_SCHEMA'),

        'oracle_tgt_host': os.getenv('ORACLE_TGT_HOST'),
        'oracle_tgt_port': os.getenv('ORACLE_TGT_PORT', '1521'),
        'oracle_tgt_user': os.getenv('ORACLE_TGT_USER'),
        'oracle_tgt_password': os.getenv('ORACLE_TGT_PASSWORD'),
        'oracle_tgt_service': os.getenv('ORACLE_TGT_SERVICE'),
        'oracle_tgt_schema': os.getenv('ORACLE_TGT_SCHEMA'),

        # === PostgreSQL ===
        'postgres_host': os.getenv('POSTGRES_HOST'),
        'postgres_port': os.getenv('POSTGRES_PORT', '5432'),
        'postgres_db': os.getenv('POSTGRES_DB') or os.getenv('POSTGRES_DB', 'rag_knowledge'),
        'postgres_user': os.getenv('POSTGRES_USER', 'postgres'),
        'postgres_password': os.getenv('POSTGRES_PASSWORD'),
        'postgres_connection_string': os.getenv('POSTGRES_CONNECTION_STRING'),


        # === OpenAI (Embeddings) ===

       'openai_api_key': os.getenv('OPENAI_API_KEY'),

        # === Gemini API (upcoming) ===
        'gemini_api_key': os.getenv('GEMINI_API_KEY'),

        # === Research APIs (plugins not yet implemented — keys reserved) ===
        'perplexity_api_key': os.getenv('PERPLEXITY_API_KEY'),
        'google_search_api_key': os.getenv('GOOGLE_SEARCH_API_KEY'),
        'google_search_engine_id': os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
        'serpapi_key': os.getenv('SERPAPI_KEY'),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),

        # === MediaWiki ===
        'mediawiki_url': (
            os.getenv('MEDIAWIKI_SERVER')
            or os.getenv('MEDIAWIKI_URL')
        ),
        'mediawiki_username': os.getenv('MEDIAWIKI_USERNAME'),
        'mediawiki_password': os.getenv('MEDIAWIKI_PASSWORD'),
        'mediawiki_api_key': os.getenv('MEDIAWIKI_API_KEY'),

        # === Service URLs (env-driven for environment portability) ===
        'pgadmin_url': os.getenv('PGADMIN_URL', 'http://localhost:8083'),
        'GALDR_url': os.getenv('GALDR_URL', 'http://localhost:8082'),

        # === Template Installer ===
        'template_source_path': os.getenv('TEMPLATE_SOURCE_PATH'),

        # === Template Git Source (for remote template fetching) ===
        'template_git_repo': os.getenv('TEMPLATE_GIT_REPO'),
        'template_git_branch': os.getenv('TEMPLATE_GIT_BRANCH', 'main'),
        'template_git_token': os.getenv('TEMPLATE_GIT_TOKEN'),
        'template_git_path': os.getenv('TEMPLATE_GIT_PATH', 'template'),
        'template_full_git_path': os.getenv('TEMPLATE_FULL_GIT_PATH', 'template'),
    }

    # Validate critical variables for core RAG functionality
    # (Other modules can work without their specific vars)
    if not config.get('openai_api_key'):
        logger.warning("OPENAI_API_KEY not set - RAG embedding will not work")

    if config.get('postgres_host'):
        logger.info(f"PostgreSQL configured: {config['postgres_host']}")
    else:
        logger.warning("POSTGRES_HOST not set - RAG storage will not work")

    # Log which optional modules are configured
    if config.get('oracle_src_host'):
        logger.info("Oracle database configured")
    if config.get('gemini_api_key'):
        logger.info("Gemini API configured")
    if config.get('mediawiki_url'):
        logger.info(f"MediaWiki configured: {config['mediawiki_url']}")
    if config.get('pgadmin_url'):
        logger.info(f"pgAdmin URL: {config['pgadmin_url']}")

    return config


def get_postgres_connection_string(config: dict = None) -> str:
    """
    Build PostgreSQL connection string from config.

    Args:
        config: Configuration dictionary (loads if not provided)

    Returns:
        PostgreSQL connection string
    """
    if config is None:
        config = load_config()

    # Check for full connection string first
    if config.get('postgres_connection_string'):
        return config['postgres_connection_string']

    host = config['postgres_host']
    port = config['postgres_port']
    database = config['postgres_db']
    user = config['postgres_user']
    password = config['postgres_password']

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_oracle_connection_config(database: str = "read", config: dict = None) -> dict:
    """
    Get Oracle database connection configuration.

    Args:
        database: "read" for source (read-only) or "write" for target
        config: Configuration dictionary (loads if not provided)

    Returns:
        Oracle connection configuration dictionary
    """
    if config is None:
        config = load_config()

    if database == "read":
        return {
            'host': config.get('oracle_src_host'),
            'port': config.get('oracle_src_port', '1521'),
            'user': config.get('oracle_src_user'),
            'password': config.get('oracle_src_password'),
            'service': config.get('oracle_src_service'),
            'schema': config.get('oracle_src_schema'),
        }
    else:
        return {
            'host': config.get('oracle_tgt_host'),
            'port': config.get('oracle_tgt_port', '1521'),
            'user': config.get('oracle_tgt_user'),
            'password': config.get('oracle_tgt_password'),
            'service': config.get('oracle_tgt_service'),
            'schema': config.get('oracle_tgt_schema'),
        }
