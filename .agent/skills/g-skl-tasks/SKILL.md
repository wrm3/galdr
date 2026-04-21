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

   **Cross-project dependency prompt** (interactive, before writing the file):
   - Ask: `"Does this task depend on a cross-project order? [order_id or 'skip']"`
   - If user supplies an `order_id` (e.g., `ord-abc123`):
     - Read `.galdr/linking/sent_orders/` and locate the matching record
     - If found: capture `sent_to` (project), `remote_task_title`, current `status`, current date as `last_synced` — populate the `cross_project_ref:` field below
     - Also append this new task's ID to that order record's `local_depends:` array
     - If not found: warn `"⚠️ No matching order in linking/sent_orders/ — proceeding without cross_project_ref"` and continue
   - If user says `skip` (or anything not matching `ord-*`): omit the `cross_project_ref:` field entirely

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
release_id: null              # optional: release ID this task is scheduled for (e.g. 3)
created_date: 'YYYY-MM-DD'
completed_date: ''
# Optional — only present when this task gates on a cross-project order:
cross_project_ref:
  - order_id: "ord-abc123"
    project: "child_project_id"
    remote_task_title: "Implement JWT auth endpoint"
    status: in-progress        # cached from last sync; updated by g-skl-pcac-read
    last_synced: "YYYY-MM-DD"
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
   - Derive tier badge from `subsystems:` list:
     - For each name in `subsystems:`, read `.galdr/subsystems/{name}.md` frontmatter `min_tier:` field
     - Badge = highest tier found: `slim` < `full` < `adv`
     - If no subsystems or no specs have `min_tier:` → default to `[slim]`
     - If `.galdr/release_profiles/` exists, use the configured tier names from profile `name:` fields
   - Add: `- [📋] **Task NNN**: Title `[{tier_badge}]` — brief acceptance summary`
   - If tier is `[slim]`, the badge may be omitted to reduce noise (display preference)

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

2a0. **Alignment Check (paused → pending unpause)**: When `from_status = paused` AND `to_status = pending`, run the ALIGNMENT CHECK sub-operation (see below) BEFORE writing the status change. If the check surfaces a prompt, block the status write until the user responds A/B/C.

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

2c. **When returning to `[📋]` / `pending` after a FAIL (g-go-review or agent rejection)**:
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

   **Release guard**: Before marking any task `[🔄]` (in-progress):
   - If the task has a `release_id:` field that is not null:
     - Read `.galdr/releases/release{NNN}_*.md` for that release ID
     - If release `status: released` → warn: `⚠️ Task {id} is assigned to already-released release {name}. Proceed? [y/n]`
     - If release not found → warn: `⚠️ release_id: {value} not found in .galdr/releases/. Proceeding without release guard.`
   - If `release_id: null` or absent → no guard needed

   **Broadcast completion ping** (if applicable):
   If the task has `delegation_type: broadcast` and `task_source` is set in its YAML frontmatter:
   - Prompt: "This task was received as a broadcast from [task_source]. Notify the source project of completion? [y/n] (default: y)"
   - If yes: invoke `g-skl-pcac-notify` with routing `--project [task_source_path]`, subject "Broadcast task completed: [title]", subtype `broadcast_completion`; include original task title and completion date in the detail
   - If no or source path unknown: skip silently — completion pings are always optional

   **Capability update check** (for [✅] completions):
   After marking a task complete, check if any subsystem in the task's `subsystems:` field maps to a capability in `.galdr/linking/capabilities.md`:
   - Read the task's `subsystems:` list
   - Read `.galdr/linking/capabilities.md` (if it exists)
   - If any subsystem name matches a capability `Name` column value:
     - Display: "📡 This task affected subsystem(s): [{subsystem_names}]. Check capabilities.md — should any status change?"
     - Show the current status of matching capabilities
     - Prompt: "Update capability status? [enter changes or press Enter to skip]"
     - If updated: write change to `capabilities.md` and optionally trigger `g-skl-pcac-notify --capability-update`
   - If no match or capabilities.md missing: skip silently

5. **Confirm**:
   ```
   ✅ Task NNN → {new_status}
   File YAML: updated | TASKS.md: updated | Sync: verified
   Release: {release name} (target: {date}) — {days} days away    ← if release_id is set
   ```

---

## Operation: ALIGNMENT CHECK (UPDATE STATUS sub-operation — unpause only)

Runs exclusively when UPDATE STATUS transitions a task from `paused` (`[⏸️]`) → `pending` (`[📋]`). Fast scan (~30 seconds). Surfaces stale references so the resumed task does not introduce drift. Never rewrites the task spec — only reports.

### 1. Gather inputs

From `.galdr/tasks/taskNNN_*.md`:
- `created_date` from YAML
- Most recent `paused` Status History row timestamp (if present) — use this as `paused_since`; else fall back to `created_date`
- `subsystems:` list
- Full task spec body text (for reference scanning)

### 2. Compute age and escalation

```
age_days = today - paused_since
  < 7d   → advisory mode (no prompt, note in history only)
  7–30d  → prompt user IF any stale finding
  > 30d  → always prompt user with full report (even if clean)
```

### 3. Gather "since pause" context

In order:
1. `git log --oneline --since={paused_since}` — list recent commits
2. `.galdr/TASKS.md` — collect `[✅]` entries whose task file `subsystems:` overlaps this task's `subsystems:`
3. `.galdr/DECISIONS.md` — collect decision entries with timestamp > `paused_since`

### 4. Scan the spec for stale references

For each reference kind:

| Reference pattern | Check |
|---|---|
| `g-skl-*` (skill name) | Folder `.cursor/skills/{name}/` exists? |
| `@g-*` or `g-*` (command name) | File `.cursor/commands/{name}.md` exists? |
| Path literals | Path still exists on disk, OR has a well-known rename (see table below) |
| Subsystem names | Appears in SUBSYSTEMS.md registry? |

A reference is **stale** when:
- Skill/command folder/file is missing, AND the well-known renames table has a mapping, OR
- Path matches the Old column of the well-known renames table, OR
- Subsystem name is not found in SUBSYSTEMS.md

### 5. Well-known renames table (inline — extend as renames happen)

| Old | New | Source |
|-----|-----|--------|
| g-skl-harvest | g-skl-res-review | T121 (2026-04-18) |
| g-skl-harvest-intake | g-skl-res-apply | T121 |
| g-skl-reverse-spec | g-skl-res-deep | T121 |
| g-skl-ingest-docs | g-skl-recon-docs | T121 |
| g-skl-ingest-url | g-skl-recon-url | T121 |
| g-skl-ingest-youtube | g-skl-recon-yt | T121 |
| `research/harvests/` | `research/recon/` | T121 intent |
| `prds/` | `features/` | T040 / T084-1 |
| `topics:` (frontmatter) | `tags:` (frontmatter) | T039 |

Agents SHOULD append new mappings here when a rename lands (keep this table canonical; no external config file).

### 6. Outcomes

**Clean case (no stale references found)**:
- Proceed with unpause silently
- Append to Status History:
  ```
  | YYYY-MM-DD | paused | pending | Unpaused; alignment check: clean |
  ```

**Advisory case (age < 7d, stale found)**:
- Proceed with unpause — do NOT block
- Append to Status History:
  ```
  | YYYY-MM-DD | paused | pending | Unpaused; alignment check advisory: {count} stale refs noted |
  ```

**Prompt case (age ≥ 7d AND stale found) OR (age > 30d always)**:
- Output the structured report (format below)
- Block the status write until user responds A/B/C
- On response:
  - `A` → route user to spec edit workflow; do NOT write the status change; leave task `[⏸️]` until user re-issues the unpause with an updated spec
  - `B` → proceed with unpause; append Status History row including the stale-ref summary
  - `C` → cancel; task stays `[⏸️]`; no Status History row written

### 7. Report format

```
⚠️ Alignment Check — Task {id}: {title}
Paused: {paused_since}  |  Age: {N} days

Stale References:
- {kind} "{old}" → now "{new}" ({rename source, e.g. T121, 2026-04-18})
- {kind} "{old}" → MISSING ({no mapping found — manual review})

Related work since pause:
- {task-id} [{status}] {title} ({date})
- {decision-id} [Decision] {decision summary}

Recommendation: {Spec refresh recommended | Proceed with caution | Cancel recommended}

Select: (A) Update spec now  (B) Proceed anyway  (C) Cancel unpause
```

### 8. Idempotency

Cache the alignment scan result keyed on `{task_id, spec_hash}` (spec_hash = hash of the task file body) within the current session to avoid re-scanning if the same task is unpaused twice without edits. Cache does not persist across sessions — first unpause of a session always scans fresh.

### 9. Acceptance criteria coverage

This sub-operation satisfies Task 150 AC-1 through AC-6. AC-7 (propagation to 10 IDE targets) and AC-8 (`g-task-upd` description update) are handled at the skill-deployment level.

---

## Operation: TIER BADGE DERIVATION

Used by CREATE TASK and STATUS display to determine the minimum galdr tier required for a task.

### Algorithm

1. Read the task's `subsystems:` list from YAML frontmatter
2. For each subsystem name, read `.galdr/subsystems/{name}.md`:
   - Extract `min_tier:` from YAML frontmatter
   - If spec file missing or `min_tier:` absent → treat as `slim` (default)
3. Badge = highest tier across all subsystems: `slim` < `full` < `adv`
4. If `.galdr/release_profiles/` exists: validate badge against configured tier names (profile `name:` fields)
5. Return the badge as a display string: `[slim]`, `[full]`, or `[adv]`

### Display Format

```
- [📋] **Task 082** `[full]` Product Tier Architecture — parent task...
- [📋] **Task 007** `[slim]` PCAC topology foundation...
```

The badge is **omitted for slim** in most contexts to reduce visual noise. It appears when:
- The task is explicitly `full` or `adv`
- A release gate check is running (all tasks shown with badges)
- User invokes `@g-task-upd NNN --show-tier`

### SYNC-CHECK Behavior

SYNC-CHECK does **NOT** flag missing tier badges as errors. Badges are derived at display time — they are not stored in task YAML. This section is informational only.

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

---

## Cross-Project Split Check (T119)

When **CREATE TASK** is invoked (step 3, before writing the file), perform a topology split check:

### Split Check Algorithm

```
1. Load topology (if available):
   - Read .galdr/linking/link_topology.md → get children[], parent, siblings[]
   - For each peer: read .galdr/linking/peers/{slug}_capabilities.md (if exists)

2. Extract domain tags from task title + description:
   - Match against capability domain keywords (e.g. "frontend", "backend", "api", 
     "database", "mobile", "ML", "docker", "UI", "auth", "real-time", "infra")

3. For each domain tag: check if a peer owns it (capability name match)

4. If ANY domain tag belongs to a peer that is NOT the current project:
   → Surface split suggestion (see format below)

5. If ANY domain tag has NO owner in topology at all:
   → Surface spawn suggestion
```

### Split Suggestion Format

```
⚡ TOPOLOGY CHECK: This task touches domains that may belong elsewhere:

  Domain "frontend" → galdr_frontend owns this capability
  Domain "mobile" → no project owns this — consider spawning

Options:
  [1] Keep entire task here (this-project only)
  [2] Split: create local task (backend slice) + PCAC order to galdr_frontend (frontend slice)
  [3] Split + spawn: create local + PCAC order + spawn new project for "mobile"
  [s] Skip topology check

Choice [1/2/3/s]:
```

### On Split Confirmed (Option 2 or 3)

1. **Create local task** — description scoped to this-project's domain slice
2. **For each remote domain**: invoke `g-skl-pcac-order` to create a PCAC order to the target project with:
   - `remote_task_title`: full original task title
   - `description`: the remote slice
   - `cross_project_ref`: `{domain}-{task_slug}` (shared canonical name across all participating projects)
3. **Add `cross_project_ref:` field** to the local task YAML:
   ```yaml
   cross_project_ref:
     slug: "{domain}-{task_slug}"      # shared logical feature name
     participating_projects:
       - "{this_project_slug}"
       - "{remote_project_slug}"
     peer_order_ids: ["ord-{id}"]      # order IDs sent to each peer
   ```
4. Print summary:
   ```
   ✅ Split complete:
   → this-project: task{NNN} (backend slice)
   → galdr_frontend: PCAC order ord-{id} sent (frontend slice)
   cross_project_ref: "auth-unified-login"
   ```

### On Spawn Confirmed (Option 3 with new capability)

1. Immediately after split write: invoke `g-pcac-spawn` with:
   - `--description`: "{capability} capability extracted from task {original_title}"
   - `--capabilities`: [the capability domain]
   - `--parent` or `--sibling` (let user choose)
2. After spawn completes: send the spawn's slice as a PCAC order to the newly created project

### Skip / No Topology

- If `.galdr/linking/link_topology.md` does not exist or is empty → skip check silently
- If topology exists but no peers own conflicting domains → skip check silently
- User can always choose option `[s]` to skip without penalty
