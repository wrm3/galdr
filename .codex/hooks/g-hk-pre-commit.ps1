#!/usr/bin/env pwsh
<#
.SYNOPSIS
    galdr pre-commit sanity hook (opt-in).

.DESCRIPTION
    Checks staged changes for: secrets, large files (>5 MB), and galdr task sync drift.
    
    BLOCK items exit 1 (commit is halted).
    WARN items exit 0 with a warning (commit proceeds).
    
    INSTALLATION (opt-in only):
        git config core.hooksPath .cursor/hooks
    
    REMOVAL:
        git config --unset core.hooksPath

    This script is safe to run manually: .\cursor\hooks\g-hk-pre-commit.ps1
#>

$ErrorActionPreference = "SilentlyContinue"

$repoRoot = git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../")).Path
}
$commonPath = Join-Path $repoRoot "scripts/galdr_git_sanity_common.ps1"
if (Test-Path $commonPath) {
    . $commonPath
}

$block = $false
$warns = @()

Write-Host ""
Write-Host "galdr pre-commit sanity check" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# --- 1. SECRETS CHECK (BLOCK) ---
$secretPatterns = @()
if (Get-Command Get-GaldrSecretPatterns -ErrorAction SilentlyContinue) {
    $secretPatterns = @(Get-GaldrSecretPatterns)
}
if ($secretPatterns.Count -eq 0) {
    $secretPatterns = @(
        "sk-[a-zA-Z0-9]{20,}",
        "Bearer\s+[a-zA-Z0-9._\-]{20,}",
        "AKIA[A-Z0-9]{16}",
        "password\s*=\s*\S+",
        "api_key\s*=\s*\S+",
        "secret_key\s*=\s*\S+",
        "private_key\s*=\s*\S+",
        "-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"
    )
}

$diff = git diff --cached 2>$null
$secretHits = @()
foreach ($pat in $secretPatterns) {
    $hits = $diff | Select-String -Pattern $pat
    if ($hits) {
        $secretHits += $hits | ForEach-Object { "  $($_.Line.Trim())" } | Select-Object -First 3
    }
}

# Also check for staged .env files
$stagedFiles = git diff --cached --name-only 2>$null
$envFiles = $stagedFiles | Where-Object { $_ -match "^\.env(\..*)?$" }
if ($envFiles) {
    $secretHits += $envFiles | ForEach-Object { "  [.env file staged: $_]" }
}

if ($secretHits.Count -gt 0) {
    Write-Host "BLOCK: Secrets detected in staged changes:" -ForegroundColor Red
    $secretHits | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    Write-Host "  -> Remove secrets before committing. Use environment variables or a vault." -ForegroundColor Red
    $block = $true
} else {
    Write-Host "Secrets:     PASS" -ForegroundColor Green
}

# --- 2. LARGE FILE CHECK (WARN) ---
$largeFiles = $stagedFiles | Where-Object {
    (Test-Path $_) -and ((Get-Item $_ -ErrorAction SilentlyContinue).Length -gt 5MB)
}

if ($largeFiles) {
    $sizeWarn = "WARN: Staged files > 5 MB detected:`n" + ($largeFiles | ForEach-Object {
        $sizeKb = [math]::Round((Get-Item $_).Length / 1KB, 0)
        "  $_ ($sizeKb KB)"
    } | Out-String)
    $warns += $sizeWarn
    Write-Host "Large files: WARN — $($largeFiles.Count) file(s) > 5 MB" -ForegroundColor Yellow
} else {
    Write-Host "Large files: PASS" -ForegroundColor Green
}

# --- 3. galdr SYNC DRIFT CHECK (WARN) ---
if (Test-Path ".galdr") {
    $tasksMdStaged = $stagedFiles | Where-Object { $_ -match "TASKS\.md" }
    $taskFilesStaged = $stagedFiles | Where-Object { $_ -match "\.galdr[/\\]tasks[/\\]" }
    
    if ($tasksMdStaged -and -not $taskFilesStaged) {
        $warns += "WARN: .galdr/TASKS.md is staged but no tasks/ files are staged. Run @g-task-sync-check."
        Write-Host "galdr sync: WARN — TASKS.md staged without tasks/ files" -ForegroundColor Yellow
    } elseif ($taskFilesStaged -and -not $tasksMdStaged) {
        $warns += "WARN: tasks/ files staged but .galdr/TASKS.md is not. Run @g-task-sync-check."
        Write-Host "galdr sync: WARN — tasks/ files staged without TASKS.md" -ForegroundColor Yellow
    } else {
        Write-Host "galdr sync: PASS" -ForegroundColor Green
    }
} else {
    Write-Host "galdr sync: SKIP (no .galdr/ in this repo)" -ForegroundColor DarkGray
}

Write-Host ""

# --- RESULT ---
if ($block) {
    Write-Host "Pre-commit check: BLOCKED — fix issues above before committing." -ForegroundColor Red
    Write-Host ""
    exit 1
}

if ($warns.Count -gt 0) {
    Write-Host "Pre-commit check: WARNINGS (commit will proceed)" -ForegroundColor Yellow
    $warns | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    Write-Host ""
    exit 0
}

Write-Host "Pre-commit check: ALL PASS" -ForegroundColor Green
Write-Host ""
exit 0
