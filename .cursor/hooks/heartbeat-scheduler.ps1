<#
.SYNOPSIS
    galdr Heartbeat Scheduler — cron-based agent wake-ups.

.DESCRIPTION
    Parses .galdr/config/HEARTBEAT.md for routine definitions with cron expressions,
    evaluates which routines are due, enforces budget/concurrency limits,
    invokes agents via CLI adapters, and logs results.

    Run modes:
      .\heartbeat-scheduler.ps1                    # Single evaluation pass
      .\heartbeat-scheduler.ps1 -Daemon            # Loop every 60s
      .\heartbeat-scheduler.ps1 -Run "nightly-cleanup"  # Manual trigger
      .\heartbeat-scheduler.ps1 -ListRoutines      # Show configured routines

.PARAMETER Run
    Manually trigger a specific routine by name (bypasses schedule check).

.PARAMETER Daemon
    Run in a loop, checking every 60 seconds.

.PARAMETER ListRoutines
    List all configured routines and exit.

.PARAMETER ProjectRoot
    Path to the project root (defaults to walking up from script location).
#>

param(
    [string]$Run = "",
    [switch]$Daemon,
    [switch]$ListRoutines,
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "Stop"

function Find-ProjectRoot {
    param([string]$StartPath)
    if ($StartPath -and (Test-Path "$StartPath\.galdr")) { return $StartPath }
    $dir = if ($StartPath) { $StartPath } else { $PSScriptRoot }
    while ($dir) {
        if (Test-Path "$dir\.galdr") { return $dir }
        $parent = Split-Path $dir -Parent
        if ($parent -eq $dir) { break }
        $dir = $parent
    }
    return $PWD.Path
}

$Root = Find-ProjectRoot $ProjectRoot
$GaldrDir = Join-Path $Root ".galdr"
$HeartbeatFile = Join-Path $GaldrDir "config" "HEARTBEAT.md"
$LogDir = Join-Path (Join-Path $GaldrDir "logs") "heartbeat"
$LockDir = Join-Path $LogDir "locks"
$BudgetFile = Join-Path $LogDir "budget_tracker.json"
$LastRunFile = Join-Path $LogDir "last_runs.json"

if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }
if (!(Test-Path $LockDir)) { New-Item -ItemType Directory -Path $LockDir -Force | Out-Null }

# --- Cron Parser ---

function Parse-CronField {
    param([string]$Field, [int]$Min, [int]$Max)
    $values = @()
    foreach ($part in $Field.Split(',')) {
        $part = $part.Trim()
        if ($part -eq '*') {
            return @($Min..$Max)
        }
        if ($part -match '^\*/(\d+)$') {
            $step = [int]$Matches[1]
            for ($i = $Min; $i -le $Max; $i += $step) { $values += $i }
            continue
        }
        if ($part -match '^(\d+)-(\d+)$') {
            $values += @([int]$Matches[1]..[int]$Matches[2])
            continue
        }
        if ($part -match '^(\d+)-(\d+)/(\d+)$') {
            $start = [int]$Matches[1]; $end = [int]$Matches[2]; $step = [int]$Matches[3]
            for ($i = $start; $i -le $end; $i += $step) { $values += $i }
            continue
        }
        if ($part -match '^\d+$') {
            $values += [int]$part
            continue
        }
    }
    return $values | Sort-Object -Unique
}

function Test-CronMatch {
    param([string]$CronExpr, [datetime]$Time)
    $fields = $CronExpr.Trim().Split(' ', [StringSplitOptions]::RemoveEmptyEntries)
    if ($fields.Count -ne 5) { return $false }

    $minutes = Parse-CronField $fields[0] 0 59
    $hours = Parse-CronField $fields[1] 0 23
    $doms = Parse-CronField $fields[2] 1 31
    $months = Parse-CronField $fields[3] 1 12
    $dows = Parse-CronField $fields[4] 0 6

    return (
        ($Time.Minute -in $minutes) -and
        ($Time.Hour -in $hours) -and
        ($Time.Day -in $doms) -and
        ($Time.Month -in $months) -and
        ([int]$Time.DayOfWeek -in $dows)
    )
}

# --- HEARTBEAT.md Parser ---

function Parse-HeartbeatConfig {
    $content = Get-Content $HeartbeatFile -Raw -ErrorAction Stop
    $config = @{
        enabled = $false
        timezone = "UTC"
        max_concurrent = 3
        budget_limit = 5.00
        default_adapter = "claude"
        adapters = @{}
        routines = @()
    }

    if ($content -match '(?s)^---\s*\n(.*?)\n---') {
        $yaml = $Matches[1]
        if ($yaml -match 'enabled:\s*(true|false)') { $config.enabled = $Matches[1] -eq 'true' }
        if ($yaml -match 'timezone:\s*(.+)') { $config.timezone = $Matches[1].Trim() }
        if ($yaml -match 'max_concurrent_agents:\s*(\d+)') { $config.max_concurrent = [int]$Matches[1] }
        if ($yaml -match 'budget_limit_daily_usd:\s*([\d.]+)') { $config.budget_limit = [double]$Matches[1] }
        if ($yaml -match 'default_adapter:\s*(\w+)') { $config.default_adapter = $Matches[1] }
    }

    $routineBlocks = [regex]::Matches($content, '### (.+)\n((?:- .+\n?)+)')
    foreach ($block in $routineBlocks) {
        $name = $block.Groups[1].Value.Trim()
        $body = $block.Groups[2].Value
        if ($name -eq "Routines") { continue }

        $routine = @{ name = $name; schedule = ""; agent = ""; skill = ""; enabled = $false; description = "" }
        if ($body -match '\*\*Schedule\*\*:\s*`(.+?)`') { $routine.schedule = $Matches[1] }
        if ($body -match '\*\*Agent\*\*:\s*(.+)') { $routine.agent = $Matches[1].Trim() }
        if ($body -match '\*\*Skill\*\*:\s*(.+)') { $routine.skill = $Matches[1].Trim() }
        if ($body -match '\*\*Enabled\*\*:\s*(true|false)') { $routine.enabled = $Matches[1] -eq 'true' }
        if ($body -match '\*\*Description\*\*:\s*(.+)') { $routine.description = $Matches[1].Trim() }

        $config.routines += $routine
    }

    return $config
}

# --- Budget Tracking ---

function Get-DailyBudget {
    $today = (Get-Date).ToString("yyyy-MM-dd")
    if (Test-Path $BudgetFile) {
        $budget = Get-Content $BudgetFile -Raw | ConvertFrom-Json
        if ($budget.date -eq $today) { return $budget }
    }
    $budget = @{ date = $today; spent_usd = 0.0; runs = 0 }
    $budget | ConvertTo-Json | Set-Content $BudgetFile
    return $budget
}

function Add-BudgetSpend {
    param([double]$Amount)
    $budget = Get-DailyBudget
    $budget.spent_usd = [double]$budget.spent_usd + $Amount
    $budget.runs = [int]$budget.runs + 1
    $budget | ConvertTo-Json | Set-Content $BudgetFile
}

# --- Lock Management ---

function Get-ActiveLocks {
    if (!(Test-Path $LockDir)) { return @() }
    return Get-ChildItem $LockDir -Filter "*.lock" -ErrorAction SilentlyContinue
}

function New-AgentLock {
    param([string]$RoutineName, [int]$Pid, [int]$TtlMinutes = 120)
    $lock = @{
        routine = $RoutineName
        pid = $Pid
        started = (Get-Date).ToUniversalTime().ToString("o")
        ttl_minutes = $TtlMinutes
        expires = (Get-Date).AddMinutes($TtlMinutes).ToUniversalTime().ToString("o")
        last_heartbeat = (Get-Date).ToUniversalTime().ToString("o")
    }
    $lockPath = Join-Path $LockDir "$RoutineName.lock"
    $lock | ConvertTo-Json | Set-Content $lockPath
    return $lockPath
}

function Remove-AgentLock {
    param([string]$RoutineName)
    $lockPath = Join-Path $LockDir "$RoutineName.lock"
    if (Test-Path $lockPath) { Remove-Item $lockPath -Force }
}

# --- Crash Recovery ---

$RecoveryLogFile = Join-Path $LogDir "recovery.log"

function Test-ProcessAlive {
    param([int]$ProcessId)
    try {
        $proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
        return ($null -ne $proc)
    }
    catch { return $false }
}

function Invoke-CrashRecovery {
    $locks = Get-ActiveLocks
    if (!$locks -or $locks.Count -eq 0) { return @() }

    $recoveries = @()
    $now = Get-Date

    foreach ($lockFile in $locks) {
        try {
            $lockData = Get-Content $lockFile.FullName -Raw | ConvertFrom-Json
        }
        catch {
            $reason = "corrupt_lock"
            Remove-Item $lockFile.FullName -Force
            $logLine = '{0} RECOVERY lock={1} reason={2} action=removed_corrupt_lock' -f $now.ToUniversalTime().ToString("o"), $lockFile.Name, $reason
            Add-Content -Path $RecoveryLogFile -Value $logLine
            $recoveries += @{ lock = $lockFile.Name; reason = $reason; action = "removed" }
            continue
        }

        $pid = [int]$lockData.pid
        $isAlive = Test-ProcessAlive -ProcessId $pid

        if ($isAlive) {
            $lastHb = [datetime]::Parse($lockData.last_heartbeat)
            $minutesSinceHb = ($now.ToUniversalTime() - $lastHb).TotalMinutes

            if ($minutesSinceHb -gt 30) {
                try { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue } catch {}
                $reason = "stuck_killed"
                Remove-Item $lockFile.FullName -Force
                $logLine = '{0} RECOVERY lock={1} reason={2} pid={3} minutes_since_heartbeat={4} action=force_killed' -f $now.ToUniversalTime().ToString("o"), $lockFile.Name, $reason, $pid, [math]::Round($minutesSinceHb, 1)
                Add-Content -Path $RecoveryLogFile -Value $logLine
                $recoveries += @{ lock = $lockFile.Name; reason = $reason; action = "force_killed" }
            }
            elseif ($minutesSinceHb -gt 10) {
                $logLine = '{0} WARNING lock={1} reason=possibly_stuck pid={2} minutes_since_heartbeat={3}' -f $now.ToUniversalTime().ToString("o"), $lockFile.Name, $pid, [math]::Round($minutesSinceHb, 1)
                Add-Content -Path $RecoveryLogFile -Value $logLine
            }
        }
        else {
            $expires = [datetime]::Parse($lockData.expires)
            $isExpired = $now.ToUniversalTime() -gt $expires
            $reason = if ($isExpired) { "ttl_expired" } else { "stale_pid" }

            Remove-Item $lockFile.FullName -Force
            $logLine = '{0} RECOVERY lock={1} reason={2} pid={3} action=removed_lock' -f $now.ToUniversalTime().ToString("o"), $lockFile.Name, $reason, $pid
            Add-Content -Path $RecoveryLogFile -Value $logLine
            $recoveries += @{ lock = $lockFile.Name; reason = $reason; action = "removed" }
        }
    }

    if ($recoveries.Count -gt 0) {
        Write-Host ('[heartbeat] Crash recovery: cleaned {0} stale lock(s)' -f $recoveries.Count) -ForegroundColor Yellow
    }

    return $recoveries
}

# --- Last Run Tracking ---

function Get-LastRuns {
    if (Test-Path $LastRunFile) {
        return Get-Content $LastRunFile -Raw | ConvertFrom-Json -AsHashtable
    }
    return @{}
}

function Set-LastRun {
    param([string]$RoutineName)
    $runs = Get-LastRuns
    $runs[$RoutineName] = (Get-Date).ToUniversalTime().ToString("o")
    $runs | ConvertTo-Json | Set-Content $LastRunFile
}

# --- Agent Invocation ---

function Invoke-AgentRoutine {
    param([hashtable]$Routine, [hashtable]$Config)

    $routineName = $Routine.name
    $timestamp = (Get-Date).ToString("yyyy-MM-dd_HHmmss")
    $logFile = Join-Path $LogDir "${timestamp}_${routineName}.md"

    Write-Host ('[heartbeat] Starting routine: {0}' -f $routineName) -ForegroundColor Cyan

    $prompt = "You are running as a scheduled heartbeat routine '$routineName'. " +
              "Execute the '$($Routine.skill)' skill workflow. " +
              "Project root: $Root. " +
              "Description: $($Routine.description). " +
              "Be thorough but concise. Output results suitable for a log file."

    $adapter = $Config.default_adapter
    $startTime = Get-Date

    $lockPath = $null
    $output = ""
    $status = "success"
    $exitCode = 0

    try {
        $lockPath = New-AgentLock -RoutineName $routineName -Pid $PID -TtlMinutes 120

        switch ($adapter) {
            "claude" {
                $result = & claude -p $prompt --output-format text 2>&1
                $output = $result -join "`n"
                $exitCode = $LASTEXITCODE
            }
            "cursor" {
                $result = & cursor agent --prompt $prompt 2>&1
                $output = $result -join "`n"
                $exitCode = $LASTEXITCODE
            }
            default {
                $output = "Adapter '$adapter' not yet implemented. Manual run required."
                $status = "skipped"
            }
        }

        if ($exitCode -ne 0) { $status = "failed" }
    }
    catch {
        $status = "failed"
        $output = $_.Exception.Message
    }
    finally {
        Remove-AgentLock -RoutineName $routineName
    }

    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds

    $logContent = @"
---
routine: $routineName
started: $($startTime.ToUniversalTime().ToString("o"))
finished: $($endTime.ToUniversalTime().ToString("o"))
duration_seconds: $([math]::Round($duration, 1))
status: $status
agent: $($Routine.agent)
skill: $($Routine.skill)
trigger: $(if ($Run) { "manual" } else { "scheduled" })
adapter: $adapter
---

# Heartbeat Run: $routineName

## Output
$output

## Status
Run completed with status: $status (exit code: $exitCode)
Duration: $([math]::Round($duration, 1)) seconds
"@

    Set-Content -Path $logFile -Value $logContent
    Set-LastRun -RoutineName $routineName

    $color = if ($status -eq "success") { "Green" } elseif ($status -eq "skipped") { "Yellow" } else { "Red" }
    Write-Host ('[heartbeat] {0} completed: {1} ({2}s)' -f $routineName, $status, [math]::Round($duration, 1)) -ForegroundColor $color

    return @{ routine = $routineName; status = $status; duration = $duration; log = $logFile }
}

# --- Main Logic ---

if (!(Test-Path $HeartbeatFile)) {
    Write-Host ('[heartbeat] No HEARTBEAT.md found at {0}' -f $HeartbeatFile) -ForegroundColor Yellow
    exit 0
}

$config = Parse-HeartbeatConfig

if ($ListRoutines) {
    Write-Host "`n=== galdr Heartbeat Routines ===" -ForegroundColor Cyan
    foreach ($r in $config.routines) {
        $enabledStr = if ($r.enabled) { "[ON]" } else { "[OFF]" }
        $color = if ($r.enabled) { "Green" } else { "DarkGray" }
        Write-Host "  $enabledStr $($r.name) — $($r.schedule) — $($r.description)" -ForegroundColor $color
    }
    Write-Host ""
    exit 0
}

if ($Run) {
    $routine = $config.routines | Where-Object { $_.name -eq $Run }
    if (!$routine) {
        Write-Host ('[heartbeat] Routine ''{0}'' not found.' -f $Run) -ForegroundColor Red
        exit 1
    }
    $result = Invoke-AgentRoutine -Routine $routine -Config $config
    Write-Host ('[heartbeat] Log: {0}' -f $result.log)
    exit $(if ($result.status -eq "success") { 0 } else { 1 })
}

function Invoke-SchedulerPass {
    Invoke-CrashRecovery

    $now = Get-Date
    $budget = Get-DailyBudget
    $activeLocks = Get-ActiveLocks
    $lastRuns = Get-LastRuns

    if (!$config.enabled) {
        Write-Host '[heartbeat] Scheduler disabled in HEARTBEAT.md' -ForegroundColor DarkGray
        return
    }

    if ([double]$budget.spent_usd -ge $config.budget_limit) {
        Write-Host ('[heartbeat] Daily budget exhausted ({0}/{1} USD)' -f $budget.spent_usd, $config.budget_limit) -ForegroundColor Yellow
        return
    }

    if ($activeLocks.Count -ge $config.max_concurrent) {
        Write-Host ('[heartbeat] Max concurrent agents reached ({0}/{1})' -f $activeLocks.Count, $config.max_concurrent) -ForegroundColor Yellow
        return
    }

    foreach ($routine in $config.routines) {
        if (!$routine.enabled) { continue }

        $alreadyRunning = $activeLocks | Where-Object { $_.BaseName -eq $routine.name }
        if ($alreadyRunning) { continue }

        if (Test-CronMatch -CronExpr $routine.schedule -Time $now) {
            $lastRun = $lastRuns[$routine.name]
            if ($lastRun) {
                $lastRunTime = [datetime]::Parse($lastRun)
                $minutesSince = ($now.ToUniversalTime() - $lastRunTime).TotalMinutes
                if ($minutesSince -lt 2) { continue }
            }

            Write-Host ('[heartbeat] Routine ''{0}'' is due - triggering' -f $routine.name) -ForegroundColor Green
            Invoke-AgentRoutine -Routine $routine -Config $config
        }
    }
}

if ($Daemon) {
    Write-Host '[heartbeat] Starting daemon mode (Ctrl+C to stop)' -ForegroundColor Cyan
    while ($true) {
        try {
            Invoke-SchedulerPass
        }
        catch {
            $errMsg = $_.Exception.Message
            Write-Host ('[heartbeat] Error: {0}' -f $errMsg) -ForegroundColor Red
        }
        Start-Sleep -Seconds 60
    }
}
else {
    Invoke-SchedulerPass
}
