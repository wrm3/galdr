"""
Plugin tools for galdr_video_analyzer.

Each .py file in this directory (except those starting with _) is loaded as a plugin.

Required plugin structure:
    TOOL_NAME = "my_tool_name"
    TOOL_DESCRIPTION = "What this tool does"
    TOOL_PARAMS = {"param1": "description", ...}  # Optional
    
    def setup(context: dict):
        # Called once with shared context (config, logger, etc.)
        pass
    
    async def execute(**kwargs) -> dict:
        # Main tool logic
        return {"success": True, "data": ...}
"""
