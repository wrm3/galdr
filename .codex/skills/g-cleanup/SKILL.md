---
name: g-cleanup
description: Nightly autonomous cleanup — sync TTL resets, health scoring, SPRINT Planning (activate **g-tasks** SPRINT PLAN operation)

### 7.### 7. ACTIVE_BACKLOG.md Regeneration
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

### 9. CLEANUP_REPORT.md
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
