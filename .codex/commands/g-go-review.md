Verification-only backlog review: $ARGUMENTS

## Mode: REVIEW ONLY

> ⚠️  **Run this in a NEW agent session** — different window, different invocation.
> If you implemented any of these tasks in this session, **skip them** (leave `[🔍]`).
> Self-review defeats the purpose of this gate.

---

## Execution Protocol

### 1. Load Context

Read in this order:
- `.galdr/TASKS.md` — identify all `[🔍]` (Awaiting Review) tasks
- Individual task files for each `[🔍]` item — read acceptance criteria
- `git log --oneline -10` — understand what was recently implemented
- `.galdr/CONSTRAINTS.md` — guardrails

### 2. Build the Review Queue

Collect all tasks/bugs with status `[🔍]`.  
If `$ARGUMENTS` specifies IDs (e.g. `@g-go-review tasks 14 15`), review only those.

**Skip any item you implemented in this session.** Leave it `[🔍]` for a future agent.

### 3. Review Each Item

For each `[🔍]` task:

**a) Read task spec** — list all acceptance criteria  
**b) Check each criterion against actual files/code**  
**c) Score PASS or FAIL per criterion**  
**d) Bug check during review** — if you encounter a bug not covered by the task's ACs:
  - Determine: introduced by this task? → flag as unmet criterion → task FAIL
  - Pre-existing? → log BUG entry via `g-skl-bugs`, add `BUG[BUG-{id}]` comment, note in session summary — does NOT fail this task (see `g-rl-35`)  
**e) Overall result:**
  - All criteria PASS → mark `[✅]` + append verification note to task file + **run docs check (step 3f)**
  - Any criterion FAIL → **before changing status**:
    1. Append a row to `## Status History` at the bottom of the task file (add section if missing):
       ```
       | YYYY-MM-DD | awaiting-verification | pending | FAIL: {AC-NNN, AC-NNN} not met — {brief reason} |
       ```
    2. **🚨 STUCK LOOP CHECK** — count all rows in the task's `## Status History` where the Message column contains `FAIL:`:
       - **Count < 3** → mark back to `[📋]` (pending) in task file YAML and TASKS.md
       - **Count ≥ 3** → mark `[🚨]` (requires-user-attention) in task file YAML and TASKS.md; append a `## [🚨] Requires User Attention` block to the task file:
         ```markdown
         ## [🚨] Requires User Attention

         This task has failed review **{N} times**. Automated agents will not retry it.

         **Last failure reason**: {last FAIL row message}

         **Human actions available**:
         - Revise acceptance criteria → add "Human reset: AC revised" to Status History → reset to `[📋]`
         - Split into simpler sub-tasks → mark this `[❌]`
         - Cancel → mark `[❌]` with reason
         - Override as complete → mark `[✅]` with manual sign-off note
         ```
    3. Document specific failure reason in task file (Review Note section)
    - The Status History row message must name which ACs failed and why. `FAIL` alone is not acceptable.
    - **Agents must NEVER autonomously reset `[🚨]` back to `[📋]` — only a human can do this.**

**f) Docs check** (PASS tasks only — fires at true completion):
  - Does this task add/remove/change user-facing behavior? (skills, commands, agents, hooks, rules, conventions)
  - **YES** → append entry to `CHANGELOG.md` under `[Unreleased]`; update `README.md` if a relevant section exists
  - **NO** (internal refactor, task file edits, bug fixes with no interface change) → skip
  - Refer to `g-rl-26-readme-changelog.mdc` for what qualifies and where to update

**Per-task output format:**
```
REVIEW: Task 014 — g-go role separation
  ✅ g-go-code.md created in template_full/.cursor/commands/
  ✅ g-go-review.md created with NEW-SESSION warning
  ❌ g-go.md not updated — self-review banner missing
  → RESULT: FAIL — moved back to [📋] — reason recorded in task file
```

### 4. Final Results Table

```
REVIEW RESULTS
──────────────────────────────────────────
Task 014  [✅] PASS — all 6 acceptance criteria met
Task 015  [❌] FAIL — DECISIONS.md missing seed entries (criterion 1)
Task 016  [✅] PASS — BACKPORT_REPORT.md present and complete
──────────────────────────────────────────
Total: 2 PASS / 1 FAIL
```

### 5. Session Summary

```markdown
## Review Session Summary

### Reviewed PASS → [✅]
- Task #X: {title} — {brief note}

### Reviewed FAIL → back to [📋]
- Task #Y: {title} — {specific failure reason}

### Skipped (Implemented This Session)
- Task #Z: left at [🔍] — cannot self-review

### Recommended Next Steps
- Re-implement failed tasks: {list}
- Hand back to implementing agent if blocking
```

## Behavioral Rules

| Rule | Why |
|------|-----|
| Never implement anything | This is read-only review |
| Never mark `[✅]` for work you coded this session | Defeats independence guarantee |
| Document PASS/FAIL per criterion, not just overall | Gives implementing agent actionable feedback |
| Leave `[🔍]` items you can't review (no context) | Don't guess |
| Be strict — partial implementations fail | A task either meets criteria or it doesn't |

## Swarm Mode (`--swarm`)

When `$ARGUMENTS` includes `--swarm`, activate the **COORDINATOR PHASE** to parallelize review.
Review is read-only — partitioning is simpler than `g-go-code --swarm` (no subsystem conflicts).

### Coordinator Phase (runs FIRST when --swarm is present)

**Step R1: Collect review queue** — all `[🔍]` items (or filtered subset if task IDs specified in `$ARGUMENTS`).

**Step R2: Evaluate swarm eligibility**
- If only 1 qualifying `[🔍]` item → fallback to standard single-agent mode:
  `[SWARM] Single item — running standard mode`
- If 0 qualifying items → exit with "nothing to review" message

**Step R3: Compute agent count** (same Smart Agent Count Formula as g-go-code)

| Queue size | Agents |
|-----------|--------|
| 1 | 1 (no swarm — fallback) |
| 2–4 | 2 |
| 5–9 | `ceil(count / 3)` (2–3) |
| 10–14 | 4 |
| 15+ | 5 (hard cap) |

**Step R4: Partition via round-robin**
```
1. Sort review_queue by priority (Critical→Low)
2. Buckets = [[] for _ in range(agent_count)]
3. For i, item in enumerate(review_queue):
     buckets[i % agent_count].append(item)
4. Output: buckets = [[task_ids...], [task_ids...], ...]
```

No conflict graph needed — review agents only write to their own task files (disjoint by partition).

**Step R5: Display partition plan**
```
[SWARM] Review queue: {M} items → {N} reviewers
  Reviewer 1: Task 14 (high), Task 17 (low)
  Reviewer 2: Task 15 (high), Task 18 (medium)
Spawning {N} reviewer agents...
```

**Step R6: Spawn reviewer agents**
- Use the Agent tool to spawn N agents, each receiving:
  - The full `g-go-review` prompt (this command file content)
  - A `tasks X, Y, Z` filter argument for that reviewer's slice
  - Independence reminder: "Do not review tasks you implemented in this session."
- **IMPORTANT**: Each reviewer produces a **result payload** (PASS/FAIL per task + status history entry) but does **NOT** write to `TASKS.md`. Only writes to individual task files.

**Step R7: Collect, batch-update TASKS.md, and merge summary**

After all reviewers complete:
1. Read each reviewer's results (which tasks PASS, which FAIL)
2. **Batch-update TASKS.md** in a single write:
   - PASS items: `[🔍]` → `[✅]`
   - FAIL items: `[🔍]` → `[📋]` (back to pending)
3. Write unified review summary:

```markdown
## Swarm Review Session Summary

### Swarm Configuration
- Reviewers spawned: N
- Partition strategy: round-robin by priority
- Total items reviewed: M

### Reviewer Results
| Reviewer | Tasks Assigned | PASS | FAIL | Skipped |
|----------|---------------|------|------|---------|
| Reviewer-1 | 14, 17 | 2 | 0 | 0 |
| Reviewer-2 | 15, 18 | 1 | 1 | 0 |

### Reviewed PASS → [✅]
- Task #14: {title}
- Task #17: {title}

### Reviewed FAIL → back to [📋]
- Task #18: {title} — {failure reason}

### Recommended Next Steps
- Re-implement failed tasks: @g-go-code tasks {failed_ids}
```

### Why Coordinator Owns TASKS.md Writes

Two agents updating different lines in `TASKS.md` simultaneously causes merge conflicts.
Each reviewer reports its results; the coordinator performs **one atomic batch write** after all finish.
Individual task file writes (status history append) are safe because each reviewer's task set is disjoint.

---

## Usage Examples

```
@g-go-review
@g-go-review tasks 14 15 16
@g-go-review tasks 14
@g-go-review --swarm
@g-go-review --swarm tasks 14 15 16 17 18
```

Ready to review.
