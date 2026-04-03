# session-start.ps1 - Cursor hook for session initialization
# Triggered when a new composer conversation is created.
# Injects galdr context and handles first-time user setup.

$inputJson = $input | Out-String

# ── User identity resolution ──────────────────────────────────────────────────
$projectUserIdFile = Join-Path (Get-Location).Path ".galdr\.user_id"
$userId      = $null
$setupNeeded = $false

if ($env:APPDATA) {
    $appDataConfig = Join-Path $env:APPDATA "galdr\user_config.json"
} else {
    $appDataConfig = Join-Path $env:HOME ".config/galdr/user_config.json"
}

# Step 1: Try .galdr/.user_id
if (Test-Path $projectUserIdFile) {
    $candidate = (Get-Content $projectUserIdFile -Raw).Trim()
    if ($candidate -and $candidate -ne '' -and $candidate -ne '{SETUP_NEEDED}') {
        $userId = $candidate
    }
}

# Step 2: Fallback to appdata config
if (-not $userId -and (Test-Path $appDataConfig)) {
    try {
        $appCfg = Get-Content $appDataConfig -Raw | ConvertFrom-Json
        if ($appCfg.user_id -and $appCfg.user_id -ne 'SETUP_NEEDED') {
            $userId = $appCfg.user_id
            try { Set-Content -Path $projectUserIdFile -Value $userId -Encoding UTF8 } catch {}
        }
    } catch {}
}

# Step 3: No user_id found — flag setup needed
if (-not $userId) {
    $setupNeeded = $true
    try {
        $appDataDir = Split-Path $appDataConfig -Parent
        if (-not (Test-Path $appDataDir)) { New-Item -ItemType Directory -Path $appDataDir -Force | Out-Null }
        if (-not (Test-Path $appDataConfig)) {
            $machineId = ""
            try {
                $machineId = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Cryptography" `
                              -Name "MachineGuid" -ErrorAction Stop).MachineGuid
            } catch {}
            if (-not $machineId) { $machineId = [System.Guid]::NewGuid().ToString() }
            $cfg = [ordered]@{
                user_id         = "SETUP_NEEDED"
                display_name    = ""
                machine_id      = $machineId
                platform        = "windows"
                created_at      = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                setup_completed = $false
            }
            $cfg | ConvertTo-Json | Set-Content -Path $appDataConfig -Encoding UTF8
        }
    } catch {}
}

# ── .project_id auto-heal ─────────────────────────────────────────────────────
$projectIdFile = ".galdr/.project_id"
if (Test-Path $projectIdFile) {
    $projectId   = (Get-Content $projectIdFile -Raw).Trim()
    $uuidPattern = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    if (-not ($projectId -match $uuidPattern)) {
        $projectId = [guid]::NewGuid().ToString()
        try { Set-Content -Path $projectIdFile -Value $projectId -Encoding UTF8 } catch {}
    }
}

# ── Build context message ─────────────────────────────────────────────────────
$setupBanner = ""
if ($setupNeeded) {
    $setupBanner = @"
## GALDR FIRST-TIME SETUP NEEDED
Your galdr user ID has not been configured yet.

**Quick setup:** Edit `.galdr/.user_id` and replace `{SETUP_NEEDED}` with your user ID (e.g. `usr_alice`).

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
