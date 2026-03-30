"""
galdr_video_analyzer - MCP Server for YouTube Video Analysis

Provides tools for YouTube playlist monitoring, video analysis, and content extraction.
Designed for automated content pipelines like CatchTheFraqUp.

TRANSPORT MODES:
    Set MCP_TRANSPORT environment variable:
    - stdio (default): For IDE integration (Cursor, Claude Code)
    - sse: Server-Sent Events over HTTP
    - streamable-http: Full HTTP for Docker/multi-client deployment
    
    For HTTP transports, also set:
    - MCP_HOST=0.0.0.0 (default: 127.0.0.1)
    - MCP_PORT=8080 (default: 8080)

DYNAMIC TOOL LOADING:
    Tools are loaded from galdr_video_analyzer/tools/plugins/ at startup.
    Each .py file (except those starting with _) is loaded as a plugin.
    
    To add a new tool:
    1. Create a .py file in tools/plugins/
    2. Define TOOL_NAME, TOOL_DESCRIPTION, and execute() function
    3. Restart the server
"""
import os
import sys
import logging
import atexit
from pathlib import Path

# Load .env file from project root BEFORE any other imports that might need env vars
from dotenv import load_dotenv
_project_root = Path(__file__).parent.parent
_env_file = _project_root / ".env"
if _env_file.exists():
    load_dotenv(_env_file)
    # Also try loading from package directory as fallback
else:
    load_dotenv()  # Will search up directory tree
from datetime import datetime
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Setup logging before other imports
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"video_analyzer_{datetime.now():%Y%m%d}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)
logger.info("=" * 60)
logger.info("galdr_video_analyzer server starting...")

# Import local modules
from .config import load_config, validate_config
from .plugin_loader import PluginLoader

# Load and validate configuration
try:
    config = load_config()
    validation = validate_config(config)
    
    if validation['issues']:
        for issue in validation['issues']:
            logger.error(f"Config issue: {issue}")
        raise EnvironmentError("Configuration validation failed")
    
    for warning in validation.get('warnings', []):
        logger.warning(f"Config warning: {warning}")
    
    logger.info("Configuration loaded successfully")
    logger.info(f"Cache dir: {config['cache_dir']}")
    logger.info(f"Frames dir: {config['frames_dir']}")
    
except Exception as e:
    logger.error(f"Configuration error: {e}")
    print(f"ERROR: {e}", file=sys.stderr)
    # Don't exit - allow server to start with warnings

# Initialize FastMCP server
mcp = FastMCP(
    "galdr_video_analyzer",
    instructions="""
YouTube Video Analysis MCP Server.

This server provides tools for YouTube video processing and analysis:

**PLAYLIST MONITORING:**
1. **video_get_playlist** - Get list of videos from a YouTube playlist
2. **video_check_new** - Check for new videos since last run (for automation)

**VIDEO EXTRACTION:**
3. **video_extract_metadata** - Get video title, description, duration, etc.
4. **video_extract_transcript** - Get video transcript/captions
5. **video_extract_frames** - Extract key frames from video

**ANALYSIS:**
6. **video_analyze** - Full analysis pipeline (metadata + transcript + frames + vision)
7. **video_batch_process** - Process multiple videos efficiently

**WORKFLOW:**
1. Use video_get_playlist to see what's in a playlist
2. Use video_check_new for daily monitoring (tracks processed videos)
3. Use video_analyze for full processing of individual videos
4. Results are cached and ready for RAG ingestion

Designed for automated content pipelines.
"""
)

# Initialize plugin loader
plugin_loader: Optional[PluginLoader] = None

try:
    plugins_dir = Path(__file__).parent / "tools" / "plugins"
    plugin_loader = PluginLoader(plugins_dir)
    
    # Set context that plugins can access
    plugin_loader.set_context(
        config=config,
        logger=logger
    )
    
    # Discover and load plugins
    discovered = plugin_loader.discover_plugins()
    logger.info(f"Discovered {len(discovered)} plugins: {discovered}")
    
    # Register plugins with FastMCP
    if discovered:
        registered_count = plugin_loader.register_all(mcp)
        logger.info(f"Registered {registered_count} dynamic tools with MCP server")
    else:
        logger.warning("No plugins discovered - check tools/plugins/ directory")
    
except Exception as e:
    logger.error(f"Plugin loading failed: {e}")
    print(f"WARNING: Plugin loading failed: {e}", file=sys.stderr)


# ========================================
# Server Status Tool (Always Available)
# ========================================

@mcp.tool(
    description="Get server status and list of loaded plugins/tools."
)
async def video_server_status() -> dict:
    """
    Get server status and list of loaded tools.
    
    Returns:
        Server status including loaded plugins and configuration
    """
    return {
        'success': True,
        'server': 'galdr_video_analyzer',
        'version': '0.1.0',
        'mode': 'dynamic_plugin',
        'plugins': plugin_loader.list_plugins() if plugin_loader else [],
        'plugin_count': len(plugin_loader.plugins) if plugin_loader else 0,
        'config': {
            'cache_dir': str(config.get('cache_dir', 'not set')),
            'frames_dir': str(config.get('frames_dir', 'not set')),
            'anthropic_key_set': bool(config.get('anthropic_api_key')),
            'frame_interval': config.get('default_frame_interval', 30),
            'max_frames': config.get('max_frames', 10)
        }
    }


# Cleanup handler
@atexit.register
def cleanup():
    """Clean up resources on shutdown."""
    logger.info("Shutting down galdr_video_analyzer server...")
    # Add any cleanup logic here
    logger.info("Shutdown complete")


def main():
    """
    Main entry point for the MCP server.
    
    Transport mode controlled by MCP_TRANSPORT environment variable:
    - stdio (default): Standard I/O for IDE integration
    - sse: Server-Sent Events over HTTP
    - streamable-http: Full HTTP transport
    """
    transport = os.getenv('MCP_TRANSPORT', 'stdio').lower()
    
    if transport == 'stdio':
        logger.info("Starting galdr_video_analyzer MCP server (stdio transport)")
        logger.info(f"Loaded {len(plugin_loader.plugins) if plugin_loader else 0} dynamic tools")
        mcp.run(transport='stdio')
    
    elif transport in ('sse', 'streamable-http'):
        host = os.getenv('MCP_HOST', '127.0.0.1')
        port = int(os.getenv('MCP_PORT', '8080'))
        
        logger.info(f"Starting galdr_video_analyzer MCP server ({transport} transport)")
        logger.info(f"Listening on http://{host}:{port}")
        logger.info(f"Loaded {len(plugin_loader.plugins) if plugin_loader else 0} dynamic tools")
        
        # Import uvicorn for HTTP server
        try:
            import uvicorn
        except ImportError:
            logger.error("uvicorn required for HTTP transport. Install: pip install uvicorn")
            print("ERROR: uvicorn required. Install: pip install uvicorn", file=sys.stderr)
            sys.exit(1)
        
        # Get the appropriate Starlette app
        if transport == 'sse':
            mcp_app = mcp.sse_app()
        else:
            mcp_app = mcp.streamable_http_app()
        
        # Wrap with health check endpoint
        from starlette.applications import Starlette
        from starlette.responses import JSONResponse
        from starlette.routing import Route, Mount
        
        async def health_check(request):
            """Health check endpoint for Docker/monitoring."""
            return JSONResponse({
                'status': 'healthy',
                'server': 'galdr_video_analyzer',
                'transport': transport,
                'plugins': len(plugin_loader.plugins) if plugin_loader else 0
            })
        
        # Create wrapper app
        app = Starlette(routes=[
            Route('/health', health_check, methods=['GET']),
            Mount('/', app=mcp_app),
        ])
        
        logger.info("Health check endpoint available at /health")
        uvicorn.run(app, host=host, port=port, log_level="info")
    
    else:
        logger.error(f"Unknown transport mode: {transport}")
        print(f"ERROR: Unknown transport '{transport}'. Use: stdio, sse, or streamable-http", file=sys.stderr)
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
