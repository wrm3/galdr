# vault-resolve.ps1 — Resolve the vault path and project identity.
# Source this from other hooks: . "$PSScriptRoot\vault-resolve.ps1"
#
# After sourcing, these variables are available:
#   $VaultPath    — resolved vault root (shared or local)
#   $ProjectId    — UUID from .galdr/.project_id (or "unknown")
#   $ProjectName  — folder name of the project root
#   $SessionsDir  — projects/{project_name}/sessions under vault root
#   $DecisionsDir — projects/{project_name}/decisions under vault root
#   $ProjectDir   — projects/{project_name} under vault root

$VaultPath     = $null
$ProjectId     = "unknown"
$ProjectName   = Split-Path (Get-Location).Path -Leaf

$pidFile = Join-Path (Get-Location).Path ".galdr\.project_id"
if (Test-Path $pidFile) {
    $ProjectId = (Get-Content $pidFile -Raw).Trim()
}

# Primary: read .galdr/.vault_location
$vaultLocFile = Join-Path (Get-Location).Path ".galdr\.vault_location"
if (Test-Path $vaultLocFile) {
    $candidate = (Get-Content $vaultLocFile -Raw).Trim()
    if ($candidate -and $candidate -ne '' -and $candidate -ne '{LOCAL}') {
        $VaultPath = $candidate
    }
}

# Deprecated fallback: .env GALDR_KNOWLEDGE_WELL_PATH (for backward compat)
if (-not $VaultPath) {
    $envFile = Join-Path (Get-Location).Path ".env"
    if (Test-Path $envFile) {
        $match = Select-String -Path $envFile -Pattern '^\s*GALDR_KNOWLEDGE_WELL_PATH\s*=\s*(.+)' | Select-Object -First 1
        if ($match) {
            $envCandidate = $match.Matches[0].Groups[1].Value.Trim().Trim('"').Trim("'")
            if ($envCandidate -and $envCandidate -ne '') {
                $VaultPath = $envCandidate
            }
        }
    }
}

# Default: local vault
if (-not $VaultPath) {
    $VaultPath = Join-Path (Get-Location).Path ".galdr\vault"
}

if (-not (Test-Path $VaultPath)) {
    New-Item -ItemType Directory -Path $VaultPath -Force | Out-Null
}

$ProjectDir   = Join-Path (Join-Path $VaultPath "projects") $ProjectName
$SessionsDir  = Join-Path $ProjectDir "sessions"
$DecisionsDir = Join-Path $ProjectDir "decisions"
