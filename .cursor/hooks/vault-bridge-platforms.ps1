# vault-bridge-platforms.ps1
# Bridges .platforms/ snapshot files into the vault's research/platforms/ folder.
# Run after a crawl4ai crawl completes, or on a schedule.
# Reads from {repo}/.platforms/{platform}/*.md and writes to {vault}/research/platforms/{platform}/

param(
    [switch]$DryRun
)

. "$PSScriptRoot\vault-resolve.ps1"

$platformsDir = Join-Path (Get-Location).Path ".platforms"
if (-not (Test-Path $platformsDir)) {
    Write-Host "No .platforms/ directory found - nothing to bridge."
    exit 0
}

$vaultPlatformsDir = Join-Path (Join-Path $VaultPath "research") "platforms"
if (-not (Test-Path $vaultPlatformsDir)) {
    New-Item -ItemType Directory -Path $vaultPlatformsDir -Force | Out-Null
}

$copied = 0
$skipped = 0
$updated = 0

Get-ChildItem -Path $platformsDir -Recurse -Filter "*.md" | ForEach-Object {
    $relPath = $_.FullName.Substring($platformsDir.Length + 1)
    if ($relPath -eq "CHANGELOG.md") { return }

    $destPath = Join-Path $vaultPlatformsDir $relPath
    $destDir = Split-Path $destPath -Parent

    if (-not (Test-Path $destDir)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }

    if (Test-Path $destPath) {
        $srcHash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
        $dstHash = (Get-FileHash $destPath -Algorithm SHA256).Hash
        if ($srcHash -eq $dstHash) {
            $skipped++
            return
        }
        $updated++
    } else {
        $copied++
    }

    if ($DryRun) {
        Write-Host "[DRY RUN] Would copy: $relPath"
    } else {
        Copy-Item $_.FullName $destPath -Force
    }
}

Write-Host "Platform docs bridge: $copied new, $updated updated, $skipped unchanged"

if (-not $DryRun -and ($copied + $updated) -gt 0) {
    Write-Host "Run @g-vault-sync to index these in the database for semantic search."
}
