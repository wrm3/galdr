# validate-shell.ps1 - Cursor hook for shell command validation

. (Join-Path $PSScriptRoot "sanitize-logs.ps1")

$inputJson = $input | Out-String

try {
    $eventData = $inputJson | ConvertFrom-Json
    $command   = $eventData.command
    $cwd       = $eventData.cwd
} catch {
    $command = ""
    $cwd     = ""
}

$response = @{ permission = "allow" }

$dangerousPatterns = @(
    "rm -rf /",
    "rm -rf /*",
    "format c:",
    "del /s /q c:\*",
    ":(){:|:&};:"
)

foreach ($pattern in $dangerousPatterns) {
    if ($command -like "*$pattern*") {
        $response = @{
            permission    = "deny"
            user_message  = "Dangerous command blocked: $pattern"
            agent_message = "This command has been blocked by a security hook because it matches a dangerous pattern."
        }
        $response | ConvertTo-Json -Compress
        exit 2
    }
}

# Write to .galdr/logs/ — project-local, safe with symlinked .cursor/
$logDir = ".galdr/logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$datePrefix = Get-Date -Format "yyyy-MM-dd"
$logFile    = "$logDir/${datePrefix}_shell_commands.log"
$timestamp  = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$safeCmd    = Invoke-Sanitize $command
$logEntry   = "[$timestamp] [cursor] [SHELL] Command: $safeCmd | CWD: $cwd"
Add-Content -Path $logFile -Value $logEntry

$response | ConvertTo-Json -Compress
exit 0
