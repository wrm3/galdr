# audit.ps1 - Cursor hook for auditing all tool events
# Logs to .galdr/logs/ (project-local, safe with symlinked .cursor/).
# Source system tagged [cursor] in every entry.

. (Join-Path $PSScriptRoot "sanitize-logs.ps1")

$inputJson = $input | Out-String
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

# Write to .galdr/logs/ — project-local, never inside the symlinked .cursor/ dir
$logDir = ".galdr/logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

try {
    $eventData = $inputJson | ConvertFrom-Json
    $hookEvent = $eventData.hook_event_name
    if (-not $hookEvent) { $hookEvent = "unknown" }
} catch {
    $hookEvent = "unknown"
}

$datePrefix = Get-Date -Format "yyyy-MM-dd"
$logFile    = "$logDir/${datePrefix}_agent-audit.log"

# Sanitize before writing — replaces real key values with [VAR_NAME]
$safeJson  = Invoke-Sanitize $inputJson
$logEntry  = "[$timestamp] [cursor] [$hookEvent] $safeJson"
Add-Content -Path $logFile -Value $logEntry

Write-Output "{}"
exit 0
