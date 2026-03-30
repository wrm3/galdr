"""
Dynamic Tool Plugin Loader for galdr MCP Server.

Scans the tools/plugins directory for plugin files and dynamically registers
them with the FastMCP server at startup.

Plugin Convention:
    Each plugin file must define:
    - TOOL_NAME: str - Unique tool name
    - TOOL_DESCRIPTION: str - Description for MCP clients
    - execute: async function - The tool implementation

    Optional:
    - TOOL_PARAMS: dict - Parameter descriptions for documentation
    - setup: function - Called once during loading with server context
"""
import os
import sys
import importlib
import importlib.util
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LoadedPlugin:
    """Represents a loaded tool plugin."""
    name: str
    description: str
    execute_fn: Callable
    file_path: Path
    params: Optional[Dict[str, Any]] = None


class PluginLoader:
    """
    Dynamic plugin loader for MCP tools.

    Scans a directory for Python files following the plugin convention
    and registers them with FastMCP.

    Usage:
        loader = PluginLoader(tools_dir="tools/plugins")
        loader.discover_plugins()
        loader.register_all(mcp, context)
    """

    REQUIRED_ATTRS = ['TOOL_NAME', 'TOOL_DESCRIPTION', 'execute']

    def __init__(self, tools_dir: Optional[Path] = None):
        """
        Initialize the plugin loader.

        Args:
            tools_dir: Directory to scan for plugins.
                      Defaults to tools/plugins/ relative to this module.
        """
        if tools_dir is None:
            tools_dir = Path(__file__).parent / "tools" / "plugins"

        self.tools_dir = Path(tools_dir)
        self.plugins: Dict[str, LoadedPlugin] = {}
        self._context: Dict[str, Any] = {}

        logger.info(f"PluginLoader initialized with tools_dir: {self.tools_dir}")

    def set_context(self, **kwargs) -> None:
        """
        Set shared context that will be passed to plugin execute functions.

        Args:
            **kwargs: Context variables (e.g., db=db, embedding_generator=eg)
        """
        self._context.update(kwargs)
        logger.info(f"Plugin context set with keys: {list(self._context.keys())}")

    def _preload_utils(self) -> None:
        """
        Preload utility modules (files starting with _ but not __).

        These are shared helper modules imported by plugins via relative
        imports (e.g. ``from ._GALDR_shared import ...``). They must be
        registered in sys.modules as ``galdr.plugins.<stem>`` *before* any
        plugin that imports them is loaded, and their __package__ must be set
        so that relative imports resolve correctly.
        """
        for file_path in self.tools_dir.glob("_*.py"):
            if file_path.name.startswith("__"):
                continue
            module_name = f"galdr.plugins.{file_path.stem}"
            if module_name in sys.modules:
                continue  # already loaded
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None or spec.loader is None:
                    logger.warning(f"Could not create spec for utility: {file_path.name}")
                    continue
                mod = importlib.util.module_from_spec(spec)
                mod.__package__ = "galdr.plugins"
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)
                logger.info(f"Preloaded utility module: {file_path.name} as {module_name}")
            except Exception as e:
                logger.error(f"Failed to preload utility {file_path.name}: {e}")

    def discover_plugins(self) -> List[str]:
        """
        Scan the tools directory and load all valid plugins.

        Returns:
            List of successfully loaded plugin names
        """
        if not self.tools_dir.exists():
            logger.warning(f"Plugins directory does not exist: {self.tools_dir}")
            self.tools_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created plugins directory: {self.tools_dir}")
            return []

        # Preload shared utility modules (_*.py) before any plugin that might
        # import them via relative imports
        self._preload_utils()

        loaded = []

        # Use recursive glob to find plugins in subdirectories too — sorted alphabetically
        for file_path in sorted(self.tools_dir.glob("**/*.py")):
            # Skip __init__.py and files starting with _
            if file_path.name.startswith("_"):
                continue

            try:
                plugin = self._load_plugin_file(file_path)
                if plugin:
                    self.plugins[plugin.name] = plugin
                    loaded.append(plugin.name)
                    logger.info(f"Loaded plugin: {plugin.name} from {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin from {file_path.name}: {e}")

        logger.info(f"Discovered {len(loaded)} plugins: {loaded}")
        return loaded

    def _load_plugin_file(self, file_path: Path) -> Optional[LoadedPlugin]:
        """
        Load a single plugin file.

        Args:
            file_path: Path to the plugin Python file

        Returns:
            LoadedPlugin if valid, None otherwise
        """
        # Create a unique module name
        module_name = f"galdr.plugins.{file_path.stem}"

        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            logger.warning(f"Could not load spec for {file_path}")
            return None

        module = importlib.util.module_from_spec(spec)
        module.__package__ = "galdr.plugins"  # enables relative imports (e.g. from ._GALDR_shared import ...)
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            logger.error(f"Error executing module {file_path.name}: {e}")
            del sys.modules[module_name]
            return None

        # Validate required attributes
        for attr in self.REQUIRED_ATTRS:
            if not hasattr(module, attr):
                logger.warning(f"Plugin {file_path.name} missing required attribute: {attr}")
                return None

        # Extract plugin info
        tool_name = getattr(module, 'TOOL_NAME')
        tool_description = getattr(module, 'TOOL_DESCRIPTION')
        execute_fn = getattr(module, 'execute')
        tool_params = getattr(module, 'TOOL_PARAMS', None)

        # Call setup if it exists
        if hasattr(module, 'setup'):
            try:
                module.setup(self._context)
            except Exception as e:
                logger.error(f"Plugin {tool_name} setup failed: {e}")

        return LoadedPlugin(
            name=tool_name,
            description=tool_description,
            execute_fn=execute_fn,
            file_path=file_path,
            params=tool_params
        )

    def register_all(self, mcp) -> int:
        """
        Register all loaded plugins with the FastMCP server.

        Args:
            mcp: FastMCP server instance

        Returns:
            Number of successfully registered tools
        """
        registered = 0

        for name, plugin in self.plugins.items():
            try:
                # Create a wrapper that injects context
                wrapped_fn = self._create_context_wrapper(plugin.execute_fn)

                # Register with FastMCP
                mcp.add_tool(
                    fn=wrapped_fn,
                    name=plugin.name,
                    description=plugin.description
                )
                registered += 1
                logger.info(f"Registered tool: {plugin.name}")

            except Exception as e:
                logger.error(f"Failed to register tool {name}: {e}")

        logger.info(f"Registered {registered}/{len(self.plugins)} plugins as MCP tools")
        return registered

    def _create_context_wrapper(self, fn: Callable) -> Callable:
        """
        Create a wrapper function that injects context into plugin execute calls.

        The wrapper checks if the function accepts a 'context' parameter
        and injects it if so.
        """
        import inspect
        sig = inspect.signature(fn)
        accepts_context = 'context' in sig.parameters

        if accepts_context:
            async def wrapper(*args, **kwargs):
                kwargs['context'] = self._context
                return await fn(*args, **kwargs)

            # Preserve function signature for FastMCP (minus context)
            params = [p for name, p in sig.parameters.items() if name != 'context']
            wrapper.__signature__ = sig.replace(parameters=params)
            wrapper.__name__ = fn.__name__
            wrapper.__doc__ = fn.__doc__

            return wrapper
        else:
            return fn

    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        Get information about all loaded plugins.

        Returns:
            List of plugin info dictionaries
        """
        return [
            {
                "name": p.name,
                "description": p.description,
                "file": p.file_path.name,
                "params": p.params
            }
            for p in self.plugins.values()
        ]

    def reload_plugin(self, name: str) -> bool:
        """
        Reload a specific plugin from disk.

        Args:
            name: Plugin name to reload

        Returns:
            True if successful, False otherwise
        """
        if name not in self.plugins:
            logger.warning(f"Plugin not found: {name}")
            return False

        plugin = self.plugins[name]
        file_path = plugin.file_path

        # Remove old module from sys.modules
        module_name = f"galdr.plugins.{file_path.stem}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        # Reload
        new_plugin = self._load_plugin_file(file_path)
        if new_plugin:
            self.plugins[name] = new_plugin
            logger.info(f"Reloaded plugin: {name}")
            return True

        return False
