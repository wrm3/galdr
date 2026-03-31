"""
galdr_install Plugin

Install or upgrade the full galdr development environment to a project directory.
Works for both first-time installs and upgrades of existing installations,
including remote containers — no drive mounts needed.

HOW IT WORKS:
  1. Call galdr_install(target_path=...) to get a ready-to-run shell command
  2. Run the shell command — it downloads a ZIP from this MCP server's
     /install/download endpoint and unzips it into target_path
  3. No GitHub API calls, no drive mounts, works on remote containers

MERGE HANDLING (agents.md / CLAUDE.md / GEMINI.md):
  For upgrades, read those files locally and pass their content via existing_files.
  The server merges the galdr-managed section while preserving your custom content.

GUARDRAILS.md:
  Included in the ZIP by default (first install). For upgrades where you have a
  customized GUARDRAILS.md, pass skip_files=['GUARDRAILS.md'] to preserve it.
"""
import json
import logging

logger = logging.getLogger(__name__)

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "galdr_install"

TOOL_DESCRIPTION = (
    "Install or upgrade the full galdr development environment to a project directory. "
    "Required parameter: target_path (the local directory path to install into). "
    "Returns a shell command (PowerShell + bash) to run locally — works with remote containers, no drive mounts needed. "
    "The command downloads templates/ as a ZIP from this MCP server and unzips it into target_path. "
    "For upgrades: pass existing_files with current content of agents.md/CLAUDE.md/GEMINI.md/.gitignore "
    "so the galdr section is updated while your custom content is preserved. "
    "GUARDRAILS.md is included by default (first install). For upgrades with a customized GUARDRAILS.md, "
    "pass skip_files=['GUARDRAILS.md'] to preserve your version."
)

TOOL_PARAMS = {
    "target_path": (
        "Target project directory to install galdr into (required). "
        "Use the exact local path as it appears on your filesystem, "
        "e.g. 'G:\\\\MyProject' or '/home/user/myproject'."
    ),
    "existing_files": (
        "Optional dict of {filename: content} for files to merge rather than overwrite. "
        "Supported keys: 'agents.md', 'CLAUDE.md', 'GEMINI.md', '.gitignore'. "
        "Read these files locally before calling this tool and pass their content here."
    ),
    "skip_files": (
        "Optional list of filenames to omit from the ZIP. "
        "Default: [] (all files included). For upgrades with a customized GUARDRAILS.md, "
        "pass ['GUARDRAILS.md'] to preserve your version."
    ),
    "dry_run": "Preview the command without running it (default: False)",
}

_config = None


def setup(context: dict):
    global _config
    _config = context.get('config', {})


async def execute(
    target_path: str,
    existing_files: dict = None,
    skip_files: list = None,
    dry_run: bool = False,
    context: dict = None,
) -> dict:
    """Return a shell command that downloads and installs galdr into target_path."""
    cfg = (context or {}).get('config', _config or {})
    GALDR_url = cfg.get('GALDR_url', 'http://localhost:8082').rstrip('/')
    endpoint = f"{GALDR_url}/install/download"

    if skip_files is None:
        skip_files = []

    # Build POST body (only needed when merging or skipping files)
    needs_post = bool(existing_files or skip_files)
    body = {}
    if existing_files:
        body['existing_files'] = existing_files
    if skip_files:
        body['skip_files'] = skip_files

    if dry_run:
        return {
            'success': True,
            'tool': 'galdr_install',
            'target_path': target_path,
            'dry_run': True,
            'endpoint': endpoint,
            'needs_post': needs_post,
            'skip_files': skip_files,
            'existing_files_keys': list((existing_files or {}).keys()),
        }

    if needs_post:
        ps_body = json.dumps(body).replace('"', '\\"')
        ps_cmd = (
            f"$body = \"{ps_body}\"; "
            f"$tmp = [System.IO.Path]::GetTempFileName() + '.zip'; "
            f"Invoke-WebRequest -Uri '{endpoint}' -Method POST "
            f"-ContentType 'application/json' -Body $body -OutFile $tmp; "
            f"Expand-Archive -Path $tmp -DestinationPath '{target_path}' -Force; "
            f"Remove-Item $tmp"
        )
        bash_body = json.dumps(body).replace("'", "'\"'\"'")
        bash_cmd = (
            f"curl -sL -X POST '{endpoint}' "
            f"-H 'Content-Type: application/json' "
            f"-d '{bash_body}' "
            f"-o /tmp/galdr_install.zip && "
            f"unzip -o /tmp/galdr_install.zip -d '{target_path}' && "
            f"rm /tmp/galdr_install.zip"
        )
    else:
        ps_cmd = (
            f"$tmp = [System.IO.Path]::GetTempFileName() + '.zip'; "
            f"Invoke-WebRequest -Uri '{endpoint}' -OutFile $tmp; "
            f"Expand-Archive -Path $tmp -DestinationPath '{target_path}' -Force; "
            f"Remove-Item $tmp"
        )
        bash_cmd = (
            f"curl -sL '{endpoint}' -o /tmp/galdr_install.zip && "
            f"unzip -o /tmp/galdr_install.zip -d '{target_path}' && "
            f"rm /tmp/galdr_install.zip"
        )

    merge_note = f" Merged: {list(existing_files.keys())}." if existing_files else ''
    skip_note = f" Preserved (skipped): {skip_files}." if skip_files else ''

    # Post-install: generate .project_id (UUID), resolve .user_id, set .vault_location
    # .project_id: UUID4 — matches g-grooming, g-setup, and g-memory expectations
    # .user_id: read from %APPDATA%/galdr/user_config.json first, then {SETUP_NEEDED}
    post_install_ps = (
        f"$projId = [guid]::NewGuid().ToString(); "
        f"Set-Content -Path '{target_path}\\.galdr\\.project_id' -Value $projId -Encoding UTF8; "
        f"Write-Host \"Project ID: $projId\"; "
        f"$vaultLoc = '{target_path}\\.galdr\\.vault_location'; "
        f"if (-not (Test-Path $vaultLoc)) {{ Set-Content -Path $vaultLoc -Value '{{LOCAL}}' -Encoding UTF8 }}; "
        f"$userIdFile = '{target_path}\\.galdr\\.user_id'; "
        f"if (-not (Test-Path $userIdFile)) {{ "
        f"$resolved = $null; "
        f"$appCfg = if ($env:APPDATA) {{ Join-Path $env:APPDATA 'galdr\\user_config.json' }} else {{ Join-Path $env:HOME '.config/galdr/user_config.json' }}; "
        f"if (Test-Path $appCfg) {{ try {{ $cfg = Get-Content $appCfg -Raw | ConvertFrom-Json; if ($cfg.user_id -and $cfg.user_id -ne 'SETUP_NEEDED') {{ $resolved = $cfg.user_id }} }} catch {{}} }}; "
        f"if ($resolved) {{ Set-Content -Path $userIdFile -Value $resolved -Encoding UTF8; Write-Host \"User ID: $resolved (from global config)\" }} "
        f"else {{ Set-Content -Path $userIdFile -Value '{{SETUP_NEEDED}}' -Encoding UTF8; Write-Host 'User ID: {{SETUP_NEEDED}} — run session-start hook or edit .galdr/.user_id' }} "
        f"}}"
    )
    post_install_bash = (
        f"projId=$(python3 -c \"import uuid; print(uuid.uuid4())\"); "
        f"echo \"$projId\" > '{target_path}/.galdr/.project_id'; "
        f"echo \"Project ID: $projId\"; "
        f"[ -f '{target_path}/.galdr/.vault_location' ] || echo '{{LOCAL}}' > '{target_path}/.galdr/.vault_location'; "
        f"userIdFile='{target_path}/.galdr/.user_id'; "
        f"if [ ! -f \"$userIdFile\" ]; then "
        f"resolved=''; "
        f"cfgFile=\"${{XDG_CONFIG_HOME:-$HOME/.config}}/galdr/user_config.json\"; "
        f"if [ -f \"$cfgFile\" ]; then resolved=$(python3 -c \"import json; c=json.load(open('$cfgFile')); uid=c.get('user_id',''); print(uid if uid and uid != 'SETUP_NEEDED' else '')\" 2>/dev/null); fi; "
        f"if [ -n \"$resolved\" ]; then echo \"$resolved\" > \"$userIdFile\"; echo \"User ID: $resolved (from global config)\"; "
        f"else echo '{{SETUP_NEEDED}}' > \"$userIdFile\"; echo 'User ID: {{SETUP_NEEDED}} — edit .galdr/.user_id'; fi; "
        f"fi"
    )

    return {
        'success': True,
        'tool': 'galdr_install',
        'target_path': target_path,
        'shell_command': {
            'powershell': ps_cmd,
            'bash': bash_cmd,
        },
        'post_install': {
            'powershell': post_install_ps,
            'bash': post_install_bash,
        },
        'instructions': (
            f"STEP 1: Run shell_command to install galdr into '{target_path}'."
            f"{merge_note}{skip_note} "
            f"STEP 2: Run post_install to generate .project_id, .vault_location, and .user_id. "
            f"User identity is configured automatically on first session start."
        ),
        'upgrade_hint': (
            "For upgrades: read agents.md/CLAUDE.md/GEMINI.md/.gitignore locally first "
            "and pass their content as existing_files to preserve your customizations."
        ),
    }
