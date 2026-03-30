"""
get_service_url — MCP tool
Returns the correct base URL for any named service in the galdr stack.

URLs are read from environment variables so they automatically reflect the
deployment environment (home, work LAN, OKE/Kubernetes, etc.).

Usage:
    get_service_url(service="mediawiki")
    → {"service": "mediawiki", "url": "http://localhost:8880", "status": "configured"}

Supported services: mediawiki, pgadmin, galdr, postgres
"""

import os
from typing import Any

TOOL_NAME = "get_service_url"
TOOL_DESCRIPTION = (
    "Returns the base URL for a named service in the galdr stack. "
    "URLs are environment-driven so they work across home, work, and cloud deployments. "
    "Supported services: mediawiki, pgadmin, galdr, postgres. "
    "Use this instead of hardcoding localhost ports — the URL changes when deployed to OKE/Kubernetes."
)
TOOL_PARAMS = {
    "type": "object",
    "properties": {
        "service": {
            "type": "string",
            "description": "Name of the service to look up.",
            "enum": ["mediawiki", "pgadmin", "galdr", "postgres"],
        }
    },
    "required": ["service"],
}


def _service_config() -> dict[str, dict[str, Any]]:
    """Build service config from environment at call time (not at import time)."""
    postgres_host = os.environ.get("POSTGRES_HOST", "localhost")
    postgres_port = os.environ.get("POSTGRES_PORT", "5433")

    return {
        "mediawiki": {
            "url": (
                os.environ.get("MEDIAWIKI_SERVER")
                or os.environ.get("MEDIAWIKI_URL")
                or "http://localhost:8880"
            ),
            "description": "MediaWiki knowledge base",
            "note": (
                "Set MEDIAWIKI_SERVER in .env to override. "
                "Start service with: docker compose --profile mediawiki up -d"
            ),
            "login_url": "{url}/wiki/Special:UserLogin",
            "api_url": "{url}/api.php",
        },
        "pgadmin": {
            "url": (
                os.environ.get("PGADMIN_URL")
                or "http://localhost:8083"
            ),
            "description": "pgAdmin 4 — PostgreSQL management UI",
            "note": (
                "Set PGADMIN_URL in .env to override. "
                "Start service with: docker compose --profile admin up -d. "
                "Login with PGADMIN_EMAIL / PGADMIN_PASSWORD from .env."
            ),
            "login_url": "{url}/login",
        },
        "galdr": {
            "url": (
                os.environ.get("GALDR_URL")
                or "http://localhost:8082"
            ),
            "description": "galdr MCP server (SSE/HTTP transport)",
            "note": (
                "Set GALDR_URL in .env to override. "
                "SSE endpoint: {url}/sse  |  MCP endpoint: {url}/mcp"
            ),
            "sse_url": "{url}/sse",
            "mcp_url": "{url}/mcp",
        },
        "postgres": {
            "url": f"postgresql://{postgres_host}:{postgres_port}",
            "description": "PostgreSQL (pgvector) — RAG + MediaWiki + memory",
            "note": (
                "Internal host=postgres port=5432 (within Docker network). "
                f"External host={postgres_host} port={postgres_port} (from host machine). "
                "Database: rag_knowledge (RAG), mediawiki (wiki)."
            ),
            "connection_string": (
                f"postgresql://{{user}}:{{password}}@{postgres_host}:{postgres_port}/{{db}}"
            ),
        },
    }


async def execute(service: str) -> dict[str, Any]:
    services = _service_config()

    if service not in services:
        return {
            "error": f"Unknown service '{service}'",
            "available_services": list(services.keys()),
        }

    info = services[service].copy()
    base_url = info["url"]

    # Resolve {url} placeholders in sub-fields
    for key, val in info.items():
        if isinstance(val, str) and "{url}" in val:
            info[key] = val.replace("{url}", base_url)

    configured = bool(
        os.environ.get("MEDIAWIKI_SERVER")
        or os.environ.get("MEDIAWIKI_URL")
        or os.environ.get("PGADMIN_URL")
        or os.environ.get("GALDR_URL")
        or os.environ.get("POSTGRES_HOST")
    ) if service in ("mediawiki", "pgadmin", "galdr", "postgres") else False

    return {
        "service": service,
        "url": base_url,
        "status": "configured" if configured else "default",
        **{k: v for k, v in info.items() if k not in ("url",)},
    }
