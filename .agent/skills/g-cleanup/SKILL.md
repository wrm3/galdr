---
name: g-cleanup
description: Nightly autonomous cleanup — sync TTL resets, health scoring, SPRINT.md generation, ACTIVE_BACKLOG.md regeneration, parity audit, and vault `_index.yaml` regeneration via vault-reindex.ps1.
---
# galdr-cleanup

## When to Use
@g-cleanup. Nightly maintenance. Runs all health checks and generates next day's sprint plan.

## Steps (Run in Order)

### 1. Git Pull
```bash
git pull
```

### 2. Task TTL Check
For each `in-progress` task:
- Is `now > claim_expires_at`? AND `last_heartbeat < claim_expires_at`?
- YES → reset: `status: pending`, clear claim fields, add `failure_history` entry with `reason: "TTL expired"`

### 3. Verification Timeout Check
For each `awaiting-verification` task:
- Has it been `[🔍]` for > 8 hours? → reset to `status: pending` with `reason: verification_timeout`
- > 4 hours? → flag in CLEANUP_REPORT.md

### 4. Platform Parity Audit
Compare file lists between `.cursor/rules/`, `.claude/rules/`, `.agent/rules/`:
- **First**: read `PARITY_EXCLUDES.md` (in this skill folder) for files to skip
- Files in one but not others (and NOT in the exclusion list) → report as parity violation

### 5. Project Health Score
```
score = (completed / total_non_cancelled) × 100
penalties: -5 per stale [🔄], -3 per [🔍] > 4h, -10 per failure_history > 2, -15 per empty subsystem
final = max(0, score - penalties)
```

### 6. SPRINT.md Generation
Select tasks for next sprint:
- `ai_safe: true`, `blast_radius: low|medium`
- No blockers (dependencies all completed)
- Sort by priority and goal alignment
- Include estimated story points and subsystem

### 7. ACTIVE_BACKLOG.md Regeneration
1. All non-completed/non-cancelled tasks
2. Grouped by subsystem
3. Recommended sprint order
4. Blocked tasks section
5. Human-required tasks section

### 8. Dependency Graph Regeneration
Regenerate `.galdr/DEPENDENCY_GRAPH.md` using the `g-dependency-graph` skill:
1. Read all task files, extract id/title/status/subsystem/priority/dependencies
2. Build adjacency list from dependencies
3. Compute critical path (longest dependency chain)
4. Identify top blockers, blocked tasks, and orphans
5. Generate Mermaid diagram with status-based styling
6. Write `.galdr/DEPENDENCY_GRAPH.md`

### 9. Vault Index Regeneration
Regenerate the vault `_index.yaml` so path listings and metadata stay in sync with note files on disk.

From the **project root** (where `.cursor/hooks/` exists), run:

```powershell
powershell -ExecutionPolicy Bypass -File .\.cursor\hooks\vault-reindex.ps1
```

On failure, note it in CLEANUP_REPORT.md under **Actions Required**.

### 10. Vault Freshness Check
Run the freshness audit from the `g-knowledge-refresh` skill (Steps 1-2 only):
1. Read `_index.yaml`, check `refresh_after` and `expires_after` dates
2. If stale or due-for-refresh notes found, add to CLEANUP_REPORT.md under **Vault Freshness**
3. Do NOT auto-refresh — only flag for human review in the report

### 11. Experiment Staleness Check
For each active experiment in `.galdr/experiments/EXPERIMENTS.md`:
- Read the EXP file
- If any stage is `[🔄]` and last modified >48h ago → flag in CLEANUP_REPORT.md
- If experiment `status: running` but no stage has been updated in >72h → mark as stale

### 12. CLEANUP_REPORT.md
```markdown
# Cleanup Report — YYYY-MM-DD

## Health Score
Score: N/100 (Healthy | Degraded | Critical)

## TTL Resets
- Task NNN: reset from in-progress (expired)

## Parity Violations
- .cursor/rules/XX_name.mdc: missing in .claude/rules/ and .agent/rules/

## Actions Required (Human Review)
- Task NNN: failure_history >= 3 — ralph_wiggum_loop
- Task NNN: ai_safe: false — needs human checkpoint

## AI Ideas (SELF_EVOLUTION proposals)
- [If any experiments proposed by sprint agents]
```
