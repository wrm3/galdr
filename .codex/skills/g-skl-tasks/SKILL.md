---
name: g-skl-tasks
description: Own and manage all task data — TASKS.md index, tasks/ individual files, status transitions, sync validation, complexity scoring, and sprint planning. Single source of truth for everything task-related.
---
# g-tasks

**Files Owned**: `.galdr/TASKS.md`, `.galdr/tasks/taskNNN_*.md`

**Activate for**: create task, update task status, sync check, complexity score, sprint plan, task dependencies, "phantom" or "orphan" issues.

---

## Operation: CREATE TASK

1. **Determine next ID**: read `TASKS.md`, find highest task ID across ALL sections → next = highest + 1

2. **Score complexity** (1-10+):
   ```
   Estimated effort > 2-3 days          +4
   Affects multiple subsystems           +3
   Changes across unrelated modules      +3
   Requirements unclear/uncertain        +2
   Multiple distinct verifiable outcomes +2
   Blocks many subsequent tasks          +2
   Long acceptance criteria              +1
   ```
   Score ≥7: STOP — expand to sub-tasks first (see EXPAND below)

3. **Create task file** at `.galdr/tasks/taskNNN_descriptive_name.md`:
```yaml
---
id: NNN
title: 'Task Title'
type: feature | bug_fix | refactor | documentation
status: pending
priority: critical | high | medium | low
prd: null
subsystems: [component1, component2]
project_context: 'Why this task matters to project goals'
dependencies: []
blast_radius: low | medium | high
requires_verification: false
ai_safe: true
created_date: 'YYYY-MM-DD'
completed_date: ''
---

# Task NNN: [Title]

## Objective
[Clear, actionable goal — done when this is complete]

## Acceptance Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]

## Implementation Notes
[Technical approach, constraints, dependencies]

## Verification
- [ ] No lint errors
- [ ] Acceptance criteria tested
- [ ] Docs updated if needed
```

4. **Add to TASKS.md** (atomic — same response):
   - Find the subsystem section (or create one)
   - Add: `- [📋] **Task NNN**: Title — brief acceptance summary`

5. **Confirm**:
   ```
   ✅ Task NNN created
   File: .galdr/tasks/taskNNN_name.md
   TASKS.md: [📋] added under Subsystem: {name}
   ```

---

## Operation: UPDATE STATUS

**Status transitions**:
```
[ ] → [📋] → [🔄] → [🔍] → [✅]
              ↓       ↓
             [⏸️]    [❌] (verification failed → reset to [📋])
```

1. **Read both**: `.galdr/tasks/taskNNN_*.md` YAML and TASKS.md indicator — fix mismatch first (file is source of truth)

2. **Apply transition**:

| Action | File YAML | TASKS.md |
|---|---|---|
| Start working | `status: in-progress` | `[🔄]` |
| Submit for verification | `status: awaiting-verification` | `[🔍]` |
| Mark complete (verifier) | `status: completed` | `[✅]` |
| Pause | `status: paused` | `[⏸️]` |
| Fail/cancel | `status: failed` | `[❌]` |

3. **For in-progress** — also set:
```yaml
claimed_by: "{agent_id}"
claimed_at: "YYYY-MM-DDTHH:MM:SSZ"
claim_ttl_minutes: {estimated * 1.5}
claim_expires_at: "YYYY-MM-DDTHH:MM:SSZ"
```

4. **For completed** — also set `completed_date: "YYYY-MM-DD"` and update subsystem Activity Logs (see g-subsystems)

5. **Confirm**:
   ```
   ✅ Task NNN → {new_status}
   File YAML: updated | TASKS.md: updated | Sync: verified
   ```

---

## Operation: SYNC CHECK

Run at session start or when phantom/orphan issues suspected.

1. **Read TASKS.md** — extract all task entries with indicators
2. **List** `.galdr/tasks/task*.md`
3. **For each TASKS.md entry**:
   ```
   [✅][❌][⏸️] → look in tasks/
   [📋][🔄][🔍] → look in tasks/ only
   [ ]           → no file expected (OK)

   ✅ FOUND   = file exists
   ⚠️ PHANTOM = in TASKS.md but no file
   ```
4. **For each task file** — has matching TASKS.md entry? NO → ORPHAN ⚠️
5. **Status mismatch** — file is source of truth, fix TASKS.md
6. **Report**:
   ```
   📋 TASK SYNC
   Task 001: ✅ FOUND — pending/[📋] match
   Task 003: ⚠️ PHANTOM — in TASKS.md but no file
   Task 099: ⚠️ ORPHAN — file exists, not in TASKS.md
   Synced: 12/13 | Fixed: 0 | Needs action: 1
   ```

---

## Operation: EXPAND (complex tasks)

When complexity score ≥7:
1. Identify logical sub-goals
2. If shared module needed → sub-task 1 = extraction
3. Create sub-task files: `task{parent}-1_name.md`, `task{parent}-2_name.md`
4. Update parent task: `sub_tasks: ["42-1", "42-2"]`
5. Add sub-tasks to TASKS.md under same subsystem section

---

## Operation: SPRINT PLAN

1. Read all `[📋]` tasks from TASKS.md
2. Score each: priority + dependencies resolved + blast_radius + goal alignment
3. Output:
   ```
   ## Proposed Sprint
   1. Task 5 — DB Schema (3 SP, no blockers)
   2. Task 6 — API Layer (5 SP, needs Task 5)
   3. Task 7 — Fix lint (1 SP, independent)
   Target: 70% capacity | Grouped by subsystem
   ```

---

## Status Indicators Reference

| Indicator | File YAML | Meaning |
|---|---|---|
| `[ ]` | (no file) | Pending — file not yet created |
| `[📋]` | `pending` | File created, ready to start |
| `[🔄]` | `in-progress` | Being worked on |
| `[🔍]` | `awaiting-verification` | Done, needs different-agent review |
| `[✅]` | `completed` | Verified complete |
| `[❌]` | `failed` | Failed or cancelled |
| `[⏸️]` | `paused` | Paused |
