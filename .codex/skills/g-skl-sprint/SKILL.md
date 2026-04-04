---
name: g-skl-sprint
description: Autonomous 2-hour sprint — read SPRINT.md, claim tasks, implement, leave verification evidence.
---
# galdr-sprint

## When to Use
@g-sprint. Autonomous task execution — reads SPRINT.md and implements tasks.

## Pre-Flight Checks (MANDATORY — All Must Pass)
```
□ git pull — work on current state
□ Read `.galdr/PROJECT.md` — autonomous config allows this?
□ Read `.galdr/CONSTRAINTS.md` — no violations?
□ Read SPRINT.md — generated within last 2 hours? (else stale)
□ can_agents_commit_directly flag? → false = STOP
```

## Claim-First Protocol
Before writing a single line of code:
```yaml
status: in-progress
claimed_by: "sprint-agent-{timestamp}"
claimed_at: "2026-03-08T14:30:00Z"
claim_ttl_minutes: {estimated * 1.5}
claim_expires_at: "2026-03-08T16:45:00Z"
last_heartbeat: "2026-03-08T14:30:00Z"
```
```bash
git add .galdr/tasks/taskNNN_*.md
git commit -m "claim(task-NNN): sprint-agent starting work"
git push
```

## Task Selection (from SPRINT.md)
1. Filter to `ai_safe: true` tasks
2. Filter to `blast_radius: low` or `medium` (not high without human approval)
3. Sort by: dependencies resolved first, then priority
4. Skip any task with `failure_history.length >= 3`
5. Check no other agent has active claim on same subsystem (for `requires_solo_agent: true` tasks)

## Blast Radius Validation (HARD GATE)
Call `galdr_validate_task()` before claiming. `valid=false` = STOP, escalate to human.

## Implementation
1. Read task file acceptance criteria fully
2. Implement minimally to meet acceptance criteria
3. No gold-plating — just make the criteria pass
4. Heartbeat commit every 15 minutes: `git commit -m "heartbeat(task-NNN): still active at {checkpoint}"`

## Evidence Generation
After implementation, create `.galdr/logs/taskNNN_evidence.log`:
```
=== TASK NNN VERIFICATION EVIDENCE ===
Date: {timestamp}
Implementer: sprint-agent-{id}

=== ACCEPTANCE CRITERIA CHECKLIST ===
[✅] Criterion 1: {what was done}

=== EVIDENCE ===
Type: test_output | runtime_log | compile_log
{actual output here}
```

## Completion (NOT [✅] — set awaiting-verification)
```yaml
status: awaiting-verification
evidence_of_completion:
  type: test_output
  path: ".galdr/logs/taskNNN_evidence.log"
```
TASKS.md: `[🔄]` → `[🔍]`

Commit: `git commit -m "impl(task-NNN): implementation complete, awaiting verification"`

## Failure Handling
On any failure:
1. Set `status: pending`, clear claim fields
2. Add to `failure_history: [{date, reason, notes}]`
3. If `failure_history.length >= 3`: set `status: failed`, TASKS.md → `[❌]`, add to CLEANUP_REPORT.md
