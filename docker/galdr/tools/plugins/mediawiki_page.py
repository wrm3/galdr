"""
MediaWiki Page Operations Tool Plugin

Create, read, update, and check MediaWiki pages.
"""
import logging
from typing import Optional, Dict, Any
from urllib.parse import urljoin

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "mediawiki_page"

TOOL_DESCRIPTION = (
    "Create, read, update, or check MediaWiki pages. "
    "Supports CRUD operations on MediaWiki instances via Action API. "
    "Requires MEDIAWIKI_URL, MEDIAWIKI_USERNAME, and MEDIAWIKI_PASSWORD configuration."
)

TOOL_PARAMS = {
    "action": "Operation: 'create', 'read', 'update', 'exists' (required)",
    "title": "The page title (required)",
    "content": "Page content in WikiText format (required for create/update)",
    "summary": "Edit summary (optional, for create/update)"
}


logger = logging.getLogger(__name__)

# ============================================================
# PLUGIN IMPLEMENTATION
# ============================================================

_config = None
_api_client = None


def setup(context: dict):
    """Called once during plugin loading to set up dependencies."""
    global _config, _api_client
    _config = context.get('config', {})

    # Initialize MediaWiki API client if credentials available
    _api_client = _initialize_client(_config)


def _initialize_client(config: dict):
    """Initialize MediaWiki API client."""
    base_url = config.get('mediawiki_url')
    username = config.get('mediawiki_username')
    password = config.get('mediawiki_password')
    api_key = config.get('mediawiki_api_key')

    if base_url and username and (password or api_key):
        return MediaWikiClient(
            base_url=base_url,
            username=username,
            password=password,
            api_key=api_key
        )
    return None


async def execute(
    action: str,
    title: str,
    content: Optional[str] = None,
    summary: Optional[str] = None,
    context: dict = None
) -> dict:
    """
    Perform MediaWiki page operations.
    """
    config = context.get('config', _config) if context else _config
    client = _api_client or _initialize_client(config)

    if not client:
        return {
            'success': False,
            'error': 'MediaWiki not configured. Set MEDIAWIKI_URL, MEDIAWIKI_USERNAME, and MEDIAWIKI_PASSWORD.'
        }

    action = action.lower()
    logger.info(f"MediaWiki {action} for page: {title}")

    try:
        if action == 'create':
            if not content:
                return {'success': False, 'error': 'Content required for create operation'}
            return await _create_page(client, title, content, summary or "Created via galdr")

        elif action == 'read':
            return await _read_page(client, title)

        elif action == 'update':
            if not content:
                return {'success': False, 'error': 'Content required for update operation'}
            return await _update_page(client, title, content, summary or "Updated via galdr")

        elif action == 'exists':
            return await _check_exists(client, title)

        else:
            return {'success': False, 'error': f"Invalid action: {action}. Use 'create', 'read', 'update', or 'exists'."}

    except Exception as e:
        logger.error(f"MediaWiki operation failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'action': action,
            'title': title
        }


async def _create_page(client, title: str, content: str, summary: str) -> dict:
    """Create a new MediaWiki page."""
    if client.page_exists(title):
        return {
            'success': False,
            'error': f"Page '{title}' already exists. Use action='update' to modify it."
        }

    success = client.create_or_update_page(title, content, summary)
    if success:
        return {
            'success': True,
            'action': 'created',
            'title': title,
            'page_url': client.get_page_url(title),
            'message': f"Successfully created page: {title}"
        }
    else:
        return {'success': False, 'error': 'Failed to create page'}


async def _read_page(client, title: str) -> dict:
    """Read a MediaWiki page."""
    content = client.get_page_content(title)
    if content is not None:
        return {
            'success': True,
            'action': 'read',
            'title': title,
            'content': content,
            'page_url': client.get_page_url(title)
        }
    else:
        return {
            'success': False,
            'error': f"Page '{title}' not found"
        }


async def _update_page(client, title: str, content: str, summary: str) -> dict:
    """Update an existing MediaWiki page."""
    if not client.page_exists(title):
        return {
            'success': False,
            'error': f"Page '{title}' does not exist. Use action='create' to create it."
        }

    success = client.create_or_update_page(title, content, summary)
    if success:
        return {
            'success': True,
            'action': 'updated',
            'title': title,
            'page_url': client.get_page_url(title),
            'message': f"Successfully updated page: {title}"
        }
    else:
        return {'success': False, 'error': 'Failed to update page'}


async def _check_exists(client, title: str) -> dict:
    """Check if a MediaWiki page exists."""
    exists = client.page_exists(title)
    return {
        'success': True,
        'action': 'exists',
        'title': title,
        'exists': exists,
        'page_url': client.get_page_url(title) if exists else None
    }


# ============================================================
# MEDIAWIKI API CLIENT
# ============================================================

class MediaWikiClient:
    """Simple MediaWiki Action API client."""

    def __init__(self, base_url: str, username: str, password: str = None, api_key: str = None):
        import requests

        self.base_url = base_url.rstrip('/')
        self.api_url = urljoin(self.base_url + '/', 'api.php')
        self.username = username
        self.password = password
        self.api_key = api_key
        self.session = requests.Session()
        self.csrf_token = None
        self.logged_in = False

        self.session.headers.update({
            'User-Agent': 'galdr/1.0'
        })

    def get_page_url(self, title: str) -> str:
        """Get the URL for a page."""
        return f"{self.base_url}/index.php?title={title.replace(' ', '_')}"

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the MediaWiki API."""
        response = self.session.post(self.api_url, data=params)
        response.raise_for_status()
        return response.json()

    def login(self) -> bool:
        """Login to MediaWiki."""
        try:
            # Get login token
            login_token = self._get_token('login')

            if self.api_key:
                login_params = {
                    'action': 'clientlogin',
                    'loginreturnurl': self.base_url,
                    'logintoken': login_token,
                    'username': self.username,
                    'password': self.api_key,
                    'format': 'json'
                }
            else:
                login_params = {
                    'action': 'login',
                    'lgname': self.username,
                    'lgpassword': self.password,
                    'lgtoken': login_token,
                    'format': 'json'
                }

            result = self._make_request(login_params)

            if result.get('login', {}).get('result') == 'Success':
                self.logged_in = True
                logger.info(f"Logged in as {self.username}")
                return True
            else:
                logger.error(f"Login failed: {result.get('login', {})}")
                return False

        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    def _get_token(self, token_type: str = 'csrf') -> str:
        """Get a token from MediaWiki API."""
        params = {
            'action': 'query',
            'meta': 'tokens',
            'type': token_type,
            'format': 'json'
        }

        result = self._make_request(params)
        token = result.get('query', {}).get('tokens', {}).get(f'{token_type}token', '')

        if token_type == 'csrf':
            self.csrf_token = token

        return token

    def get_page_content(self, title: str) -> Optional[str]:
        """Get the content of a MediaWiki page."""
        params = {
            'action': 'query',
            'prop': 'revisions',
            'titles': title,
            'rvprop': 'content',
            'format': 'json'
        }

        result = self._make_request(params)
        pages = result.get('query', {}).get('pages', {})

        for page_id, page_data in pages.items():
            if page_id != '-1':
                revisions = page_data.get('revisions', [])
                if revisions:
                    return revisions[0].get('*', '')

        return None

    def page_exists(self, title: str) -> bool:
        """Check if a page exists."""
        params = {
            'action': 'query',
            'titles': title,
            'format': 'json'
        }

        result = self._make_request(params)
        pages = result.get('query', {}).get('pages', {})

        for page_id in pages.keys():
            if page_id != '-1':
                return True

        return False

    def create_or_update_page(self, title: str, content: str, summary: str) -> bool:
        """Create or update a MediaWiki page."""
        if not self.logged_in:
            if not self.login():
                return False

        if not self.csrf_token:
            self._get_token('csrf')

        params = {
            'action': 'edit',
            'title': title,
            'text': content,
            'summary': summary,
            'token': self.csrf_token,
            'format': 'json'
        }

        result = self._make_request(params)

        if result.get('edit', {}).get('result') == 'Success':
            logger.info(f"Created/updated page: {title}")
            return True
        else:
            logger.error(f"Failed to create/update page: {result}")
            return False
