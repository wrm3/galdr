#!/usr/bin/env pwsh
<#
.SYNOPSIS
    galdr optional pre-push gate (opt-in).

.DESCRIPTION
    Delegates to scripts/galdr_push_gate.ps1 -HookMode.
    Release checks run only when GALDR_RELEASE_PUSH=1 (or true).

    INSTALLATION (opt-in):
        git config core.hooksPath .cursor/hooks

    Same hooksPath as pre-commit; both hooks live in this folder.

.NOTES
    Complements g-hk-pre-commit.ps1 and scripts/galdr_git_sanity_common.ps1 (T049/T050).
#>
$ErrorActionPreference = "Continue"

$repoRoot = git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

$gate = Join-Path $repoRoot "scripts/galdr_push_gate.ps1"
if (-not (Test-Path $gate)) {
    Write-Host "galdr pre-push: scripts/galdr_push_gate.ps1 not found — allow push" -ForegroundColor DarkYellow
    exit 0
}

& $gate -HookMode
exit $LASTEXITCODE
