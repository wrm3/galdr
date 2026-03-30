"""
Shared utilities for galdr_install, galdr_update, and galdr_plan_reset plugins.

This module is NOT a plugin (underscore prefix prevents auto-loading).
Import it directly in each galdr plugin file.
"""
import os
import sys
import logging
import platform
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ============================================================
# TOKEN AND REPO DEFAULTS
# ============================================================

# GitHub token for accessing the wrm3/galdr repo.
# For public repos, no token is needed for basic operations.
# Set GITHUB_TOKEN in your environment if you need authenticated access.
DEFAULT_GITHUB_TOKEN = ""

DEFAULT_GITHUB_REPO = "wrm3/galdr"


def get_github_token() -> str:
    """Return GitHub token: env var first, bundled default as fallback."""
    return os.environ.get("GITHUB_TOKEN") or DEFAULT_GITHUB_TOKEN


def get_github_repo() -> str:
    """Return GitHub repo slug from env var or default."""
    return os.environ.get("GITHUB_REPO") or DEFAULT_GITHUB_REPO


# ============================================================
# INSTALL MANIFESTS
# ============================================================

# ── Full install — all systems + .galdr template ──────────────────────────────
# All paths are relative to the template/ subfolder in the repo.
# The installer strips "template/" when writing to the target project.
TEMPLATE_PREFIX = "template/"

FULL_MANIFEST: List[str] = [
    # IDE Configurations
    'template/.agent',                   # Google Antigravity / Gemini
    'template/.claude',                  # Claude Code
    'template/.cursor',                  # Cursor IDE
    'template/.platforms',   # Cross-platform architecture docs

    # Scaffold folders (contain .gitkeep so they deploy to target projects)
    'template/docs',
    'template/research',
    'template/temp_scripts',

    # Root files
    'template/.gitignore',               # galdr-required gitignore patterns (merged)
    'template/agents.md',                # Universal agent instructions  (merged)
    'template/CLAUDE.md',                # Claude-specific context        (merged)
    'template/GEMINI.md',
    'template/GUARDRAILS.md',
    'template/LICENSE',
    'template/LICENSE',
    'template/NOTICE',
    'template/NOTICE',

    # .galdr/ blank template — blank root files, empty tasks/phases,
    # examples/ and reference/ included. No live task data.
    'template/.galdr',
]

# ── IDE-only manifests (platform-specific installs, never touch .galdr/) ──────

# Cursor IDE — rules, skills, agents, commands, hooks + shared root files
# NOTE: CLAUDE.md is NOT included — it is Claude Code-specific, not read by Cursor.
CURSOR_MANIFEST: List[str] = [
    'template/.cursor',
    'template/.platforms',
    'template/docs',
    'template/research',
    'template/temp_scripts',
    'template/.gitignore',               # galdr-required gitignore patterns (merged)
    'template/agents.md',                # universal agent instructions (merged)
    'template/GUARDRAILS.md',
    'template/LICENSE',
    'template/LICENSE',
    'template/NOTICE',
    'template/NOTICE',
]

# Claude Code — rules, skills, agents, commands, hooks + root files
# agents.md: explicitly says "Compatible with both Cursor and Claude Code"
# CURSOR_SETUP.md: intentionally excluded — Cursor-specific
CLAUDE_MANIFEST: List[str] = [
    'template/.claude',
    'template/.platforms',
    'template/docs',
    'template/research',
    'template/temp_scripts',
    'template/.gitignore',               # galdr-required gitignore patterns (merged)
    'template/agents.md',                # universal agent instructions (merged)
    'template/CLAUDE.md',                # Claude-specific context (merged)
    'template/GUARDRAILS.md',
    'template/LICENSE',
    'template/LICENSE',
    'template/NOTICE',
    'template/NOTICE',
]

# Google Antigravity / Gemini — rules, skills, workflows + root files
# agents.md: GEMINI.md explicitly says "See AGENTS.md for universal instructions"
# CLAUDE.md: excluded — Claude Code-specific
GEMINI_MANIFEST: List[str] = [
    'template/.agent',
    'template/.platforms',
    'template/docs',
    'template/research',
    'template/temp_scripts',
    'template/.gitignore',               # galdr-required gitignore patterns (merged)
    'template/agents.md',                # universal agent instructions (merged)
    'template/GEMINI.md',
    'template/GUARDRAILS.md',
    'template/LICENSE',
    'template/LICENSE',
    'template/NOTICE',
    'template/NOTICE',
]

# All-platforms IDE manifest — everything in FULL_MANIFEST except .galdr/
# Used by galdr_install phase 1 (force-overwrite IDE configs while leaving .galdr/ alone)
RULES_MANIFEST: List[str] = [item for item in FULL_MANIFEST if item != 'template/.galdr']

# .galdr-only manifest — for plan reset
GALDR_MANIFEST: List[str] = ['template/.galdr']

# ── templates manifests (vNext — autonomous multi-agent support) ────────────
# All paths are relative to the templates/ subfolder in the repo.
# The installer strips "templates/" when writing to the target project.
templates_PREFIX = "templates/"

FULL_MANIFEST_V2: List[str] = [
    # IDE Configurations
    'templates/.agent',
    'templates/.claude',
    'templates/.cursor',
    'templates/.platforms',

    # Scaffold folders
    'templates/docs',
    'templates/research',
    'templates/temp_scripts',

    # Root files
    'templates/.gitignore',              # galdr-required gitignore patterns (merged)
    'templates/agents.md',
    'templates/CLAUDE.md',
    'templates/GEMINI.md',
    'templates/GUARDRAILS.md',
    'templates/LICENSE',
    'templates/NOTICE',

    # .galdr/ blank template — vNext version with ARCHITECTURE_CONSTRAINTS.md,
    # SPRINT.md, CLEANUP_REPORT.md, SYSTEM_EXPERIMENTS.md, etc.
    'templates/.galdr',
]

CURSOR_MANIFEST_V2: List[str] = [
    'templates/.cursor',
    'templates/.platforms',
    'templates/docs',
    'templates/research',
    'templates/temp_scripts',
    'templates/.gitignore',              # galdr-required gitignore patterns (merged)
    'templates/agents.md',
    'templates/GUARDRAILS.md',
    'templates/LICENSE',
    'templates/NOTICE',
]

CLAUDE_MANIFEST_V2: List[str] = [
    'templates/.claude',
    'templates/.platforms',
    'templates/docs',
    'templates/research',
    'templates/temp_scripts',
    'templates/.gitignore',              # galdr-required gitignore patterns (merged)
    'templates/agents.md',
    'templates/CLAUDE.md',
    'templates/GUARDRAILS.md',
    'templates/LICENSE',
    'templates/NOTICE',
]

GEMINI_MANIFEST_V2: List[str] = [
    'templates/.agent',
    'templates/.platforms',
    'templates/docs',
    'templates/research',
    'templates/temp_scripts',
    'templates/.gitignore',              # galdr-required gitignore patterns (merged)
    'templates/agents.md',
    'templates/GEMINI.md',
    'templates/GUARDRAILS.md',
    'templates/LICENSE',
    'templates/NOTICE',
]

# IDE configs only — used by galdr_install phase 1 with v2 template
RULES_MANIFEST_V2: List[str] = [
    item for item in FULL_MANIFEST_V2 if item != 'templates/.galdr'
]

# .galdr-only manifest for v2 — for plan reset / first-time .galdr init
GALDR_MANIFEST_V2: List[str] = ['templates/.galdr']

# Paths that are NEVER extracted to a target project, regardless of manifest.
# Protects internal implementation details from leaking into user projects.
NEVER_EXTRACT: List[str] = [
    'docker',           # MCP server source code — internal only
    'docs',             # Internal project documentation
    'research',         # Internal research files
    'logs',             # Log files
    '.git',             # Git internals
    'temp_scripts',     # Internal test scripts
    '.GALDR_backup',    # Backup archives
    '.env',             # Environment secrets (any .env file)
]

# Files where user content is preserved via section-marker merging.
# the galdr section (between markers) is updated from the template;
# everything outside the markers is left untouched.
MERGEABLE_FILES = {'agents.md', 'claude.md', 'gemini.md', '.gitignore'}

# Files that are NEVER overwritten on upgrade — only installed if missing.
# These accumulate user-specific content over time (learned guardrails, etc.).
SKIP_IF_EXISTS_FILES = {'guardrails.md'}


# ============================================================
# GITHUB API — ZIP-BASED (fast: 1 request vs 300+ sequential calls)
# ============================================================

def download_repo_zip(repo: str, token: str, ref: str = 'main') -> bytes:
    """
    Download the entire GitHub repository as a ZIP archive in a single request.

    Much faster than the Contents API for bulk installs — one network round-trip
    instead of hundreds of sequential calls.

    Returns raw ZIP bytes.
    Raises urllib.error.URLError / HTTPError on failure.
    """
    url = f'https://api.github.com/repos/{repo}/zipball/{ref}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('X-GitHub-Api-Version', '2022-11-28')
    req.add_header('User-Agent', 'galdr-tools/3.0')
    # Generous timeout — repo ZIP can be several MB
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def extract_manifest_from_zip(
    zip_bytes: bytes,
    manifest: List[str],
    target_dir: Path,
    overwrite: bool = True,
) -> Dict[str, Any]:
    """
    Extract files matching manifest paths from a repo ZIP to target_dir.

    GitHub ZIP archives have a top-level directory like:
      wrm3-galdr-abc123/
    This function strips that prefix automatically.

    Manifest entries should be relative to the repo's template/ subfolder
    (e.g. ['template/.cursor', 'template/agents.md']). The "template/" prefix
    is automatically stripped when writing to target_dir, so files land at the
    project root (e.g. target_dir/.cursor/, target_dir/agents.md).

    Args:
        zip_bytes:   Raw bytes of the GitHub ZIP download.
        manifest:    List of repo-relative paths to extract, e.g. ['template/.cursor', 'template/agents.md'].
                     Both individual files and directories are supported.
        target_dir:  Local directory to write files into.
        overwrite:   If False, skip files that already exist locally.

    Returns:
        {'success': bool, 'files_fetched': [str], 'files_skipped': [str], 'errors': [str]}
    """
    import zipfile
    import io

    result: Dict[str, Any] = {
        'success': False,
        'files_fetched': [],
        'files_skipped': [],
        'errors': [],
    }

    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            all_names = zf.namelist()
            if not all_names:
                result['errors'].append("ZIP archive is empty")
                return result

            # Identify and strip the top-level directory prefix (e.g. "wrm3-galdr-abc123/")
            top_prefix = all_names[0].split('/')[0] + '/'

            for member in zf.infolist():
                # Skip directories themselves (we create them on demand)
                if member.filename.endswith('/'):
                    continue

                # Strip repo prefix → repo-relative path
                if not member.filename.startswith(top_prefix):
                    continue
                rel_path = member.filename[len(top_prefix):]
                if not rel_path:
                    continue

                # Hard-block protected paths — never extract these regardless of manifest
                first_segment = rel_path.split('/')[0]
                if any(
                    first_segment == blocked or rel_path.startswith(blocked + '/')
                    for blocked in NEVER_EXTRACT
                ):
                    logger.debug(f"Blocked (protected path): {rel_path}")
                    continue

                # Check if this file matches any manifest entry
                matched = False
                for entry in manifest:
                    entry_norm = entry.lstrip('/')
                    if rel_path == entry_norm or rel_path.startswith(entry_norm + '/'):
                        matched = True
                        break
                if not matched:
                    continue

                # Strip template/ prefix so files land at the project root, not template/
                install_rel_path = rel_path
                if install_rel_path.startswith(TEMPLATE_PREFIX):
                    install_rel_path = install_rel_path[len(TEMPLATE_PREFIX):]
                    if not install_rel_path:
                        continue  # skip the template/ directory entry itself

                local_target = target_dir / install_rel_path

                # Honour overwrite flag
                if not overwrite and local_target.exists():
                    result['files_skipped'].append(str(local_target))
                    logger.debug(f"Skipped (exists): {local_target}")
                    continue

                try:
                    local_target.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as src:
                        local_target.write_bytes(src.read())
                    result['files_fetched'].append(str(local_target))
                    logger.debug(f"Extracted: {rel_path} → {local_target}")
                except Exception as exc:
                    msg = f"Failed to write {rel_path}: {exc}"
                    logger.warning(msg)
                    result['errors'].append(msg)

    except zipfile.BadZipFile as exc:
        result['errors'].append(f"Bad ZIP archive: {exc}")
        return result
    except Exception as exc:
        result['errors'].append(f"ZIP extraction error: {exc}")
        return result

    result['success'] = True
    return result


# ── Legacy Contents API (kept for fetch_from_github callers in galdr_plan_reset) ──

def github_api_request(url: str, token: str) -> Any:
    """Make a single GitHub API GET request and return parsed JSON."""
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('X-GitHub-Api-Version', '2022-11-28')
    req.add_header('User-Agent', 'galdr-tools/3.0')

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))


def fetch_from_github(
    repo: str,
    path: str,
    target_dir: Path,
    token: str,
    strip_prefix: Optional[str] = None,
    exclude_prefixes: Optional[List[str]] = None,
    overwrite: bool = True,
) -> Dict[str, Any]:
    """
    Recursively fetch files from a GitHub repository path via the Contents API.

    NOTE: This is the legacy per-file approach. For bulk installs use
    download_repo_zip() + extract_manifest_from_zip() instead — it is
    dramatically faster (1 request vs hundreds).

    Kept here because galdr_plan_reset uses it for targeted .galdr/ downloads.
    """
    result: Dict[str, Any] = {
        'success': False,
        'files_fetched': [],
        'files_skipped': [],
        'errors': [],
        'error': None,
    }

    api_path = path.strip('/')
    url = f'https://api.github.com/repos/{repo}/contents/{api_path}'

    try:
        data = github_api_request(url, token)
    except urllib.error.HTTPError as exc:
        result['error'] = f"GitHub API HTTP {exc.code} for {url}: {exc.reason}"
        return result
    except urllib.error.URLError as exc:
        result['error'] = f"GitHub network error for {url}: {exc.reason}"
        return result
    except Exception as exc:
        result['error'] = f"GitHub unexpected error for {url}: {exc}"
        return result

    entries = [data] if isinstance(data, dict) else data

    for entry in entries:
        entry_type = entry.get('type')
        entry_path = entry.get('path', '')
        entry_name = entry.get('name', '')

        if exclude_prefixes:
            if any(entry_path == p or entry_path.startswith(p + '/') for p in exclude_prefixes):
                logger.debug(f"Skipping excluded: {entry_path}")
                continue

        rel_path = entry_path
        if strip_prefix and rel_path.startswith(strip_prefix):
            rel_path = rel_path[len(strip_prefix):].lstrip('/')
        local_target = target_dir / rel_path if rel_path else target_dir / entry_name

        if entry_type == 'dir':
            sub = fetch_from_github(
                repo, entry_path, target_dir, token, strip_prefix, exclude_prefixes, overwrite
            )
            result['files_fetched'].extend(sub['files_fetched'])
            result['files_skipped'].extend(sub['files_skipped'])
            result['errors'].extend(sub['errors'])
            if sub.get('error'):
                result['errors'].append(sub['error'])

        elif entry_type == 'file':
            if not overwrite and local_target.exists():
                result['files_skipped'].append(str(local_target))
                logger.debug(f"Skipped (exists): {local_target}")
                continue

            try:
                encoding = entry.get('encoding', 'base64')
                raw_content = entry.get('content', '')

                if encoding == 'base64' and raw_content:
                    file_bytes = base64.b64decode(raw_content)
                else:
                    download_url = entry.get('download_url')
                    if not download_url:
                        result['errors'].append(f"No download_url for {entry_path}")
                        continue
                    req = urllib.request.Request(download_url)
                    req.add_header('Authorization', f'Bearer {token}')
                    req.add_header('User-Agent', 'galdr-tools/3.0')
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        file_bytes = resp.read()

                local_target.parent.mkdir(parents=True, exist_ok=True)
                local_target.write_bytes(file_bytes)
                result['files_fetched'].append(str(local_target))
                logger.debug(f"Fetched: {entry_path} -> {local_target}")

            except Exception as exc:
                msg = f"Failed to write {entry_path}: {exc}"
                logger.warning(msg)
                result['errors'].append(msg)

    result['success'] = True
    return result


# ============================================================
# MARKDOWN MERGE (for agents.md / CLAUDE.md)
# ============================================================

def merge_markdown_file(source_content: str, dest_content: str, filename: str) -> str:
    """
    Merge galdr-managed section from source into dest, preserving all other content.

    For agents.md / CLAUDE.md / GEMINI.md: replaces the galdr marker block
    from source while leaving everything else in dest untouched.

    For .gitignore: same marker-based merge using comment-style markers.
    """
    fname = filename.lower()
    # Strip path components — we only care about the basename
    if '/' in fname:
        fname = fname.rsplit('/', 1)[-1]
    if '\\' in fname:
        fname = fname.rsplit('\\', 1)[-1]

    if fname == 'agents.md':
        start_marker = '<!-- galdr system SECTION -->'
        end_marker = '<!-- END galdr system SECTION -->'
    elif fname == 'claude.md':
        start_marker = '<!-- galdr system CONTEXT -->'
        end_marker = '<!-- END galdr system CONTEXT -->'
    elif fname == 'gemini.md':
        start_marker = '<!-- galdr system CONTEXT -->'
        end_marker = '<!-- END galdr system CONTEXT -->'
    elif fname == '.gitignore':
        start_marker = '# <!-- galdr GITIGNORE SECTION -->'
        end_marker = '# <!-- END galdr GITIGNORE SECTION -->'
    else:
        return source_content

    if start_marker not in source_content:
        # Source has no galdr section — fall back to full overwrite
        return source_content

    # Extract galdr section from source
    src_start = source_content.find(start_marker)
    src_end = source_content.find(end_marker)
    src_end = (src_end + len(end_marker)) if src_end != -1 else len(source_content)
    new_section = source_content[src_start:src_end]

    if start_marker in dest_content:
        # Replace existing galdr section in dest
        dst_start = dest_content.find(start_marker)
        dst_end = dest_content.find(end_marker)
        dst_end = (dst_end + len(end_marker)) if dst_end != -1 else len(dest_content)
        return dest_content[:dst_start] + new_section + dest_content[dst_end:]
    else:
        # Append galdr section to end of dest
        return dest_content.rstrip() + '\n\n' + new_section + '\n'


# ============================================================
# PATH UTILITIES
# ============================================================

def translate_windows_path(path: str) -> str:
    """Translate Windows drive path to Docker /mnt/ path when running in container."""
    import re
    match = re.match(r'^([a-zA-Z]):[/\\](.*)$', path)
    if match:
        drive = match.group(1).lower()
        rest = match.group(2).replace('\\', '/')
        return f'/mnt/{drive}/{rest}'
    return path


def resolve_target_path(target_path: str) -> Path:
    """Translate and resolve the target path, handling Windows/Docker differences."""
    if os.path.exists('/mnt'):
        target_path = translate_windows_path(target_path)
    return Path(target_path).resolve()


# ============================================================
# BACKUP UTILITIES
# ============================================================

def backup_GALDR_dir(GALDR_dir: Path, target_dir: Path) -> dict:
    """
    Create a timestamped zip backup of .galdr/ before destructive operations.

    The backup is saved as .GALDR_backup_YYYYMMDD_HHMMSS.zip in target_dir.
    Also ensures .gitignore excludes the backup pattern (if .gitignore exists).

    Returns:
        {
            'success': bool,
            'backup_path': str | None,
            'backup_name': str | None,
            'file_count': int,
            'backup_size_bytes': int,
            'skipped': bool,          # True if nothing to back up
            'error': str | None,
        }
    """
    import zipfile
    from datetime import datetime

    if not GALDR_dir.exists():
        return {
            'success': True,
            'backup_path': None,
            'backup_name': None,
            'file_count': 0,
            'backup_size_bytes': 0,
            'skipped': True,
            'skip_reason': '.galdr/ does not exist — nothing to back up',
            'error': None,
        }

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'.GALDR_backup_{timestamp}.zip'
    backup_path = target_dir / backup_name

    try:
        files_added = []
        with zipfile.ZipFile(str(backup_path), 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in sorted(GALDR_dir.rglob('*')):
                if file_path.is_file():
                    # Store path relative to target_dir (e.g., .galdr/TASKS.md)
                    arcname = file_path.relative_to(target_dir)
                    zf.write(str(file_path), str(arcname))
                    files_added.append(str(arcname))

        backup_size = backup_path.stat().st_size

        # Keep .gitignore clean — exclude backup zips from commits
        _ensure_gitignore_pattern(target_dir, '.GALDR_backup_*.zip')

        logger.info(
            f"Backed up .galdr/ → {backup_name} "
            f"({len(files_added)} files, {backup_size} bytes)"
        )
        return {
            'success': True,
            'backup_path': str(backup_path),
            'backup_name': backup_name,
            'file_count': len(files_added),
            'backup_size_bytes': backup_size,
            'skipped': False,
            'error': None,
        }

    except Exception as e:
        # Clean up an incomplete zip if it was partially written
        try:
            if backup_path.exists():
                backup_path.unlink()
        except Exception:
            pass
        logger.error(f"backup_GALDR_dir failed: {e}")
        return {
            'success': False,
            'backup_path': None,
            'backup_name': None,
            'file_count': 0,
            'backup_size_bytes': 0,
            'skipped': False,
            'error': str(e),
        }


def _ensure_gitignore_pattern(target_dir: Path, pattern: str) -> None:
    """
    Append pattern to .gitignore in target_dir if not already present.
    Does nothing if .gitignore does not exist (we don't create it).
    """
    gitignore = target_dir / '.gitignore'
    if not gitignore.exists():
        return
    try:
        content = gitignore.read_text(encoding='utf-8')
        if pattern not in content:
            with open(str(gitignore), 'a', encoding='utf-8') as f:
                f.write(f'\n# galdr backup archives\n{pattern}\n')
            logger.info(f"Added '{pattern}' to .gitignore")
    except Exception as e:
        logger.warning(f"Could not update .gitignore with backup pattern: {e}")


def GALDR_dir_has_user_data(GALDR_dir: Path) -> bool:
    """
    Return True if .galdr/ appears to contain real user task data
    (i.e. it has been used, not just installed as a blank template).

    Checks for:
      - Any task*.md files in .galdr/tasks/
      - Any phase*.md files in .galdr/phases/
      - Any task list items (- [ ], - [x], etc.) in TASKS.md
    """
    if not GALDR_dir.exists():
        return False

    tasks_dir = GALDR_dir / 'tasks'
    phases_dir = GALDR_dir / 'phases'

    if tasks_dir.exists():
        task_files = [f for f in tasks_dir.glob('task*.md') if f.name != '.gitkeep']
        if task_files:
            return True

    if phases_dir.exists():
        phase_files = [f for f in phases_dir.glob('phase*.md') if f.name != '.gitkeep']
        if phase_files:
            return True

    tasks_md = GALDR_dir / 'TASKS.md'
    if tasks_md.exists():
        try:
            for line in tasks_md.read_text(encoding='utf-8').splitlines():
                stripped = line.strip()
                # Any markdown task list item indicates user has started populating
                if stripped.startswith('- [') and len(stripped) > 6:
                    return True
        except Exception:
            pass

    return False


# ============================================================
# OS INFO
# ============================================================

def get_os_info() -> dict:
    """Return OS platform information."""
    is_windows = platform.system() == 'Windows'
    can_symlink = False

    if is_windows:
        import tempfile
        try:
            with tempfile.TemporaryDirectory() as tmp:
                src = Path(tmp) / 'test.txt'
                lnk = Path(tmp) / 'link.txt'
                src.write_text('test')
                try:
                    lnk.symlink_to(src)
                    can_symlink = True
                except OSError:
                    can_symlink = False
        except Exception:
            can_symlink = False
    else:
        can_symlink = True

    return {
        'platform': platform.system(),
        'is_windows': is_windows,
        'can_create_symlinks': can_symlink,
        'python_version': sys.version,
        'machine': platform.machine(),
    }


# ============================================================
# CORE INSTALL LOGIC (shared by galdr_install and galdr_update)
# ============================================================

def run_install(
    manifest: List[str],
    target: Path,
    github_repo: str,
    github_token: str,
    force_overwrite: bool,
    dry_run: bool,
    original_target_path: str,
) -> dict:
    """
    Core install logic: download repo ZIP once, extract manifest items to target.

    Uses download_repo_zip() + extract_manifest_from_zip() for speed — one HTTP
    request instead of hundreds of sequential GitHub Contents API calls.

    Mergeable files (agents.md, CLAUDE.md) are handled separately: the source
    content is extracted from the ZIP to a temp buffer, then merged with the
    existing local file to preserve user content outside the galdr markers.

    Returns a result dict suitable for returning from an MCP tool execute().
    """
    import tempfile
    from datetime import datetime

    result = {
        'success': False,
        'target_path': original_target_path,
        'target_path_resolved': str(target),
        'source': f'github:{github_repo}',
        'dry_run': dry_run,
        'manifest_items': len(manifest),
        'copied_files': [],
        'skipped_files': [],
        'merged_files': [],
        'warnings': [],
        'operation_time_seconds': 0,
    }

    if dry_run:
        result['success'] = True
        result['message'] = (
            f"Dry run: would install {len(manifest)} items from {github_repo}"
        )
        for gh_path in manifest:
            result['copied_files'].append({
                'item': gh_path,
                'action': 'would_copy',
                'source': f'https://github.com/{github_repo}/tree/main/{gh_path}',
            })
        return result

    start_time = datetime.now()

    # ── Step 1: Download repo ZIP (single HTTP request) ───────────────────────
    logger.info(f"Downloading repo ZIP from {github_repo}...")
    try:
        zip_bytes = download_repo_zip(github_repo, github_token)
        logger.info(f"ZIP downloaded: {len(zip_bytes):,} bytes")
    except Exception as exc:
        result['error'] = f"Failed to download repo ZIP from {github_repo}: {exc}"
        return result

    # ── Step 2: Bucket manifest entries by handling strategy ─────────────────
    # mergeable: galdr section updated, user content outside markers preserved
    # skip_if_exists: never overwrite (user-owned accumulated content)
    # regular: overwrite or skip according to force_overwrite
    mergeable_in_manifest = [
        p for p in manifest if Path(p).name.lower() in MERGEABLE_FILES
    ]
    skip_if_exists_in_manifest = [
        p for p in manifest
        if Path(p).name.lower() in SKIP_IF_EXISTS_FILES
        and p not in mergeable_in_manifest
    ]
    non_mergeable_manifest = [
        p for p in manifest
        if p not in mergeable_in_manifest
        and p not in skip_if_exists_in_manifest
    ]

    # ── Step 3: Extract regular files ─────────────────────────────────────────
    if non_mergeable_manifest:
        extract_result = extract_manifest_from_zip(
            zip_bytes=zip_bytes,
            manifest=non_mergeable_manifest,
            target_dir=target,
            overwrite=force_overwrite,
        )
        result['copied_files'].extend(extract_result['files_fetched'])
        result['skipped_files'].extend(extract_result['files_skipped'])
        if extract_result['errors']:
            result['warnings'].extend(extract_result['errors'])

    # ── Step 3b: Extract skip-if-exists files (always skip if present) ────────
    if skip_if_exists_in_manifest:
        extract_result = extract_manifest_from_zip(
            zip_bytes=zip_bytes,
            manifest=skip_if_exists_in_manifest,
            target_dir=target,
            overwrite=False,  # Always skip if exists — user-owned content
        )
        result['copied_files'].extend(extract_result['files_fetched'])
        result['skipped_files'].extend(extract_result['files_skipped'])
        if extract_result['errors']:
            result['warnings'].extend(extract_result['errors'])
            result['warnings'].extend(extract_result['errors'])

    # ── Step 4: Handle mergeable files ────────────────────────────────────────
    for gh_path in mergeable_in_manifest:
        dest_item = target / gh_path

        # Extract just this file from the ZIP to a temp buffer
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tmp_result = extract_manifest_from_zip(
                zip_bytes=zip_bytes,
                manifest=[gh_path],
                target_dir=tmp_path,
                overwrite=True,
            )
            source_file = tmp_path / gh_path

            if not source_file.exists():
                result['warnings'].append(
                    f"Mergeable file {gh_path} not found in ZIP"
                )
                continue

            if dest_item.exists() and not force_overwrite:
                # Merge: update galdr section, keep user content
                try:
                    merged = merge_markdown_file(
                        source_file.read_text(encoding='utf-8'),
                        dest_item.read_text(encoding='utf-8'),
                        gh_path,
                    )
                    dest_item.write_text(merged, encoding='utf-8')
                    result['merged_files'].append(str(dest_item))
                    logger.info(f"Merged: {gh_path}")
                except Exception as e:
                    result['warnings'].append(f"Failed to merge {gh_path}: {e}")
            else:
                # Destination doesn't exist or force_overwrite — just copy
                try:
                    dest_item.parent.mkdir(parents=True, exist_ok=True)
                    dest_item.write_bytes(source_file.read_bytes())
                    result['copied_files'].append(str(dest_item))
                    logger.info(f"Copied: {gh_path}")
                except Exception as e:
                    result['warnings'].append(f"Failed to copy {gh_path}: {e}")

    result['operation_time_seconds'] = round(
        (datetime.now() - start_time).total_seconds(), 2
    )

    total = len(result['copied_files']) + len(result['merged_files'])
    if total > 0:
        result['success'] = True
        result['message'] = (
            f"Successfully installed {total} files "
            f"({len(result['skipped_files'])} skipped, {len(result['merged_files'])} merged) "
            f"from {github_repo} in {result['operation_time_seconds']}s"
        )
    else:
        result['success'] = False
        result['error'] = (
            f"No files were installed. "
            f"Skipped: {len(result['skipped_files'])}. "
            f"Warnings: {result['warnings']}"
        )

    return result
