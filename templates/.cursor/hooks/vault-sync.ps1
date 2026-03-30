# vault-sync.ps1 — Migrate from local .galdr/vault/ to shared vault.
# Run manually or triggered when session-start detects pending local content.
# When GALDR_KNOWLEDGE_WELL_PATH is set in .env and .galdr/vault/ has content, this
# moves everything to the shared location, updating changed files.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File .cursor/hooks/vault-sync.ps1
#   powershell -ExecutionPolicy Bypass -File .cursor/hooks/vault-sync.ps1 -AutoClean

param(
    [switch]$AutoClean
)

$ErrorActionPreference = "Continue"

. "$PSScriptRoot\vault-resolve.ps1"

$localVault = Join-Path (Get-Location).Path ".galdr\vault"

if (-not (Test-Path $localVault)) {
    Write-Host "No local vault found at $localVault — nothing to sync."
    exit 0
}

if (-not $VaultPath -or $VaultPath -eq $localVault) {
    Write-Host "GALDR_KNOWLEDGE_WELL_PATH not set or points to local vault."
    Write-Host "Set GALDR_KNOWLEDGE_WELL_PATH in .env to a shared location (e.g., G:\knowledge_well)."
    Write-Host "Until then, vault writes go to .galdr/vault/ — they'll auto-migrate when you set the path."
    exit 0
}

$localFiles = Get-ChildItem -Path $localVault -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
if (-not $localFiles -or $localFiles.Count -eq 0) {
    Write-Host "Local vault is empty — nothing to sync."
    exit 0
}

Write-Host "Migrating $($localFiles.Count) notes from .galdr/vault/ to $VaultPath ..."

$copied = 0
$updated = 0
$skipped = 0

foreach ($file in $localFiles) {
    $relPath = $file.FullName.Substring($localVault.Length).TrimStart('\', '/')
    $destPath = Join-Path $VaultPath $relPath

    $destDir = Split-Path $destPath -Parent
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    if (Test-Path $destPath) {
        $srcHash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
        $dstHash = (Get-FileHash $destPath -Algorithm SHA256).Hash
        if ($srcHash -eq $dstHash) {
            $skipped++
        } else {
            Copy-Item -Path $file.FullName -Destination $destPath -Force
            $updated++
            Write-Host "  UPDATE: $relPath"
        }
    } else {
        Copy-Item -Path $file.FullName -Destination $destPath -Force
        $copied++
        Write-Host "  COPY: $relPath"
    }
}

Write-Host "`nMigration complete: $copied new, $updated updated, $skipped unchanged."

if (($copied + $updated) -gt 0) {
    if ($AutoClean) {
        Remove-Item -Path $localVault -Recurse -Force
        Write-Host "Local vault (.galdr/vault/) cleaned up automatically."
    } else {
        $answer = Read-Host "Delete local vault contents now that they're in the shared location? (y/N)"
        if ($answer -eq "y" -or $answer -eq "Y") {
            Remove-Item -Path $localVault -Recurse -Force
            Write-Host "Local vault deleted."
        } else {
            Write-Host "Local vault preserved. Run with -AutoClean to skip this prompt."
        }
    }
}
