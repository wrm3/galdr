# vault-enrich-platforms.ps1 — Inject frontmatter into platform docs that lack it.
# Adds ingestion_type, source, topics, refresh_policy, expires_after.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File .cursor/hooks/vault-enrich-platforms.ps1
#   powershell -ExecutionPolicy Bypass -File .cursor/hooks/vault-enrich-platforms.ps1 -DryRun

param(
    [switch]$DryRun
)

. "$PSScriptRoot\vault-resolve.ps1"

$platformsDir = Join-Path $VaultPath "research\platforms"
if (-not (Test-Path $platformsDir)) {
    Write-Host "No platforms directory found at $platformsDir"
    exit 0
}

$platformMeta = @{
    "claude-code" = @{
        topics = "AI, Platform, Anthropic, claude-code, documentation"
        baseUrl = "https://docs.anthropic.com"
        vendor = "Anthropic"
    }
    "cursor" = @{
        topics = "AI, Platform, cursor, IDE, documentation"
        baseUrl = "https://docs.cursor.com"
        vendor = "Cursor"
    }
    "gemini" = @{
        topics = "AI, Platform, Google, Gemini, documentation"
        baseUrl = "https://ai.google.dev"
        vendor = "Google"
    }
    "openai" = @{
        topics = "AI, Platform, OpenAI, Codex, documentation"
        baseUrl = "https://platform.openai.com"
        vendor = "OpenAI"
    }
    "opencode" = @{
        topics = "AI, Platform, Open Source, OpenCode, documentation"
        baseUrl = "https://opencode.ai"
        vendor = "OpenCode"
    }
}

$enriched = 0
$skipped = 0
$errors = 0

$allFiles = Get-ChildItem $platformsDir -Recurse -Filter "*.md" -File

foreach ($file in $allFiles) {
    $raw = Get-Content $file.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $raw) { $errors++; continue }

    if ($raw -match '^---\r?\n') {
        $skipped++
        continue
    }

    $relFromPlatforms = $file.FullName.Substring($platformsDir.Length + 1).Replace("\", "/")
    $platformKey = ($relFromPlatforms -split "/")[0]

    $meta = $platformMeta[$platformKey]
    if (-not $meta) {
        $meta = @{
            topics = "AI, Platform, documentation"
            baseUrl = "https://unknown"
            vendor = "Unknown"
        }
    }

    $title = ""
    $firstHeading = ($raw -split "`n" | Where-Object { $_ -match '^#\s+' } | Select-Object -First 1)
    if ($firstHeading) {
        $title = ($firstHeading -replace '^#+\s*', '').Trim()
    } else {
        $title = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    }
    $title = $title -replace '"', "'"
    if ($title.Length -gt 120) { $title = $title.Substring(0, 120) }

    $sourceUrl = $meta.baseUrl
    $fnameClean = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    if ($fnameClean -match '^(https?[_\-])') {
        $sourceUrl = $fnameClean -replace '_', '/' -replace '\.md$', ''
    }

    $dateStr = $file.LastWriteTime.ToString("yyyy-MM-dd")
    $refreshDate = (Get-Date).AddDays(14).ToString("yyyy-MM-dd")
    $expiresDate = (Get-Date).AddDays(30).ToString("yyyy-MM-dd")

    $frontmatter = @"
---
date: $dateStr
type: platform_doc
ingestion_type: crawl4ai
title: "$title"
source: $sourceUrl
topics: [$($meta.topics)]
refresh_policy: weekly
refresh_after: $refreshDate
expires_after: $expiresDate
source_volatility: high
project_id: null
---

"@

    if ($DryRun) {
        Write-Host "[DRY RUN] Would enrich: $relFromPlatforms"
        Write-Host "  title: $title"
        Write-Host "  topics: $($meta.topics)"
        $enriched++
    } else {
        $newContent = $frontmatter + $raw
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
        $enriched++
    }
}

$mode = if ($DryRun) { "DRY RUN" } else { "LIVE" }
Write-Host "`n=== Platform Enrichment Complete ($mode) ==="
Write-Host "Enriched: $enriched"
Write-Host "Skipped (already has frontmatter): $skipped"
Write-Host "Errors: $errors"
Write-Host "Total processed: $($allFiles.Count)"
