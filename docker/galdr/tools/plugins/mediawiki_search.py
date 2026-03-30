"""
MediaWiki Search Tool Plugin

Search for pages in a MediaWiki instance.
"""
import logging
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "mediawiki_search"

TOOL_DESCRIPTION = (
    "Search for pages in a MediaWiki instance. "
    "Returns matching pages with titles and snippets. "
    "Requires MEDIAWIKI_URL configuration."
)

TOOL_PARAMS = {
    "query": "The search query (required)",
    "limit": "Maximum number of results (default: 10)",
    "namespace": "Namespace to search in (optional, 0 = main namespace)"
}


logger = logging.getLogger(__name__)

# ============================================================
# PLUGIN IMPLEMENTATION
# ============================================================

_config = None


def setup(context: dict):
    """Called once during plugin loading to set up dependencies."""
    global _config
    _config = context.get('config', {})


async def execute(
    query: str,
    limit: int = 10,
    namespace: Optional[int] = None,
    context: dict = None
) -> dict:
    """
    Search for pages in MediaWiki.
    """
    import requests

    config = context.get('config', _config) if context else _config

    base_url = config.get('mediawiki_url')
    if not base_url:
        return {
            'success': False,
            'error': 'MediaWiki not configured. Set MEDIAWIKI_URL.'
        }

    api_url = urljoin(base_url.rstrip('/') + '/', 'api.php')
    logger.info(f"MediaWiki search for: {query}")

    try:
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'srlimit': min(limit, 50),  # MediaWiki typically limits to 50
            'format': 'json'
        }

        if namespace is not None:
            params['srnamespace'] = namespace

        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()

        search_results = result.get('query', {}).get('search', [])

        # Format results
        formatted_results = []
        for item in search_results:
            formatted_results.append({
                'title': item.get('title', ''),
                'snippet': item.get('snippet', ''),
                'page_id': item.get('pageid'),
                'size': item.get('size'),
                'word_count': item.get('wordcount'),
                'timestamp': item.get('timestamp'),
                'page_url': f"{base_url.rstrip('/')}/index.php?title={item.get('title', '').replace(' ', '_')}"
            })

        return {
            'success': True,
            'query': query,
            'results': formatted_results,
            'total_results': len(formatted_results),
            'search_info': result.get('query', {}).get('searchinfo', {})
        }

    except Exception as e:
        logger.error(f"MediaWiki search failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'query': query
        }
