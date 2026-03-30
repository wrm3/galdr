# agent-complete.ps1 - Cursor hook for agent/stop lifecycle
# Triggered when the agent loop ends.
# Captures the conversation into galdr agent memory (async, best-effort).

$inputJson = $input | Out-String

try {
    $eventData      = $inputJson | ConvertFrom-Json
    $status         = $eventData.status
    $loopCount      = $eventData.loop_count
    $conversationId = $eventData.conversation_id
} catch {
    $status         = "unknown"
    $loopCount      = 0
    $conversationId = "unknown"
}

# ── Memory Capture (async background job) ────────────────────────────────────
$projectPath   = (Get-Location).Path
$adapterScript = Join-Path $PSScriptRoot "cursor_adapter.py"

if (Test-Path $adapterScript) {
    $jobArgs = @(
        $adapterScript,
        "--project-path", $projectPath,
        "--loop-count",   $loopCount,
        "--status",       $(if ($status -eq "success") { "completed" } else { "partial" })
    )
    if ($conversationId -and $conversationId -ne "unknown") {
        $jobArgs += "--conversation-id"
        $jobArgs += $conversationId
    }

    Start-Job -ScriptBlock {
        param($pythonExe, $args)
        & $pythonExe @args 2>&1 | Out-Null
    } -ArgumentList "python", $jobArgs | Out-Null
}

# ── Vault Session Summary (best-effort) ───────────────────────────────────────
try {
    . "$PSScriptRoot\vault-resolve.ps1"
    if ($VaultPath -and [int]$loopCount -ge 2) {
        $dateStr = Get-Date -Format "yyyy-MM-dd"
        $timeStr = Get-Date -Format "HHmmss"
        $idShort = if ($conversationId -and $conversationId -ne "unknown") { $conversationId.Substring(0, [Math]::Min(8, $conversationId.Length)) } else { "noid" }

        if (-not (Test-Path $SessionsDir)) { New-Item -ItemType Directory -Path $SessionsDir -Force | Out-Null }

        $fileName = "${dateStr}_${timeStr}_${idShort}.md"
        $filePath = Join-Path $SessionsDir $fileName

        $frontmatter = @"
---
date: $dateStr
project: $ProjectName
project_id: $ProjectId
type: session
ingestion_type: session
source: cursor/hook
conversation_id: $conversationId
turns: $loopCount
platform: cursor
status: $(if ($status -eq 'success') { 'completed' } else { 'partial' })
topics: [session, $ProjectName]
---

# Session: $ProjectName ($dateStr)

- **Project ID**: $ProjectId
- **Turns**: $loopCount
- **Status**: $status
- **Conversation**: $conversationId

> Auto-generated session stub. The AI agent will enrich this note with a summary during the next continual-learning pass.
"@
        Set-Content -Path $filePath -Value $frontmatter -Encoding UTF8

        # Sync the session stub to the database (best-effort, background)
        $syncScript = Join-Path $PSScriptRoot "vault-sync-to-db.ps1"
        if (Test-Path $syncScript) {
            Start-Job -ScriptBlock {
                param($script, $path)
                & powershell -NoProfile -File $script -FilePath $path 2>&1 | Out-Null
            } -ArgumentList $syncScript, $filePath | Out-Null
        }
    }
} catch {}

# ── Reflection hint file ─────────────────────────────────────────────────────
# If the session had enough loops (≥5), write a pending_reflection.json so that
# session-start.ps1 injects a memory-check reminder on the NEXT session.
if ([int]$loopCount -ge 5) {
    try {
        $logsDir = ".galdr/logs"
        if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir -Force | Out-Null }
        $reflectionData = @{
            conversation_id = $conversationId
            loop_count      = [int]$loopCount
            status          = $status
        }
        $reflectionData | ConvertTo-Json -Compress | Set-Content -Path "$logsDir/pending_reflection.json" -Encoding UTF8
    } catch {}
}

$response = @{}
$response | ConvertTo-Json -Compress
exit 0
