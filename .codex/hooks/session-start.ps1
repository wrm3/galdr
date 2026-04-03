# session-start.ps1 - Cursor hook for session initialization
# Triggered when a new composer conversation is created.
# Injects past agent-memory context so the AI has continuity across sessions.

$inputJson = $input | Out-String

try {
    $eventData    = $inputJson | ConvertFrom-Json
    $sessionId    = $eventData.session_id
    $composerMode = $eventData.composer_mode
} catch {
    $sessionId    = "unknown"
    $composerMode = "unknown"
}

# ── User identity resolution ─────────────────────────────────────────────────
# Priority: .galdr/.user_id -> %APPDATA%/galdr/user_config.json -> prompt setup
$projectUserIdFile = Join-Path (Get-Location).Path ".galdr\.user_id"
$userId       = $null
$setupNeeded  = $false

# Cross-platform appdata path
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
            # Populate .galdr/.user_id from appdata for future fast reads
            try {
                Set-Content -Path $projectUserIdFile -Value $userId -Encoding UTF8
            } catch {}
        }
    } catch {}
}

# Step 3: If still no user_id, create skeleton appdata config and flag setup
if (-not $userId) {
    $setupNeeded = $true
    try {
        $appDataDir = Split-Path $appDataConfig -Parent
        if (-not (Test-Path $appDataDir)) {
            New-Item -ItemType Directory -Path $appDataDir -Force | Out-Null
        }
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

# ── Reflection reminder (letta-style step-count trigger) ─────────────────────
$setupBanner = ""
if ($setupNeeded) {
    $setupBanner = @"
## GALDR FIRST-TIME SETUP NEEDED
Your galdr user ID has not been configured yet.

**Quick setup:** Edit `.galdr/.user_id` and replace `{SETUP_NEEDED}` with your user ID (e.g. `usr_alice`).

**Full setup:** Also create `$appDataConfig` with:
```json
{
  "user_id": "usr_alice",
  "display_name": "Alice",
  "machine_id": "(auto-generated)",
  "platform": "windows"
}
```

AI memory features will work but sessions won't be linked to a named user until setup is complete.

---
"@
}

$reflectionBanner = ""
$reflectionFile   = ".galdr/logs/pending_reflection.json"
if (Test-Path $reflectionFile) {
    try {
        $reflData    = Get-Content $reflectionFile -Raw | ConvertFrom-Json
        $sessionSize = 0
        if ($reflData.turn_count)  { $sessionSize = [int]$reflData.turn_count }
        elseif ($reflData.loop_count) { $sessionSize = [int]$reflData.loop_count }

        if ($sessionSize -ge 5) {
            $topicHint = ""
            if ($reflData.recent_topics -and $reflData.recent_topics.Count -gt 0) {
                $topicHint = "`nSession covered (rough summary from first/last messages):`n"
                foreach ($t in $reflData.recent_topics) { $topicHint += "  - $t`n" }
            }

            $reflectionBanner = @"
## Memory Check Reminder
Your previous session had $sessionSize turns.$topicHint
Consider running **``@g-continual-learning``** to scan recent transcripts and update AGENTS.md with durable facts.

Alternatively, call **``memory_capture_insight``** for individual insights:
- **procedure** — how to do something (deploy, test, git workflow)
- **preference** — user preferences (code style, naming, formatting)
- **correction** — mistakes to avoid next time
- **decision** — architectural choices + rationale
- **context** — project background worth remembering

---
"@
        }
        Remove-Item $reflectionFile -ErrorAction SilentlyContinue
    } catch {
        Remove-Item $reflectionFile -ErrorAction SilentlyContinue
    }
}

$additionalContext = "${setupBanner}${reflectionBanner}galdr task management system is active. Check .galdr/TASKS.md for current tasks."

# ── Fallback Drain ────────────────────────────────────────────────────────────
$fallbackFile = ".galdr/memory_fallback.jsonl"
if (Test-Path $fallbackFile) {
    try {
        $mcpUrlFallback = "http://localhost:8082"
        if (Test-Path $appDataConfig) {
            try {
                $ucFallback = Get-Content $appDataConfig -Raw | ConvertFrom-Json
                if ($ucFallback.mcp_url) { $mcpUrlFallback = $ucFallback.mcp_url.TrimEnd("/") }
            } catch {}
        }

        Invoke-WebRequest -Uri "$mcpUrlFallback/memory/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop | Out-Null

        $lines = Get-Content $fallbackFile
        $failedLines = @()
        foreach ($line in $lines) {
            $line = $line.Trim()
            if (-not $line) { continue }
            try {
                $headers = @{ "Content-Type" = "application/json" }
                Invoke-WebRequest -Uri "$mcpUrlFallback/memory/ingest" -Method POST -Body $line -Headers $headers -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop | Out-Null
            } catch {
                $failedLines += $line
            }
        }

        if ($failedLines.Count -eq 0) {
            Remove-Item $fallbackFile -ErrorAction SilentlyContinue
        } else {
            Set-Content -Path $fallbackFile -Value ($failedLines -join "`n") -Encoding UTF8
        }
    } catch {}
}

# ── .project_id auto-heal ────────────────────────────────────────────────────
$projectIdFile = ".galdr/.project_id"
if (Test-Path $projectIdFile) {
    $projectId = (Get-Content $projectIdFile -Raw).Trim()
    $uuidPattern = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    if (-not ($projectId -match $uuidPattern)) {
        $projectId = [guid]::NewGuid().ToString()
        try { Set-Content -Path $projectIdFile -Value $projectId -Encoding UTF8 } catch {}
    }
}

# ── Memory Context Retrieval ─────────────────────────────────────────────────
if (Test-Path $projectIdFile) {
    $projectId = (Get-Content $projectIdFile -Raw).Trim()
    if ($projectId -ne "" -and $projectId -ne "{GENERATED_ON_INSTALL}") {
        try {
            $mcpUrl = "http://localhost:8082"
            if (Test-Path $appDataConfig) {
                try {
                    $userConfig = Get-Content $appDataConfig -Raw | ConvertFrom-Json
                    if ($userConfig.mcp_url) { $mcpUrl = $userConfig.mcp_url.TrimEnd("/") }
                } catch {}
            }

            $resp = Invoke-WebRequest -Uri "$mcpUrl/memory/context?project_id=$projectId&max_tokens=3000&platform=cursor" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
            $body = $resp.Content | ConvertFrom-Json

            if ($body.success -and $body.context -ne "") {
                $additionalContext = @"
$($body.context)

---
galdr task management system is active. Check .galdr/TASKS.md for current tasks.
"@
            }
        } catch {}
    }
}

# ── Vault migration (auto-migrate .galdr/vault/ -> shared when .vault_location is set) ──
try {
    . "$PSScriptRoot\vault-resolve.ps1"
    $localVault = Join-Path (Get-Location).Path ".galdr\vault"
    if ($VaultPath -and $VaultPath -ne $localVault -and (Test-Path $localVault)) {
        $localFiles = Get-ChildItem -Path $localVault -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
        if ($localFiles -and $localFiles.Count -gt 0) {
            $migrated = 0
            foreach ($file in $localFiles) {
                $relPath = $file.FullName.Substring($localVault.Length).TrimStart('\', '/')
                $destPath = Join-Path $VaultPath $relPath
                $destDir = Split-Path $destPath -Parent
                if (-not (Test-Path $destDir)) {
                    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                }
                if (-not (Test-Path $destPath)) {
                    Copy-Item -Path $file.FullName -Destination $destPath -Force
                    $migrated++
                } else {
                    $srcHash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
                    $dstHash = (Get-FileHash $destPath -Algorithm SHA256).Hash
                    if ($srcHash -ne $dstHash) {
                        Copy-Item -Path $file.FullName -Destination $destPath -Force
                        $migrated++
                    }
                }
            }
            if ($migrated -gt 0) {
                Remove-Item -Path $localVault -Recurse -Force -ErrorAction SilentlyContinue
                $additionalContext += "`n`n## Vault Auto-Migration`nMigrated $migrated notes from .galdr/vault/ to $VaultPath. Local vault cleaned up.`n"
            }
        }
    }
} catch {}

# ── Response ─────────────────────────────────────────────────────────────────
$response = @{
    continue           = $true
    additional_context = $additionalContext
}

$response | ConvertTo-Json -Compress
exit 0
