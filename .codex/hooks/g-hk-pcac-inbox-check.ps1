# g-hk-pcac-inbox-check.ps1
# Cross-project INBOX scanner. Called by g-hk-session-start.ps1.
# Read-only — never modifies INBOX.md.
# Outputs a summary line or a WARNING block for CONFLICT items.
# Completes in <1 second (simple file read + grep).

param(
    [string]$ProjectRoot = (Get-Location).Path
)

$inboxPath = Join-Path $ProjectRoot ".galdr\linking\INBOX.md"

# Graceful: linking/ not configured
if (-not (Test-Path $inboxPath)) {
    Write-Output "INBOX: not configured"
    return
}

$lines = Get-Content $inboxPath -ErrorAction SilentlyContinue

if (-not $lines) {
    Write-Output "INBOX: clear"
    return
}

# Count open items by type (lines starting with "## [OPEN]" followed by type keyword)
$conflicts  = @($lines | Where-Object { $_ -match "^\s*-\s*\[\s*\]" -and $_ -match "\[CONFLICT\]|CONFLICT" }).Count
$requests   = @($lines | Where-Object { $_ -match "REQ-\d+" -and $_ -match "\[OPEN\]" }).Count
$broadcasts = @($lines | Where-Object { $_ -match "BCAST-\d+" -and $_ -match "\[OPEN\]" }).Count
$syncs      = @($lines | Where-Object { $_ -match "SYNC-\d+" -and $_ -match "\[OPEN\]" }).Count

# Also count CONFLICT section headers (## [CONFLICT] section with content)
$inConflictSection = $false
$conflictItems = 0
foreach ($line in $lines) {
    if ($line -match "^## \[CONFLICT\]") { $inConflictSection = $true; continue }
    if ($line -match "^## \[" -and $line -notmatch "^## \[CONFLICT\]") { $inConflictSection = $false }
    if ($inConflictSection -and $line -match "^\s*-\s*\[") { $conflictItems++ }
}

# Merge both counts
$totalConflicts = [Math]::Max($conflicts, $conflictItems)
$total = $totalConflicts + $requests + $broadcasts + $syncs

if ($total -eq 0) {
    Write-Output "INBOX: clear"
    return
}

if ($totalConflicts -gt 0) {
    Write-Output ""
    Write-Output "⚠️  INBOX WARNING — $totalConflicts CONFLICT item(s) detected"
    Write-Output "   Conflicts MUST be resolved via @g-pcac-read before any other work."
    Write-Output "   File: .galdr/linking/INBOX.md"
    Write-Output ""
} else {
    $parts = @()
    if ($requests -gt 0)   { $parts += "$requests request(s)" }
    if ($broadcasts -gt 0) { $parts += "$broadcasts broadcast(s)" }
    if ($syncs -gt 0)      { $parts += "$syncs sync(s)" }
    $detail = if ($parts.Count -gt 0) { " (" + ($parts -join ", ") + ")" } else { "" }
    Write-Output "INBOX: $total open${detail}"
}
