# session-start.ps1 - Cursor hook for session initialization
# Triggered when a new composer conversation is created.
# Injects galdr context and handles first-time user setup.

$inputJson = $input | Out-String

# ── Read .identity file ───────────────────────────────────────────────────────
$identityFile = ".galdr\.identity"
$identity = @{ project_id=""; project_name=""; user_id=""; user_name=""; galdr_version=""; vault_location="" }
$setupNeeded = $false

if (Test-Path $identityFile) {
    Get-Content $identityFile | ForEach-Object {
        if ($_ -match "^(\w+)=(.*)$") { $identity[$Matches[1]] = $Matches[2].Trim() }
    }
}

# ── User identity resolution ──────────────────────────────────────────────────
$userId = $identity.user_id
if (-not $userId -or $userId -eq "{SETUP_NEEDED}" -or $userId -eq "") {
    # Fallback to appdata config
    $appDataConfig = if ($env:APPDATA) {
        Join-Path $env:APPDATA "galdr\user_config.json"
    } else {
        Join-Path $env:HOME ".config/galdr/user_config.json"
    }
    if (Test-Path $appDataConfig) {
        try {
            $appCfg = Get-Content $appDataConfig -Raw | ConvertFrom-Json
            if ($appCfg.user_id -and $appCfg.user_id -ne "SETUP_NEEDED") {
                $userId = $appCfg.user_id
                # Write back to .identity
                try {
                    $content = Get-Content $identityFile -Raw
                    $content = $content -replace "user_id=.*", "user_id=$userId"
                    Set-Content $identityFile $content -NoNewline
                } catch {}
            }
        } catch {}
    }
    if (-not $userId -or $userId -eq "SETUP_NEEDED") { $setupNeeded = $true }
}

# ── .project_id auto-heal ─────────────────────────────────────────────────────
$projectId = $identity.project_id
$uuidPattern = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
if (-not ($projectId -match $uuidPattern)) {
    $projectId = [guid]::NewGuid().ToString()
    try {
        $content = Get-Content $identityFile -Raw
        $content = $content -replace "project_id=.*", "project_id=$projectId"
        Set-Content $identityFile $content -NoNewline
    } catch {}
}

# ── Build context message ─────────────────────────────────────────────────────
$setupBanner = ""
if ($setupNeeded) {
    $setupBanner = @"
## GALDR FIRST-TIME SETUP NEEDED
Your galdr user ID has not been configured yet.

**Quick setup:** Edit `.galdr/.identity` and set `user_id` and `user_name` to your values.

---
"@
}

$reflectionBanner = ""
$reflectionFile   = ".galdr/logs/pending_reflection.json"
if (Test-Path $reflectionFile) {
    try {
        $reflData    = Get-Content $reflectionFile -Raw | ConvertFrom-Json
        $sessionSize = 0
        if ($reflData.loop_count) { $sessionSize = [int]$reflData.loop_count }

        if ($sessionSize -ge 5) {
            $reflectionBanner = @"
## Previous Session Reminder
Your last session had $sessionSize turns. Consider running **``@g-status``** to review where things stand.

---
"@
        }
        Remove-Item $reflectionFile -ErrorAction SilentlyContinue
    } catch {
        Remove-Item $reflectionFile -ErrorAction SilentlyContinue
    }
}

$additionalContext = "${setupBanner}${reflectionBanner}galdr task management system is active. Check .galdr/TASKS.md for current tasks."

# ── Response ──────────────────────────────────────────────────────────────────
$response = @{
    continue           = $true
    additional_context = $additionalContext
}

$response | ConvertTo-Json -Compress
exit 0
