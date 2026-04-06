# g-hk-agent-complete.ps1 - Cursor hook for agent/stop lifecycle
# Triggered when the agent loop ends.
# Persists a local chat log and writes a reflection hint for the next session.

$inputJson = $input | Out-String

try {
    $eventData      = $inputJson | ConvertFrom-Json
    $status         = $eventData.status
    $loopCount      = $eventData.loop_count
    $conversationId = $eventData.conversation_id
    $transcriptPath = $eventData.transcript_path
} catch {
    $status         = "unknown"
    $loopCount      = 0
    $conversationId = "unknown"
    $transcriptPath = $null
}

# Write a local chat transcript in the background using Cursor's state.vscdb.
try {
    $projectPath   = (Get-Location).Path
    $loggerScript  = Join-Path $PSScriptRoot "g-hk-cursor-chat-logger.py"

    if (Test-Path $loggerScript) {
        $pythonCmd = $null
        if (Get-Command py -ErrorAction SilentlyContinue) {
            $pythonCmd = "py"
            $pythonArgs = @(
                "-3",
                $loggerScript,
                "--project-path", $projectPath,
                "--loop-count",   $loopCount,
                "--status",       $(if ($status -eq "success") { "completed" } else { "partial" }),
                "--platform",     "cursor"
            )
        } elseif (Get-Command python -ErrorAction SilentlyContinue) {
            $pythonCmd = "python"
            $pythonArgs = @(
                $loggerScript,
                "--project-path", $projectPath,
                "--loop-count",   $loopCount,
                "--status",       $(if ($status -eq "success") { "completed" } else { "partial" }),
                "--platform",     "cursor"
            )
        } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
            $pythonCmd = "python3"
            $pythonArgs = @(
                $loggerScript,
                "--project-path", $projectPath,
                "--loop-count",   $loopCount,
                "--status",       $(if ($status -eq "success") { "completed" } else { "partial" }),
                "--platform",     "cursor"
            )
        }

        if ($pythonCmd) {
            if ($conversationId -and $conversationId -ne "unknown") {
                $pythonArgs += "--conversation-id"
                $pythonArgs += $conversationId
            }
            if ($transcriptPath) {
                $pythonArgs += "--transcript-path"
                $pythonArgs += $transcriptPath
            }

            Start-Job -ScriptBlock {
                param($exe, $cliArgs)
                & $exe @cliArgs 2>&1 | Out-Null
            } -ArgumentList $pythonCmd, $pythonArgs | Out-Null
        }
    }
} catch {}

# If session had enough turns, write a reflection hint for next session-start
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

@{} | ConvertTo-Json -Compress
exit 0
