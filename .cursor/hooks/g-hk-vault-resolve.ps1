# g-hk-vault-resolve.ps1
# Source this from other hooks:
#   . "$PSScriptRoot\g-hk-vault-resolve.ps1"
#
# Exported variables:
#   $VaultPath
#   $ReposPath
#   $VaultLocalPath
#   $ReposLocalPath
#   $VaultUsingFallback
#   $VaultMigrationCandidate
#   $VaultMessages

function Get-GaldrIdentityMap {
    param([string]$IdentityPath)

    $map = @{
        project_id = ""
        project_name = ""
        user_id = ""
        user_name = ""
        galdr_version = ""
        vault_location = ""
        repos_location = ""
    }

    if (Test-Path $IdentityPath) {
        Get-Content $IdentityPath | ForEach-Object {
            if ($_ -match "^(\w+)=(.*)$") {
                $map[$Matches[1]] = $Matches[2].Trim()
            }
        }
    }

    return $map
}

function Get-EnvSetting {
    param(
        [string]$EnvPath,
        [string[]]$Keys
    )

    if (-not (Test-Path $EnvPath)) {
        return $null
    }

    foreach ($key in $Keys) {
        $match = Select-String -Path $EnvPath -Pattern ("^\s*" + [regex]::Escape($key) + "\s*=\s*(.+)$") | Select-Object -First 1
        if ($match) {
            $value = $match.Matches[0].Groups[1].Value.Trim().Trim('"').Trim("'")
            if ($value) {
                return $value
            }
        }
    }

    return $null
}

function Test-GaldrPathWritable {
    param([string]$PathToCheck)

    try {
        if (-not (Test-Path $PathToCheck)) {
            New-Item -ItemType Directory -Path $PathToCheck -Force | Out-Null
        }
        $probe = Join-Path $PathToCheck ".galdr_write_probe.tmp"
        "" | Set-Content -Path $probe -Encoding UTF8
        Remove-Item $probe -Force -ErrorAction SilentlyContinue
        return $true
    } catch {
        return $false
    }
}

function Get-MarkdownCount {
    param([string]$PathToScan)

    if (-not (Test-Path $PathToScan)) {
        return 0
    }

    return @(
        Get-ChildItem -Path $PathToScan -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "\\.obsidian(\|\\)" }
    ).Count
}

$ProjectRoot = (Get-Location).Path
$IdentityPath = Join-Path $ProjectRoot ".galdr\.identity"
$EnvPath = Join-Path $ProjectRoot ".env"
$Identity = Get-GaldrIdentityMap -IdentityPath $IdentityPath

$VaultLocalPath = Join-Path $ProjectRoot ".galdr\vault"
$ReposLocalPath = Join-Path $ProjectRoot ".galdr\repos"
$VaultUsingFallback = $false
$VaultMigrationCandidate = $false
$VaultMessages = @()

$vaultLocation = $Identity.vault_location
if (-not $vaultLocation) {
    $vaultLocation = Get-EnvSetting -EnvPath $EnvPath -Keys @("GALDR_VAULT_LOCATION", "GALDR_KNOWLEDGE_WELL_PATH")
}

$reposLocation = $Identity.repos_location
if (-not $reposLocation) {
    $reposLocation = Get-EnvSetting -EnvPath $EnvPath -Keys @("GALDR_REPOS_LOCATION")
}

if (-not $vaultLocation -or $vaultLocation -eq "{LOCAL}") {
    $VaultPath = $VaultLocalPath
} else {
    if (Test-GaldrPathWritable -PathToCheck $vaultLocation) {
        $VaultPath = $vaultLocation
    } else {
        $VaultPath = $VaultLocalPath
        $VaultUsingFallback = $true
        $VaultMessages += "Shared vault unavailable; writing to local fallback at `.galdr/vault/`."
    }
}

if (-not $reposLocation -or $reposLocation -eq "{LOCAL}") {
    $ReposPath = $ReposLocalPath
} else {
    if (Test-GaldrPathWritable -PathToCheck $reposLocation) {
        $ReposPath = $reposLocation
    } else {
        $ReposPath = $ReposLocalPath
        $VaultMessages += "Configured repos mirror unavailable; using local `.galdr/repos/`."
    }
}

if (-not (Test-Path $VaultLocalPath)) {
    New-Item -ItemType Directory -Path $VaultLocalPath -Force | Out-Null
}
if (-not (Test-Path $ReposLocalPath)) {
    New-Item -ItemType Directory -Path $ReposLocalPath -Force | Out-Null
}
if (-not (Test-Path $VaultPath)) {
    New-Item -ItemType Directory -Path $VaultPath -Force | Out-Null
}
if (-not (Test-Path $ReposPath)) {
    New-Item -ItemType Directory -Path $ReposPath -Force | Out-Null
}

$localVaultMdCount = Get-MarkdownCount -PathToScan $VaultLocalPath
if ($VaultPath -ne $VaultLocalPath -and $localVaultMdCount -gt 0) {
    $VaultMigrationCandidate = $true
    $VaultMessages += "Local vault contains $localVaultMdCount markdown files while a shared vault is configured. Consider running migration."
}

$ProjectId = $Identity.project_id
if (-not $ProjectId) {
    $ProjectId = "unknown"
}

$ProjectName = $Identity.project_name
if (-not $ProjectName -or $ProjectName -eq "{project_name}") {
    $ProjectName = Split-Path $ProjectRoot -Leaf
}

$ProjectDir = Join-Path (Join-Path $VaultPath "projects") $ProjectName
$SessionsDir = Join-Path $ProjectDir "sessions"
$DecisionsDir = Join-Path $ProjectDir "decisions"

foreach ($path in @($ProjectDir, $SessionsDir, $DecisionsDir)) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}
