# @g-sprint — Autonomous Sprint Agent

**Purpose**: Run a 2-hour autonomous work sprint on the current project.
Agents claim tasks, implement them, and submit for verification.
No human needed at the keyboard — tasks MUST be ai_safe: true.

---

## Pre-Sprint Checklist (MANDATORY — do before claiming anything)

1. **Pull latest**: `git pull` — never work on stale state
2. **Read SPRINT.md** — confirm it is < 2h old. If stale, stop and run `@g-cleanup` first
3. **Read CONSTRAINTS.md** — load all active constraints into context
4. **Check your agent identity**: set `AGENT_ID = "{ide}-sprint-{session-hash-6chars}"`
5. **Read git log** — `git log --oneline -20` to understand recent changes

If any check fails, STOP and report the issue.

---

## Task Selection (from SPRINT.md only)

1. Read SPRINT.md — tasks in the Active Sprint Tasks table are pre-filtered as eligible
2. Pick the FIRST unclaimed task you can handle (highest priority, unblocked)
3. Verify task file exists: `.galdr/tasks/task{ID}_*.md`
4. Verify `ai_safe: true` in task YAML — if false, SKIP it
5. Verify `blast_radius` is NOT `high` or `critical` — if it is, SKIP it
6. If `requires_solo_agent: true` — verify you are the only active agent by checking git log for other claims in last 30 minutes

---

## Atomic Task Claim Protocol

**Step 1**: Read task file, verify it is still `status: pending` (not claimed by another agent)
```bash
git pull  # CRITICAL: pull first to detect concurrent claims
```

**Step 2**: Update task YAML immediately:
```yaml
status: in-progress
claimed_by: {your_agent_id}
claimed_at: {ISO-8601 timestamp}
claim_ttl_minutes: {estimated_duration * 1.5}
claim_expires_at: {claimed_at + claim_ttl_minutes}
last_heartbeat: {same as claimed_at}
```

**Step 3**: Commit the claim BEFORE writing any code:
```bash
git add .galdr/tasks/task{ID}_*.md
git commit -m "claim(task-{ID}): {agent_id} starting work"
git push
```

**Step 4**: If `git push` fails (conflict) — another agent claimed first. Reset your changes, pick next task.

---

## Pre-Implementation

Before writing code:

1. **Pre-mortem** (1-2 min): What could go wrong? What is the riskiest assumption?
   - Write your pre-mortem in the task file under `## Pre-Mortem` section
   - Commit: `git commit -m "spec(task-{ID}): pre-mortem complete"`

2. **Memory query** (if memory MCP available):
   ```
   memory_context(project_id="{project_id}", subsystems=["{subsystem}"], budget_tokens=500)
   ```
   Review: recent completions, failures, lessons learned for this subsystem

3. **Spec freshness check**: Is the task spec still accurate given recent git history?
   - If spec is stale and `allow_spec_update: true` → update spec, commit with `spec(task-{ID}):` prefix
   - If spec is stale and `allow_spec_update: false` → set `status: failed`, `failure_reason: spec_outdated`

---

## Implementation

Write code to satisfy acceptance criteria.

### During implementation:
- **Checkpoint every 20 min** — update `execution_progress` in task YAML and commit:
  ```bash
  git add .galdr/tasks/task{ID}_*.md {modified_code_files}
  git commit -m "wip(task-{ID}): {what was done}, {percent}% complete"
  git push
  ```
- **Heartbeat** — update `last_heartbeat` in task YAML every 30 min to prevent TTL expiry
- **Blast radius check** — if you realize you are touching more files than `affected_files_estimate`, PAUSE and assess

### If stuck (cannot proceed):
1. Try a different approach (attempt 1)
2. Revert and try yet another approach (attempt 2)
3. On 3rd failure — **Ralph Wiggum Rule**: STOP. Set `status: failed`, `failure_reason: approach_wrong`, document all 3 attempts in `failure_history`. DO NOT loop.

---

## Task Completion (Implementer Role)

When acceptance criteria are all satisfied:

1. **Fill evidence_of_completion** in task YAML:
   ```yaml
   evidence_of_completion:
     provided_by: {agent_id}
     provided_at: {timestamp}
     evidence_items:
       - type: file_exists
         description: "{filename} created"
         value: "{path}"
       - type: test_output
         description: "{what was tested}"
         value: "{output snippet}"
   verification_commands:
     - {command to independently verify}
   ```

2. **Set status to awaiting_verification**:
   ```yaml
   status: awaiting_verification
   claimed_by: null   # Release claim — verifier will take over
   ```

3. **Update TASKS.md**: change `[🔄]` to `[🔍]`

4. **Commit all changes**:
   ```bash
   git add .
   git commit -m "feat(task-{ID}): {task_title} — implementation complete, awaiting verification

   Task: #{ID}
   Subsystem: {subsystem}
   Evidence: {1-line summary}

   Agent: {agent_id}
   Model: {model_name}
   Cost: ~${estimated_cost}"
   git push
   ```

5. **STOP**: Do NOT mark `[✅]`. A different agent must verify.

---

## Multi-Task Sprint

After completing a task (submitting for verification), pick the next eligible task from SPRINT.md and repeat.

**Sprint ends when**:
- 2 hours have elapsed from sprint start
- SPRINT.md has no more eligible unclaimed tasks
- Rate limit approaching (>85%)
- A `requires_solo_agent` task is the only option and another agent may be active

---

## Sprint Exit (Clean Shutdown)

Before ending the session, emit a sprint summary:

```
## Sprint Summary — {agent_id} — {date}

Tasks submitted for verification:
- Task {ID}: {title} — [🔍] awaiting verification

Tasks attempted but failed:
- Task {ID}: {title} — [❌] {failure_reason}

Tasks skipped (reason):
- Task {ID}: {reason for skip}

Total commits: {n}
Estimated cost: ~${n}
Git status: all changes pushed

Handoff note: {anything the next agent should know}
```

---

## SPRINT AGENT MUST NOT

- Mark any task `[✅]` — verification requires a different agent
- Modify tasks not in SPRINT.md without explicit user instruction
- Work on tasks with `ai_safe: false`
- Run destructive operations (schema changes, file deletes) without `requires_solo_agent: true` confirmed
- Modify CONSTRAINTS.md
- Push directly to main/master without going through the standard commit workflow
- Continue past 3 failures on the same task (Ralph Wiggum Rule)
