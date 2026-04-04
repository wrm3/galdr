---
name: g-cleanup
description: Nightly autonomous cleanup — TTL resets, verification timeouts, platform parity audit, health scoring, sprint planning, backlog regeneration, and dependency graph update.
---
# g-cleanup

**Activate for**: nightly maintenance, `@g-cleanup`, health check, sprint plan generation.

**Does NOT**: modify version in `.identity` (use `g-upgrade`), create/delete task files (use `g-tasks`), write PRDs (use `g-plan`).

---

## Steps (Run in Order)

### 1. Git Pull
```bash
git pull
```

### 2. Task TTL Check
For each `in-progress` task file in `.galdr/tasks/`:
- Is `now > claim_expires_at` AND `last_heartbeat < claim_expires_at`?
- YES → reset: `status: pending`, clear `claimed_by/claimed_at/claim_expires_at`, append `failure_history` entry with `reason: "TTL expired"`
- Update TASKS.md indicator from `[🔄]` to `[📋]`

### 3. Verification Timeout Check
For each `awaiting-verification` task:
- `> 8 hours` in `[🔍]` → reset to `status: pending`, `[📋]`, reason: `verification_timeout`
- `> 4 hours` → flag in CLEANUP_REPORT.md only (do not reset)

### 4. Platform Parity Audit
Compare file lists between `.cursor/rules/`, `.claude/rules/`, `.agent/rules/`:
- **First**: read `PARITY_EXCLUDES.md` (in this skill's folder) for intentionally excluded files
- Files missing from one or more targets (and NOT in exclusion list) → report as parity violation

### 5. Project Health Score
```
base  = (completed / total_non_cancelled) × 100
penalties:
  -5  per stale [🔄] (TTL expired but not yet reset)
  -3  per [🔍] > 4h
  -10 per task with failure_history length > 2
  -15 per subsystem in SUBSYSTEMS.md with no tasks ever
final = max(0, base − penalties)

Healthy: ≥80 | Degraded: 50-79 | Critical: <50
```

### 6. Sprint Planning
Activate **g-tasks → SPRINT PLAN operation** to generate next sprint recommendation.
Write result to `.galdr/config/SPRINT.md` if that file exists (galdr_full only — skip silently in slim).

### 7. ACTIVE_BACKLOG.md Regeneration
Write `.galdr/ACTIVE_BACKLOG.md`:
1. All non-completed/non-cancelled tasks, grouped by subsystem
2. Recommended sprint order (priority + no unresolved blockers first)
3. Blocked tasks section (list what each is waiting on)
4. Human-required tasks section (`ai_safe: false` or `requires_verification: true`)

### 8. Dependency Graph Regeneration
Activate **g-dependency-graph** skill:
1. Read all task files — extract `id, title, status, subsystem, priority, dependencies`
2. Build adjacency list
3. Compute critical path (longest dependency chain)
4. Identify top blockers, blocked tasks, orphans
5. Generate Mermaid diagram with status-based styling
6. Write `.galdr/DEPENDENCY_GRAPH.md`

### 9. CLEANUP_REPORT.md
Write `.galdr/reports/CLEANUP_REPORT.md`:
```markdown
# Cleanup Report — YYYY-MM-DD HH:MM

## Health Score
Score: N/100 (Healthy | Degraded | Critical)

## TTL Resets
- Task NNN: reset from in-progress (expired at {timestamp})

## Verification Timeouts
- Task NNN: [🔍] for > 8h — reset to pending

## Parity Violations
- .cursor/rules/XX_name.mdc: missing in .claude/rules/

## Actions Required (Human Review)
- Task NNN: failure_history ≥ 3 — needs manual intervention
- Task NNN: ai_safe: false — needs human checkpoint

## Sprint Plan
[output from g-tasks SPRINT PLAN]
```
