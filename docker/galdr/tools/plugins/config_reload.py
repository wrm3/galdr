"""
Config Reload Tool Plugin

Hot-reload API keys without restarting Docker.
Pass new key values directly — they update the in-memory config dict
shared by all plugins (video_analyze, rag_search, etc.) immediately.

No Docker rebuild, no volume mount, no restart needed.
"""
import os
import logging
from typing import Optional

TOOL_NAME = "config_reload"

TOOL_DESCRIPTION = (
    "Hot-reload API keys without restarting Docker. "
    "Pass new key values directly to update all in-memory configs. "
    "Call with no arguments to see current key status. "
    "Example: config_reload(anthropic_api_key='sk-ant-...')"
)

TOOL_PARAMS = {
    "anthropic_api_key": "New Anthropic API key (optional)",
    "openai_api_key": "New OpenAI API key (optional)",
    "gemini_api_key": "New Gemini API key (optional)",
    "perplexity_api_key": "New Perplexity API key (optional)",
    "show_keys": "Show first 10 chars of each key for verification (default: True)",
}

_config = None
_logger = logging.getLogger(__name__)

KEY_MAP = {
    'anthropic_api_key': 'ANTHROPIC_API_KEY',
    'openai_api_key': 'OPENAI_API_KEY',
    'gemini_api_key': 'GEMINI_API_KEY',
    'perplexity_api_key': 'PERPLEXITY_API_KEY',
}


def setup(context: dict):
    global _config
    _config = context.get('config', {})


async def execute(
    anthropic_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    gemini_api_key: Optional[str] = None,
    perplexity_api_key: Optional[str] = None,
    show_keys: bool = True,
) -> dict:
    updates = {}
    if anthropic_api_key:
        updates['anthropic_api_key'] = anthropic_api_key
    if openai_api_key:
        updates['openai_api_key'] = openai_api_key
    if gemini_api_key:
        updates['gemini_api_key'] = gemini_api_key
    if perplexity_api_key:
        updates['perplexity_api_key'] = perplexity_api_key

    changed = []
    for config_key, new_val in updates.items():
        old_val = _config.get(config_key, '') or ''
        if old_val != new_val:
            _config[config_key] = new_val
            os.environ[KEY_MAP[config_key]] = new_val
            changed.append(config_key)
            _logger.info(f"Updated {config_key}")

    result = {
        "success": True,
        "changed": changed,
        "unchanged_count": len(KEY_MAP) - len(changed),
        "mode": "update" if updates else "status-only",
    }

    if show_keys:
        result["key_status"] = {}
        for config_key in KEY_MAP:
            val = _config.get(config_key, '')
            if val:
                result["key_status"][config_key] = val[:10] + "..." + f" ({len(val)} chars)"
            else:
                result["key_status"][config_key] = "(not set)"

    if changed:
        _logger.info(f"Config hot-reloaded. Changed: {changed}")
    else:
        _logger.info("Config status check (no changes)")

    return result
