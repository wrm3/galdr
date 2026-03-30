"""
Dynamic Plugin Loader for galdr_video_analyzer.

Discovers and loads tool plugins from the tools/plugins/ directory.
Each plugin file should define:
    - TOOL_NAME: str - The MCP tool name
    - TOOL_DESCRIPTION: str - Tool description for MCP
    - TOOL_PARAMS: dict - Parameter descriptions (optional)
    - setup(context: dict) - Called once with shared context
    - execute(**kwargs) - The async function to run

Based on fsGALDR_mcp_rag_docker plugin pattern.
"""
import logging
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from functools import wraps

logger = logging.getLogger(__name__)


class PluginLoader:
    """
    Dynamic plugin loader for MCP tools.
    
    Usage:
        loader = PluginLoader(plugins_dir)
        loader.set_context(config=config, ...)
        loader.discover_plugins()
        loader.register_all(mcp_server)
    """
    
    def __init__(self, plugins_dir: Path):
        """
        Initialize plugin loader.
        
        Args:
            plugins_dir: Path to directory containing plugin .py files
        """
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.context: Dict[str, Any] = {}
    
    def set_context(self, **kwargs) -> None:
        """
        Set context that will be passed to plugin setup() functions.
        
        Args:
            **kwargs: Key-value pairs to include in context
        """
        self.context.update(kwargs)
        logger.info(f"Plugin context set with keys: {list(self.context.keys())}")
    
    def discover_plugins(self) -> List[str]:
        """
        Discover plugin files in the plugins directory.
        
        Returns:
            List of discovered plugin names
        """
        discovered = []
        
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return discovered
        
        for plugin_file in self.plugins_dir.glob("*.py"):
            # Skip __init__.py and files starting with _
            if plugin_file.name.startswith("_"):
                continue
            
            plugin_name = plugin_file.stem
            
            try:
                # Load the module
                spec = importlib.util.spec_from_file_location(
                    f"plugin_{plugin_name}",
                    plugin_file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Validate required attributes
                    if not hasattr(module, 'TOOL_NAME'):
                        logger.warning(f"Plugin {plugin_name} missing TOOL_NAME, skipping")
                        continue
                    
                    if not hasattr(module, 'execute'):
                        logger.warning(f"Plugin {plugin_name} missing execute(), skipping")
                        continue
                    
                    # Store plugin info
                    self.plugins[plugin_name] = {
                        'module': module,
                        'file': plugin_file,
                        'tool_name': getattr(module, 'TOOL_NAME'),
                        'description': getattr(module, 'TOOL_DESCRIPTION', ''),
                        'params': getattr(module, 'TOOL_PARAMS', {}),
                        'execute': getattr(module, 'execute'),
                        'setup': getattr(module, 'setup', None)
                    }
                    
                    discovered.append(plugin_name)
                    logger.info(f"Discovered plugin: {plugin_name} -> {self.plugins[plugin_name]['tool_name']}")
                    
            except Exception as e:
                logger.exception(f"Failed to load plugin {plugin_name}: {e}")
        
        return discovered
    
    def register_all(self, mcp_server) -> int:
        """
        Register all discovered plugins with the MCP server.
        
        Args:
            mcp_server: FastMCP server instance
            
        Returns:
            Number of successfully registered plugins
        """
        registered = 0
        
        for plugin_name, plugin_info in self.plugins.items():
            try:
                # Call setup if defined
                if plugin_info['setup']:
                    plugin_info['setup'](self.context)
                    logger.debug(f"Called setup() for {plugin_name}")
                
                # Create the tool wrapper
                execute_fn = plugin_info['execute']
                tool_name = plugin_info['tool_name']
                description = plugin_info['description']
                
                # Register with MCP
                # Use the tool decorator programmatically
                decorated = mcp_server.tool(
                    name=tool_name,
                    description=description
                )(execute_fn)
                
                registered += 1
                logger.info(f"Registered tool: {tool_name}")
                
            except Exception as e:
                logger.exception(f"Failed to register plugin {plugin_name}: {e}")
        
        return registered
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """
        List all loaded plugins.
        
        Returns:
            List of plugin info dictionaries
        """
        return [
            {
                'name': name,
                'tool_name': info['tool_name'],
                'description': info['description'][:100] + '...' if len(info['description']) > 100 else info['description']
            }
            for name, info in self.plugins.items()
        ]
