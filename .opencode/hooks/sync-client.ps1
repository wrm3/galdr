# sync-client.ps1 — Push .galdr/ files to server via WebSocket
# Triggered on session-start (after session-start.ps1) or manually.
# Graceful fallback: if server is unreachable, silently skips (file-first, C-003).
#
# Cross-platform: PowerShell 5.1+ (Windows) and PowerShell Core (Linux/macOS).

param(
    [switch]$Force
)

$ErrorActionPreference = "SilentlyContinue"

# ── Resolve project root ─────────────────────────────────────────────────────
$projectRoot = (Get-Location).Path
$galdrDir = Join-Path $projectRoot ".galdr"

if (-not (Test-Path $galdrDir)) {
    exit 0
}

# ── Read project_id ──────────────────────────────────────────────────────────
$projectIdFile = Join-Path $galdrDir ".project_id"
if (-not (Test-Path $projectIdFile)) { exit 0 }
$projectId = (Get-Content $projectIdFile -Raw).Trim()
if (-not $projectId -or $projectId -match '^\{') { exit 0 }

# ── Read user_id ─────────────────────────────────────────────────────────────
$userIdFile = Join-Path $galdrDir ".user_id"
$userId = ""
if (Test-Path $userIdFile) {
    $userId = (Get-Content $userIdFile -Raw).Trim()
    if ($userId -match '^\{') { $userId = "" }
}

# ── Read server URL ──────────────────────────────────────────────────────────
# Priority: .galdr/.server_url -> env GALDR_SERVER_URL -> default
$serverUrlFile = Join-Path $galdrDir ".server_url"
$serverUrl = $env:GALDR_SERVER_URL

if (Test-Path $serverUrlFile) {
    $serverUrl = (Get-Content $serverUrlFile -Raw).Trim()
}

if (-not $serverUrl) {
    $serverUrl = "ws://localhost:8082"
}

# Normalize: ensure ws:// prefix
if ($serverUrl -match '^https?://') {
    $serverUrl = $serverUrl -replace '^http://', 'ws://' -replace '^https://', 'wss://'
}
if ($serverUrl -notmatch '^wss?://') {
    $serverUrl = "ws://$serverUrl"
}

# ── Read vault_id (optional) ─────────────────────────────────────────────────
$vaultId = ""
$vaultLocFile = Join-Path $galdrDir ".vault_location"
if (Test-Path $vaultLocFile) {
    $vaultLoc = (Get-Content $vaultLocFile -Raw).Trim()
    if ($vaultLoc -and $vaultLoc -ne "local") {
        $vaultId = [System.IO.Path]::GetFileName($vaultLoc)
    }
}

# ── Collect .galdr/ files ────────────────────────────────────────────────────
$skipPatterns = @("logs", ".user_id", ".project_id", ".server_url")

function Get-GaldrFiles {
    $files = @()
    $allFiles = Get-ChildItem -Path $galdrDir -Recurse -File -ErrorAction SilentlyContinue

    foreach ($f in $allFiles) {
        $relPath = $f.FullName.Substring($galdrDir.Length + 1).Replace("\", "/")

        # Skip excluded patterns
        $skip = $false
        foreach ($pattern in $skipPatterns) {
            if ($relPath -like "$pattern*" -or $relPath -eq $pattern) {
                $skip = $true
                break
            }
        }
        if ($skip) { continue }

        $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
        if ($null -eq $content) { continue }

        $hash = [System.BitConverter]::ToString(
            [System.Security.Cryptography.SHA256]::Create().ComputeHash(
                [System.Text.Encoding]::UTF8.GetBytes($content)
            )
        ).Replace("-", "").Substring(0, 16).ToLower()

        $files += @{
            path      = $relPath
            content   = $content
            hash      = $hash
            file_type = "galdr"
        }
    }
    return $files
}

# ── Collect vault files (if shared vault configured) ─────────────────────────
function Get-VaultFiles {
    param([string]$VaultPath)
    $files = @()
    if (-not (Test-Path $VaultPath)) { return $files }

    $vaultSkip = @("_index.yaml", ".crawl_schedule.json")
    $allFiles = Get-ChildItem -Path $VaultPath -Recurse -File -Include "*.md" -ErrorAction SilentlyContinue | Select-Object -First 200

    foreach ($f in $allFiles) {
        $relPath = $f.FullName.Substring($VaultPath.Length + 1).Replace("\", "/")

        $skip = $false
        foreach ($pattern in $vaultSkip) {
            if ($relPath -eq $pattern) { $skip = $true; break }
        }
        if ($skip) { continue }

        $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
        if ($null -eq $content) { continue }
        if ($content.Length -gt 100000) { continue }

        $hash = [System.BitConverter]::ToString(
            [System.Security.Cryptography.SHA256]::Create().ComputeHash(
                [System.Text.Encoding]::UTF8.GetBytes($content)
            )
        ).Replace("-", "").Substring(0, 16).ToLower()

        $files += @{
            path      = $relPath
            content   = $content
            hash      = $hash
            file_type = "vault"
        }
    }
    return $files
}

# ── WebSocket sync ───────────────────────────────────────────────────────────
$wsUrl = "$serverUrl/sync/$projectId"
if ($userId) { $wsUrl += "?user_id=$userId" }
if ($vaultId) {
    $sep = if ($userId) { "&" } else { "?" }
    $wsUrl += "${sep}vault_id=$vaultId"
}

try {
    $ws = New-Object System.Net.WebSockets.ClientWebSocket
    $ws.Options.SetRequestHeader("X-Galdr-Project", $projectId)

    $cts = New-Object System.Threading.CancellationTokenSource
    $cts.CancelAfter(5000)

    $connectTask = $ws.ConnectAsync([Uri]$wsUrl, $cts.Token)
    $connectTask.Wait()

    if ($ws.State -ne [System.Net.WebSockets.WebSocketState]::Open) {
        exit 0
    }

    $files = Get-GaldrFiles

    # Add vault files if shared vault is configured
    if ($vaultId) {
        $vaultLocContent = (Get-Content $vaultLocFile -Raw).Trim()
        if (Test-Path $vaultLocContent) {
            $vaultFiles = Get-VaultFiles -VaultPath $vaultLocContent
            $files += $vaultFiles
        }
    }

    foreach ($file in $files) {
        $msg = @{
            type      = "file_changed"
            path      = $file.path
            content   = $file.content
            hash      = $file.hash
            file_type = $file.file_type
        } | ConvertTo-Json -Depth 3 -Compress

        $bytes = [System.Text.Encoding]::UTF8.GetBytes($msg)
        $segment = New-Object System.ArraySegment[byte] -ArgumentList @(,$bytes)
        $sendTask = $ws.SendAsync($segment, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None)
        $sendTask.Wait()

        # Read ack (non-blocking, 2s timeout)
        $recvBuf = New-Object byte[] 4096
        $recvSeg = New-Object System.ArraySegment[byte] -ArgumentList @(,$recvBuf)
        $recvCts = New-Object System.Threading.CancellationTokenSource
        $recvCts.CancelAfter(2000)
        try {
            $recvTask = $ws.ReceiveAsync($recvSeg, $recvCts.Token)
            $recvTask.Wait()
        } catch { }
    }

    # Graceful close
    $closeCts = New-Object System.Threading.CancellationTokenSource
    $closeCts.CancelAfter(2000)
    try {
        $closeTask = $ws.CloseAsync(
            [System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure,
            "sync complete",
            $closeCts.Token
        )
        $closeTask.Wait()
    } catch { }

} catch {
    # Server unreachable — silently skip (file-first fallback)
    exit 0
} finally {
    if ($ws) { $ws.Dispose() }
}
