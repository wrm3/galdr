"""
galdr_plan_reset Plugin

Reset .galdr/ to a blank template by deleting it and re-downloading from GitHub.

Safety features:
  1. confirm=False (default): preview mode — shows exactly what will be deleted.
  2. backup=True  (default):  zips .galdr/ to .GALDR_backup_YYYYMMDD_HHMMSS.zip
                              BEFORE deleting anything. Backup is excluded from
                              git via .gitignore automatically.
  3. confirm=True required:   explicit opt-in to actually execute the reset.

USE WITH CAUTION: This permanently deletes all local .galdr/ content including:
  - TASKS.md, PRD.md, SUBSYSTEMS.md  (root files)
  - config/HEARTBEAT.md, config/SPRINT.md  (operational config)
  - docs/PROJECT_CONTEXT.md, docs/ARCHITECTURE_CONSTRAINTS.md  (project docs)
  - tracking/BUGS.md, tracking/IDEA_BOARD.md  (status tracking)
  - subsystems/  (subsystem spec files)
  - All files in .galdr/tasks/   (every task file)
  - All files in .galdr/phases/  (every phase file)

After reset, .galdr/ contains the blank galdr template from the GitHub repo:
  - Blank root files (ready to fill in for a new project)
  - .galdr/examples/   (example files for reference)
  - .galdr/reference/  (reference documentation)
  - Empty tasks/ and phases/ directories

Typical safe workflow:
  1. galdr_plan_reset(target_path, confirm=False)         ← preview + backup info
  2. Confirm you have a backup OR your data is committed
  3. galdr_plan_reset(target_path, confirm=True)          ← backup then reset

See also:
  galdr_install       — full first-time install
  galdr_update  — update IDE configs only (NEVER touches .galdr/)
"""
import shutil
import logging
from pathlib import Path

from ._galdr_shared import (
    get_github_token,
    get_github_repo,
    get_os_info,
    resolve_target_path,
    download_repo_zip,
    extract_manifest_from_zip,
    backup_GALDR_dir,
    GALDR_MANIFEST,
)

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "galdr_plan_reset"

TOOL_DESCRIPTION = (
    "Reset .galdr/ task management folder to the blank template by deleting it "
    "and re-downloading from GitHub. "
    "SAFETY: By default (backup=True) the existing .galdr/ is zipped to "
    ".GALDR_backup_YYYYMMDD_HHMMSS.zip before anything is deleted. "
    "Requires confirm=True to actually execute — call with confirm=False first to "
    "preview what will be deleted and where the backup will be saved. "
    "Use this when starting a new project in an existing galdr directory, or when "
    "you want to completely reset the task management state."
)

TOOL_PARAMS = {
    "target_path": (
        "Target project directory containing the .galdr/ folder to reset (required)"
    ),
    "confirm": (
        "Must be True to actually delete and reset. "
        "Pass confirm=False (default) to preview what would be deleted. "
        "REQUIRED explicit opt-in — even with backup=True, confirm is required."
    ),
    "backup": (
        "Create a zip backup of .galdr/ before deleting (default: True, highly recommended). "
        "Backup saved as .GALDR_backup_YYYYMMDD_HHMMSS.zip in the target directory. "
        "Pass backup=False only if you are certain the data is already committed or disposable."
    ),
    "dry_run": (
        "Preview GitHub download without writing files (default: False). "
        "Only meaningful when confirm=True."
    ),
}

logger = logging.getLogger(__name__)

_config = None


def setup(context: dict):
    """Called once at plugin load time."""
    global _config
    _config = context.get('config', {})


def _inventory_galdr(GALDR_dir: Path) -> dict:
    """
    Build an inventory of .galdr/ contents to show in the preview.
    Returns counts and a sample file listing.
    """
    if not GALDR_dir.exists():
        return {'exists': False, 'total_files': 0, 'files': []}

    all_files = sorted(GALDR_dir.rglob('*'))
    files = [f for f in all_files if f.is_file() and f.name != '.gitkeep']
    dirs = [f for f in all_files if f.is_dir()]

    # Highlight the critical data files
    critical_files = []
    root_files = ['TASKS.md', 'PRD.md', 'SUBSYSTEMS.md']
    tracking_files = ['tracking/BUGS.md', 'tracking/IDEA_BOARD.md', 'tracking/INBOX.md']
    docs_files = ['docs/PROJECT_CONTEXT.md', 'docs/PROJECT_GOALS.md']
    for name in root_files + tracking_files + docs_files:
        fp = GALDR_dir / name
        if fp.exists():
            critical_files.append(name)

    tasks_dir = GALDR_dir / 'tasks'
    phases_dir = GALDR_dir / 'phases'
    task_files = [
        f for f in tasks_dir.glob('*.md') if f.name != '.gitkeep'
    ] if tasks_dir.exists() else []
    phase_files = [
        f for f in phases_dir.glob('*.md') if f.name != '.gitkeep'
    ] if phases_dir.exists() else []

    return {
        'exists': True,
        'total_files': len(files),
        'total_dirs': len(dirs),
        'critical_files': critical_files,
        'task_count': len(task_files),
        'phase_count': len(phase_files),
        'task_files': [f.name for f in task_files[:20]],   # cap sample at 20
        'phase_files': [f.name for f in phase_files],
    }


async def execute(
    target_path: str,
    confirm: bool = False,
    backup: bool = True,
    dry_run: bool = False,
    context: dict = None,
) -> dict:
    """
    Reset .galdr/ to blank template.

    confirm=False : returns a preview of what would be deleted (no changes made).
    confirm=True  : optionally backs up, then deletes .galdr/, then downloads
                    a fresh blank template from GitHub.
    """
    token = get_github_token()
    repo = get_github_repo()
    original_path = target_path

    try:
        target = resolve_target_path(target_path)
    except Exception as e:
        return {
            'success': False,
            'error': f"Invalid target path '{target_path}': {e}",
        }

    GALDR_dir = target / '.galdr'
    inventory = _inventory_galdr(GALDR_dir)

    # ── Preview mode (confirm=False) ──────────────────────────────────────────
    if not confirm:
        if not inventory['exists']:
            return {
                'success': True,
                'tool': 'galdr_plan_reset',
                'confirm_required': True,
                'message': (
                    f".galdr/ does not exist at {original_path}. "
                    "Pass confirm=True to download the blank template."
                ),
                'inventory': inventory,
                'action': 'none — .galdr/ not present',
            }

        backup_location = str(target / f'.GALDR_backup_YYYYMMDD_HHMMSS.zip')
        return {
            'success': True,
            'tool': 'galdr_plan_reset',
            'confirm_required': True,
            'message': (
                "PREVIEW ONLY — no changes made.\n\n"
                f"Calling galdr_plan_reset with confirm=True will:\n"
                f"  {'1. CREATE BACKUP: zip .galdr/ → .GALDR_backup_YYYYMMDD_HHMMSS.zip' if backup else '1. (backup=False — NO BACKUP WILL BE CREATED)'}\n"
                f"  {'2' if backup else '1'}. PERMANENTLY DELETE .galdr/ at: {original_path}\n"
                f"  {'3' if backup else '2'}. Download the blank galdr template from GitHub ({repo})\n\n"
                f"The following data will be PERMANENTLY DESTROYED (after backup):"
            ),
            'inventory': inventory,
            'backup_will_be_created': backup,
            'backup_location': backup_location if backup else None,
            'warning': (
                "Even with backup=True, verify the backup was created successfully "
                "before discarding the original. "
                "The backup zip is excluded from git commits automatically."
                if backup
                else
                "WARNING: backup=False — no backup will be created before deletion. "
                "Ensure your task data is committed or already backed up."
            ),
            'next_step': "Call galdr_plan_reset with confirm=True to proceed.",
        }

    # ── Confirmed execution ───────────────────────────────────────────────────
    from datetime import datetime
    start_time = datetime.now()

    result = {
        'success': False,
        'tool': 'galdr_plan_reset',
        'target_path': original_path,
        'target_path_resolved': str(target),
        'source': f'github:{repo}',
        'dry_run': dry_run,
        'backup_requested': backup,
        'backup_result': None,
        'pre_reset_inventory': inventory,
        'deleted': False,
        'downloaded_files': [],
        'warnings': [],
        'operation_time_seconds': 0,
    }

    # Step 1: Backup (before touching anything)
    if backup and not dry_run:
        backup_result = backup_GALDR_dir(GALDR_dir, target)
        result['backup_result'] = backup_result

        if not backup_result['success'] and not backup_result.get('skipped'):
            result['error'] = (
                f"Backup failed: {backup_result['error']}. "
                "Reset aborted to protect your data. "
                "Fix the backup issue or pass backup=False to skip backup (not recommended)."
            )
            return result

        if backup_result['success'] and not backup_result.get('skipped'):
            logger.info(f"Backup created: {backup_result['backup_name']}")
    elif dry_run and backup:
        result['backup_result'] = {
            'success': True,
            'skipped': True,
            'skip_reason': 'dry_run=True — backup not created',
        }

    # Step 2: Delete existing .galdr/
    if GALDR_dir.exists() and not dry_run:
        try:
            shutil.rmtree(str(GALDR_dir))
            result['deleted'] = True
            logger.info(f"galdr_plan_reset: deleted {GALDR_dir}")
        except Exception as e:
            result['error'] = f"Failed to delete .galdr/: {e}"
            if result['backup_result'] and result['backup_result'].get('backup_path'):
                result['error'] += (
                    f" (Your backup is safe at: {result['backup_result']['backup_path']})"
                )
            return result
    elif dry_run and GALDR_dir.exists():
        result['deleted'] = 'would_delete (dry_run)'
        logger.info(f"galdr_plan_reset: dry_run — would delete {GALDR_dir}")

    # Step 3: Download fresh .galdr/ from GitHub (ZIP approach — fast, no timeouts)
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    try:
        zip_bytes = download_repo_zip(repo=repo, token=token)
    except Exception as exc:
        result['error'] = f"Failed to download repo ZIP: {exc}"
        if result['backup_result'] and result['backup_result'].get('backup_path'):
            result['error'] += (
                f" Your backup is at: {result['backup_result']['backup_path']}."
            )
        return result

    gh_result = extract_manifest_from_zip(
        zip_bytes=zip_bytes,
        manifest=GALDR_MANIFEST,
        target_dir=target,
        overwrite=True,
    )

    if not gh_result.get('success') or gh_result['errors']:
        backup_note = ''
        if result['backup_result'] and result['backup_result'].get('backup_path'):
            backup_note = (
                f" Your backup is at: {result['backup_result']['backup_path']}. "
                "Run galdr_plan_reset again to retry."
            )
        if not gh_result.get('success'):
            result['error'] = f"Failed to extract .galdr/ from ZIP.{backup_note}"
            return result
        result['warnings'].extend(gh_result['errors'])

    result['downloaded_files'] = gh_result['files_fetched']

    result['operation_time_seconds'] = round(
        (datetime.now() - start_time).total_seconds(), 2
    )
    result['success'] = True

    # Build human-readable summary
    backup_summary = ''
    br = result['backup_result']
    if br and br.get('success') and not br.get('skipped'):
        kb = round(br['backup_size_bytes'] / 1024, 1)
        backup_summary = (
            f"Backup: {br['backup_name']} ({br['file_count']} files, {kb} KB). "
        )
    elif backup and (not br or br.get('skipped')):
        backup_summary = 'Backup: nothing to back up (.galdr/ was empty or absent). '

    result['message'] = (
        f"Successfully reset .galdr/. "
        f"{backup_summary}"
        f"Deleted {inventory.get('total_files', 0)} old files, "
        f"downloaded {len(result['downloaded_files'])} template files "
        f"in {result['operation_time_seconds']}s."
    )
    result['os_info'] = get_os_info()
    return result
