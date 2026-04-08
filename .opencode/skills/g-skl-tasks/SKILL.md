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

## Status History

| Timestamp | From | To | Message |
|-----------|------|----|---------|
| YYYY-MM-DD | — | pending | Task created |
```

4. **Subsystem guard** (subsystem integrity check — do before TASKS.md):
   - For each name in the task's `subsystems:` field:
     - Read `.galdr/SUBSYSTEMS.md` — is the name listed?
     - **If NOT listed**: create a stub spec at `.galdr/subsystems/{name}.md` using the CREATE SUBSYSTEM SPEC template from `g-skl-subsystems`, set `status: planned`. Add a `planned` entry row to SUBSYSTEMS.md index. This keeps the registry in sync from the moment the task is specced.
     - **If listed as `planned`**: no action — it's already tracked.
     - **If listed as `active`**: no action — read its spec before modifying.
   - ⚠️ Never leave a task referencing a subsystem that has no SUBSYSTEMS.md entry.

5. **Add to TASKS.md** (atomic — same response):
   - Find the subsystem section (or create one)
   - Add: `- [📋] **Task NNN**: Title — brief acceptance summary`

6. **Confirm**:
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

2a. **Before → `[🔍]` (AC gate)**: Walk every `- [ ]` acceptance criterion in the task file.
   - Each criterion confirmed met in actual files/code? → proceed to mark `[🔍]`
   - Any unmet → **do not mark `[🔍]`**; resolve the gap or log as a Blocker
   - Partial work is not `[🔍]`-eligible; task stays `[🔄]` until all ACs pass
   - **Stub/TODO scan**: search files modified for this task for bare stubs without `[TASK-X→TASK-Y]` annotation (`# TODO`, `pass`, `raise NotImplementedError`, etc.) — each unannotated stub is an unmet criterion; annotate per `g-rl-34` before marking `[🔍]`
   - **Bug-discovery gate**: any pre-existing bug encountered must have a `BUG[BUG-{id}]` comment and a `.galdr/bugs/` entry before `[🔍]`; bugs introduced by this task must be fixed inline (see `g-rl-35`)
   - **Status History append** (REQUIRED before `[🔍]`): append a row to `## Status History` at the bottom of the task file:
     ```
     | YYYY-MM-DD | {previous_status} | awaiting-verification | Implementation complete; {brief summary of what was done} |
     ```

2b. **Before → `[✅]` (docs check)**: After all ACs verified, check user-facing impact:
   - Does this task add/remove/change user-facing behavior? (skills, commands, agents, hooks, rules, conventions)
   - **YES** → append entry to `CHANGELOG.md` under `[Unreleased]`; update `README.md` if a relevant section exists
   - **NO** (internal refactor, task housekeeping, bug fix with no interface change) → skip
   - See `g-rl-26-readme-changelog.mdc` for qualifying criteria and format

2c. **When returning to `[📋]` / `pending` after a FAIL (g-go-verify or agent rejection)**:
   - **Status History append is REQUIRED** — message must name the specific failing ACs:
     ```
     | YYYY-MM-DD | awaiting-verification | pending | FAIL: {AC-NNN, AC-NNN} not met — {brief reason} |
     ```
   - Message must not be empty; "FAIL" alone is not acceptable
   - **🚨 STUCK LOOP CHECK** — before writing `[📋]`, count `FAIL:` rows in the Status History:
     ```
     Count all rows where the Message column contains "FAIL:"
     If count ≥ 3 → mark [🚨] (requires-user-attention) instead of [📋]
     ```
     When marking `[🚨]`, append a `## [🚨] Requires User Attention` block to the task file (see template below) and log in the session summary. **Agents must NEVER autonomously reset `[🚨]` back to `[📋]` — only a human can do this.**

3. **For in-progress** — also set:
```yaml
claimed_by: "{agent_id}"
claimed_at: "YYYY-MM-DDTHH:MM:SSZ"
claim_ttl_minutes: {estimated * 1.5}
claim_expires_at: "YYYY-MM-DDTHH:MM:SSZ"
```

4. **For completed** — also set `completed_date: "YYYY-MM-DD"` and update subsystem Activity Logs (see g-subsystems)

   **Broadcast completion ping** (if applicable):
   If the task has `delegation_type: broadcast` and `task_source` is set in its YAML frontmatter:
   - Prompt: "This task was received as a broadcast from [task_source]. Notify the source project of completion? [y/n] (default: y)"
   - If yes: invoke `g-skl-pcac-notify` with routing `--project [task_source_path]`, subject "Broadcast task completed: [title]", subtype `broadcast_completion`; include original task title and completion date in the detail
   - If no or source path unknown: skip silently — completion pings are always optional

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
| `[🚨]` | `requires-user-attention` | Stuck ≥3 FAIL cycles — **agents must not retry; human-only resolution** |

### [🚨] Stuck Note Template

When triggering `[🚨]`, append this block to the task/bug file:

```markdown
## [🚨] Requires User Attention

This item has failed verification **{N} times**. Automated agents will not retry it.

**Last failure reason**: {last FAIL row message}

**Human actions available**:
- Revise acceptance criteria → add "Human reset: AC revised" to Status History → reset to `[📋]`
- Split into simpler sub-tasks → mark this `[❌]`
- Cancel → mark `[❌]` with reason
- Override as complete → mark `[✅]` with manual sign-off note
```
