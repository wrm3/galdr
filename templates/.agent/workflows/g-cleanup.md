# @g-cleanup — Midnight Cleanup Agent

**Purpose**: Nightly housekeeping agent. Runs unattended at midnight (or on-demand).
Validates state, expires stale claims, generates SPRINT.md, produces CLEANUP_REPORT.md.

**Safe to run**: Yes — cleanup is read-mostly. The only writes are task YAML resets for expired TTLs and SPRINT.md/CLEANUP_REPORT.md regeneration.

---

## Pre-Cleanup (MANDATORY)

```bash
git pull   # Always work from latest state
```

Read:
1. `.galdr/PROJECT_CONTEXT.md` — load project identity and constraints reference
2. `.galdr/ARCHITECTURE_CONSTRAINTS.md` — load active constraints
3. `.galdr/TASKS.md` — master task list
4. All files in `.galdr/tasks/` — individual task states

---

## Step 1: Task Sync Audit

Compare TASKS.md entries against `.galdr/tasks/` files:

**Orphan detection** — files in `tasks/` not referenced in TASKS.md:
- Report each orphan. If clearly abandoned (>30 days, status: failed), ask human via CLEANUP_REPORT.

**Phantom detection** — TASKS.md entries with `[📋]` or higher but no file:
- Auto-reset to `[ ]` in TASKS.md and log.

**Status mismatch** — TASKS.md indicator vs task file YAML `status` disagree:
- TASK FILE IS SOURCE OF TRUTH. Update TASKS.md to match task file. Log the fix.

---

## Step 2: Expired Claim Recovery (TTL)

For every task with `status: in-progress` or `status: speccing`:
1. Read `claimed_at` and `claim_ttl_minutes`
2. If `now > claim_expires_at` AND `last_heartbeat` is also past TTL → claim is stale
3. Reset the task:
   ```yaml
   status: pending
   claimed_by: null
   claimed_at: null
   claim_expires_at: null
   last_heartbeat: null
   ```
4. Update TASKS.md: `[🔄]` → `[📋]` (or `[📝]` → `[📋]`)
5. Add to `failure_history`:
   ```yaml
   - attempt: {n+1}
     failed_at: "{now}"
     agent_id: "{previous_claimed_by}"
     reason: "TTL expired — claim abandoned without completion or heartbeat"
     error_snippet: null
     resolution_tried: "N/A"
     escalated: false
   ```
6. Commit each reset: `git commit -m "ttl-reset(task-{id}): claim expired, returned to pending"`

---

## Step 3: Stale Spec Detection

For every task with `status: pending` or `status: in-progress`:
1. Check `spec_last_verified` — if > 30 days ago, mark for CLEANUP_REPORT
2. If `allow_spec_update: false` AND spec is > 30 days old → flag as high-risk, note in report
3. Do NOT auto-modify specs — just report

---

## Step 4: Resource Gate Review

For every task with `status: resource_gated` (`[⏳]`):
1. Note what resource it's waiting on (from task YAML `resource_requirements`)
2. Check if the resource might now be available (e.g., date-based gates)
3. Cannot auto-resolve resource gates — report for human review
4. If gated for > 14 days with no update, escalate in CLEANUP_REPORT

---

## Step 5: Health Score Calculation

For each subsystem listed in SUBSYSTEMS.md:
```
score = (completed / total_non_cancelled) * 100

penalties:
  - for each [🔄] past TTL: -5
  - for each [🔍] > 4 hours old: -3
  - for each task with failure_history.length > 2: -10
  - if subsystem has 0 completed tasks: -15

final_score = max(0, score - penalties)
```

Overall project health = weighted average of subsystem scores.

Classify: 80-100 = healthy (🟢), 50-79 = degraded (🟡), < 50 = critical (🔴)

---

## Step 6: SPRINT.md Generation

Build the next sprint queue (see task 045 rules for full algorithm). Summary:

**Eligibility filter** (task must pass ALL):
- `status: pending` (has task file, not claimed)
- `ai_safe: true`
- `blast_radius` is `low` or `medium`
- All dependencies in `[✅]`
- Not resource-gated
- No active claim (claimed_by is null)

**Ranking** (sort eligible tasks):
1. Priority (critical > high > medium > low)
2. Is this task blocking other tasks? (blockers first)
3. Age (older tasks first — prevents starvation)
4. Blast radius (low before medium)
5. Estimated effort (smaller first if tie)

**Solo task handling**: If `requires_solo_agent: true` tasks appear, add them to SPRINT.md
but mark them as `solo` — sprint agent must verify no other agent is active before claiming.

**Write SPRINT.md** using the template at `.galdr/SPRINT.md`.

---

## Step 7: Platform Parity Check

Compare rule files across `.cursor/rules/`, `.claude/rules/`, `.agent/rules/`:
1. List files in each directory (normalize extension)
2. Report any file present in one but missing from others
3. Cannot auto-fix content — report violations for human action

---

## Step 8: Dependency Graph Update

Generate `.galdr/DEPENDENCY_GRAPH.md`:
1. Read all task files, collect `dependencies` field
2. Build adjacency list
3. Identify critical path (longest dependency chain to completion)
4. Generate Mermaid diagram
5. Identify blockers (tasks blocking the most other tasks)

---

## Step 9: Cost Aggregation

For all tasks with `execution_cost.total_cost_usd` set:
1. Aggregate by subsystem
2. Compute project running total
3. Add to CLEANUP_REPORT.md cost summary

---

## Step 10: CLEANUP_REPORT.md Generation

Write the complete report to `.galdr/CLEANUP_REPORT.md` using the template.

---

## Step 11: Commit Everything

```bash
git add .galdr/
git commit -m "cleanup(nightly): {date} — {n} TTL resets, {n} sync fixes, SPRINT.md updated

Health: {score}/100 ({status})
Sprint tasks: {n} queued
Expired claims: {n} reset
Platform parity: {status}

Agent: {agent_id}
Rules-Version: {rules_version}"
git push
```

---

## CLEANUP AGENT MUST NOT

- Modify task acceptance criteria or implementation notes
- Add or remove tasks from TASKS.md (except fixing phantom entries)
- Change architecture constraints
- Promote AI ideas to tasks
- Mark any task as `[✅]` — completion requires verification
- Run destructive operations (file deletes) without logging to CLEANUP_REPORT first
- Continue if `git pull` returns conflicts — report and stop
