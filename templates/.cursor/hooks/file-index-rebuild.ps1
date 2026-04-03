# file-index-rebuild.ps1
#
# Triggers a galdr file index rebuild via the MCP server.
# Called by session-start.ps1 on first session of the day (max once per 12 hours).
# Can also be called manually: .\file-index-rebuild.ps1 [-Force]
#
# What this does:
#   Calls file_index(action='rebuild') on the MCP server, which walks all
#   active project roots and rebuilds the PostgreSQL file index.
#   This lets the AI use file_index(action='find'/'grep'/'read') to see
#   gitignored files that Cursor's Glob/Grep tools cannot access.
#
# Scope:
#   Indexes all active projects listed in C-011:
#     G:\galdr, G:\Maestro2, P:\hieroglyphics,
#     G:\CatchTheFraqUp, G:\CBTrade, G:\Future_Shadows_AI
#   Respects .galdrignore files in each root directory.

param(
    [switch]$Force,       # Force full rebuild (drops and recreates index)
    [switch]$Silent       # Suppress output (for hook invocations)
)

$MCP_URL     = "http://localhost:8092"
$STATE_DIR   = Join-Path $PSScriptRoot "state"
$STAMP_FILE  = Join-Path $STATE_DIR "file-index-last-rebuild.txt"
$MIN_HOURS   = 12   # rebuild at most once every 12 hours (unless -Force)

# Active project roots (C-011 registry)
$ROOTS = @(
    "G:\galdr",
    "G:\Maestro2",
    "P:\hieroglyphics",
    "G:\CatchTheFraqUp",
    "G:\CBTrade",
    "G:\Future_Shadows_AI"
)

# ── State dir ────────────────────────────────────────────────────────────────
if (-not (Test-Path $STATE_DIR)) {
    New-Item -ItemType Directory -Path $STATE_DIR -Force | Out-Null
}

# ── Cooldown check ────────────────────────────────────────────────────────────
if (-not $Force -and (Test-Path $STAMP_FILE)) {
    $lastRun = [datetime](Get-Content $STAMP_FILE -Raw).Trim()
    $hoursSince = [math]::Round(([datetime]::UtcNow - $lastRun).TotalHours, 1)
    if ($hoursSince -lt $MIN_HOURS) {
        if (-not $Silent) {
            Write-Host "file-index: skipping rebuild ($hoursSince h since last run, min $MIN_HOURS h). Use -Force to override."
        }
        exit 0
    }
}

# ── MCP health check ──────────────────────────────────────────────────────────
try {
    $healthCheck = Invoke-WebRequest -Uri "$MCP_URL/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    if ($healthCheck.StatusCode -ne 200) { throw "non-200" }
} catch {
    if (-not $Silent) {
        Write-Host "file-index: MCP server not reachable at $MCP_URL — skipping rebuild."
        Write-Host "           Start Docker: cd G:\galdr\docker && docker compose up -d"
    }
    exit 0
}

# ── Build MCP tool call payload ───────────────────────────────────────────────
$payload = @{
    tool   = "file_index"
    params = @{
        action        = "rebuild"
        roots         = $ROOTS
        force_rebuild = $Force.IsPresent
    }
} | ConvertTo-Json -Depth 5

# ── Call MCP ──────────────────────────────────────────────────────────────────
$startTime = Get-Date
try {
    $response = Invoke-WebRequest `
        -Uri "$MCP_URL/tool" `
        -Method POST `
        -Body $payload `
        -ContentType "application/json" `
        -UseBasicParsing `
        -TimeoutSec 120 `
        -ErrorAction Stop

    $result = $response.Content | ConvertFrom-Json
    $elapsed = [math]::Round(((Get-Date) - $startTime).TotalSeconds, 1)

    # ── Write timestamp ───────────────────────────────────────────────────────
    [datetime]::UtcNow.ToString("o") | Set-Content $STAMP_FILE

    if (-not $Silent) {
        Write-Host ""
        Write-Host "📂 File Index Rebuilt ($elapsed s)" -ForegroundColor Cyan
        Write-Host "   Roots indexed : $($result.roots_indexed.Count)"
        Write-Host "   Files added   : $($result.files_added)"
        Write-Host "   Files updated : $($result.files_updated)"
        Write-Host "   Files ignored : $($result.files_ignored)"
        if ($result.roots_skipped -and $result.roots_skipped.Count -gt 0) {
            Write-Host "   Roots skipped : $($result.roots_skipped -join ', ')" -ForegroundColor Yellow
        }
        Write-Host "   Agent can now use: file_index(action='find'/'grep'/'read')" -ForegroundColor Green
        Write-Host ""
    }

} catch {
    if (-not $Silent) {
        Write-Host "file-index: rebuild failed: $_" -ForegroundColor Red
    }
    exit 1
}
