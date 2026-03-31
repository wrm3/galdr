---
description: "Manage the heartbeat scheduler — run routines, check status, configure schedules"
---

# g-heartbeat

Manage the galdr heartbeat scheduler for autonomous agent work.

## Usage

- `@g-heartbeat` — Show heartbeat status and configured routines
- `@g-heartbeat run <routine-name>` — Manually trigger a specific routine
- `@g-heartbeat status` — Show last run times and budget usage
- `@g-heartbeat enable <routine-name>` — Enable a routine in HEARTBEAT.md
- `@g-heartbeat disable <routine-name>` — Disable a routine

## Behavior

1. Read the `g-heartbeat` skill at `.cursor/skills/g-heartbeat/SKILL.md`
2. Follow the skill instructions for the requested operation
3. For `run`: invoke the heartbeat-scheduler.ps1 with `-Run` parameter
4. For `status`: read HEARTBEAT.md, budget_tracker.json, and recent logs
5. For `enable`/`disable`: edit HEARTBEAT.md routine's Enabled field
