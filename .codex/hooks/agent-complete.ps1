# agent-complete.ps1 - Cursor hook for agent/stop lifecycle
# Triggered when the agent loop ends.
# Writes a reflection hint so session-start can remind you about your last session.

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
