# vault-sync-to-db.ps1
# Syncs a single vault .md file (or all files) to the database via the MCP HTTP endpoint.
# Called by agent-complete.ps1 after writing session stubs, or manually for bulk sync.
#
# Usage:
#   . vault-sync-to-db.ps1 -FilePath "G:\knowledge_well\projects\...\sessions\2026-03-24_123456_abc.md"
#   . vault-sync-to-db.ps1 -BulkSync   # syncs all .md files in the vault

param(
    [string]$FilePath,
    [switch]$BulkSync,
    [string]$McpUrl = "http://localhost:8082/mcp"
)

. "$PSScriptRoot\vault-resolve.ps1"

function Invoke-VaultSync {
    param([string]$RelPath, [string]$Content)

    try {
        # Initialize MCP session
        $initBody = @{
            jsonrpc = "2.0"; id = 0; method = "initialize"
            params = @{ protocolVersion = "2025-03-26"; capabilities = @{}; clientInfo = @{ name = "hook"; version = "1.0" } }
        } | ConvertTo-Json -Depth 5
        $headers = @{ "Content-Type" = "application/json"; "Accept" = "application/json, text/event-stream" }
        $initResp = Invoke-RestMethod -Uri $McpUrl -Method Post -Body $initBody -Headers $headers -ErrorAction Stop
        # Session ID is in response headers — for simplicity, use a fresh session per call

        # Send initialized notification
        $notifBody = @{ jsonrpc = "2.0"; method = "notifications/initialized" } | ConvertTo-Json
        Invoke-RestMethod -Uri $McpUrl -Method Post -Body $notifBody -Headers $headers -ErrorAction SilentlyContinue

        # Call vault_sync
        $syncBody = @{
            jsonrpc = "2.0"; id = 1; method = "tools/call"
            params = @{
                name = "vault_sync"
                arguments = @{ path = $RelPath; content = $Content; mode = "ingest" }
            }
        } | ConvertTo-Json -Depth 5 -Compress
        $resp = Invoke-RestMethod -Uri $McpUrl -Method Post -Body $syncBody -Headers $headers -TimeoutSec 30 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

if ($BulkSync) {
    $count = 0; $failed = 0
    Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" | ForEach-Object {
        $relPath = $_.FullName.Substring($VaultPath.Length + 1).Replace("\", "/")
        $content = Get-Content $_.FullName -Raw -Encoding UTF8
        $ok = Invoke-VaultSync -RelPath $relPath -Content $content
        if ($ok) { $count++ } else { $failed++ }
    }
    Write-Host "Bulk sync: $count synced, $failed failed"
} elseif ($FilePath -and (Test-Path $FilePath)) {
    $relPath = $FilePath.Substring($VaultPath.Length + 1).Replace("\", "/")
    $content = Get-Content $FilePath -Raw -Encoding UTF8
    $ok = Invoke-VaultSync -RelPath $relPath -Content $content
    if ($ok) { Write-Host "Synced: $relPath" } else { Write-Host "Sync failed: $relPath" }
} else {
    Write-Host "Usage: vault-sync-to-db.ps1 -FilePath <path> OR -BulkSync"
}
