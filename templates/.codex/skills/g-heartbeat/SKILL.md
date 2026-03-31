---
name: g-heartbeat
description: >-
  Manage the galdr heartbeat scheduler — configure routines, trigger manual runs,
  monitor status, and manage the wakeup queue. For scheduled agent work, autonomous
  sprints, and routine automation.
---

# g-heartbeat

Manage the galdr heartbeat scheduler that wakes AI agents on configurable cron schedules.

## When to Use

- Configure scheduled agent routines (cleanup, sprint, review, SWOT, ideas)
- Manually trigger a routine for testing
- Check heartbeat status and recent run logs
- Manage the wakeup queue for event-driven triggers

## Configuration

Edit `.galdr/HEARTBEAT.md` to configure routines. YAML frontmatter controls global settings:

```yaml
---
enabled: true                    # Master switch
timezone: America/Chicago        # Cron evaluation timezone
max_concurrent_agents: 3         # Max parallel agents
budget_limit_daily_usd: 5.00    # Daily cost cap
default_adapter: claude          # claude | cursor | gemini
---
```

Each routine is a `### heading` with these fields:
- **Schedule**: 5-field cron expression (minute hour dom month dow)
- **Agent**: galdr agent name
- **Skill**: galdr skill to invoke
- **Enabled**: true/false
- **Description**: What the routine does

## Status Query Script

`heartbeat_status_query.py` provides machine-readable project state as JSON without LLM invocation. Used by the scheduler to check health before/after runs, and available as a standalone CLI.

```powershell
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py status     # Full overview
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py tasks      # All tasks
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py tasks --status in_progress
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py tasks --phase 6
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py health     # Score only
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py bugs       # Open bugs
python .cursor/skills/g-heartbeat/scripts/heartbeat_status_query.py heartbeat  # Scheduler config
```

Exit codes: `0`=healthy, `1`=warnings, `2`=critical, `3`=read error.

## Commands

### Run the scheduler (single pass)
```powershell
powershell -File .cursor/hooks/heartbeat-scheduler.ps1
```

### Daemon mode (continuous, checks every 60s)
```powershell
powershell -File .cursor/hooks/heartbeat-scheduler.ps1 -Daemon
```

### Manual trigger
```powershell
powershell -File .cursor/hooks/heartbeat-scheduler.ps1 -Run "nightly-cleanup"
```

### List routines
```powershell
powershell -File .cursor/hooks/heartbeat-scheduler.ps1 -ListRoutines
```

## Run Logs

Each run produces a log at `.galdr/logs/heartbeat/{timestamp}_{routine}.md` with YAML frontmatter containing routine name, start/end times, duration, status, agent, and trigger type.

## Budget Tracking

Daily spend tracked in `.galdr/logs/heartbeat/budget_tracker.json`. Resets daily. Scheduler skips routines when budget is exhausted.

## Wakeup Queue

`.galdr/WAKEUP_QUEUE.md` holds event-driven triggers. Add rows to wake agents outside their cron schedule (e.g., when a bug is reported or a dependency unblocks).

## Cron Expression Reference

```
┌────────── minute (0-59)
│ ┌──────── hour (0-23)
│ │ ┌────── day of month (1-31)
│ │ │ ┌──── month (1-12)
│ │ │ │ ┌── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

Examples:
- `0 2 * * *` — 2:00 AM daily
- `0 8 * * 1-5` — 8:00 AM weekdays
- `0 10 * * 5` — 10:00 AM Fridays
- `*/15 * * * *` — every 15 minutes
- `0 0 1 * *` — midnight on the 1st of each month

## Default Routines

| Routine | Schedule | Purpose |
|---------|----------|---------|
| nightly-cleanup | 2:00 AM daily | TTL resets, health scoring, SPRINT.md |
| morning-sprint | 8:00 AM weekdays | Claim and implement tasks |
| weekly-review | 10:00 AM Fridays | Code review of week's changes |
| weekly-swot | 2:00 PM Fridays | Phase SWOT analysis |
| daily-ideas | Noon daily | Review idea board |
| continual-learning | 10:00 PM daily | Extract durable facts from transcripts |
