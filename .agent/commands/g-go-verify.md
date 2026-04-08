Verification-only backlog review: $ARGUMENTS

## Mode: VERIFY ONLY

> ⚠️  **Run this in a NEW agent session** — different window, different invocation.
> If you implemented any of these tasks in this session, **skip them** (leave `[🔍]`).
> Self-verification defeats the purpose of this gate.

---

## Execution Protocol

### 1. Load Context

Read in this order:
- `.galdr/TASKS.md` — identify all `[🔍]` (Awaiting Verification) tasks
- Individual task files for each `[🔍]` item — read acceptance criteria
- `git log --oneline -10` — understand what was recently implemented
- `.galdr/CONSTRAINTS.md` — guardrails

### 2. Build the Verification Queue

Collect all tasks/bugs with status `[🔍]`.  
If `$ARGUMENTS` specifies IDs (e.g. `@g-go-verify tasks 14 15`), verify only those.

**Skip any item you implemented in this session.** Leave it `[🔍]` for a future agent.

### 3. Verify Each Item

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

         This task has failed verification **{N} times**. Automated agents will not retry it.

         **Last failure reason**: {last FAIL row message}

         **Human actions available**:
         - Revise acceptance criteria → add "Human reset: AC revised" to Status History → reset to `[📋]`
         - Split into simpler sub-tasks → mark this `[❌]`
         - Cancel → mark `[❌]` with reason
         - Override as complete → mark `[✅]` with manual sign-off note
         ```
    3. Document specific failure reason in task file (Verification Note section)
    - The Status History row message must name which ACs failed and why. `FAIL` alone is not acceptable.
    - **Agents must NEVER autonomously reset `[🚨]` back to `[📋]` — only a human can do this.**

**f) Docs check** (PASS tasks only — fires at true completion):
  - Does this task add/remove/change user-facing behavior? (skills, commands, agents, hooks, rules, conventions)
  - **YES** → append entry to `CHANGELOG.md` under `[Unreleased]`; update `README.md` if a relevant section exists
  - **NO** (internal refactor, task file edits, bug fixes with no interface change) → skip
  - Refer to `g-rl-26-readme-changelog.mdc` for what qualifies and where to update

**Per-task output format:**
```
VERIFY: Task 014 — g-go role separation
  ✅ g-go-code.md created in template_full/.cursor/commands/
  ✅ g-go-verify.md created with NEW-SESSION warning
  ❌ g-go.md not updated — self-review banner missing
  → RESULT: FAIL — moved back to [📋] — reason recorded in task file
```

### 4. Final Results Table

```
VERIFY RESULTS
──────────────────────────────────────────
Task 014  [✅] PASS — all 6 acceptance criteria met
Task 015  [❌] FAIL — DECISIONS.md missing seed entries (criterion 1)
Task 016  [✅] PASS — BACKPORT_REPORT.md present and complete
──────────────────────────────────────────
Total: 2 PASS / 1 FAIL
```

### 5. Session Summary

```markdown
## Verification Session Summary

### Verified PASS → [✅]
- Task #X: {title} — {brief note}

### Verified FAIL → back to [📋]
- Task #Y: {title} — {specific failure reason}

### Skipped (Implemented This Session)
- Task #Z: left at [🔍] — cannot self-verify

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
| Leave `[🔍]` items you can't verify (no context) | Don't guess |
| Be strict — partial implementations fail | A task either meets criteria or it doesn't |

## Usage Examples

```
@g-go-verify
@g-go-verify tasks 14 15 16
@g-go-verify tasks 14
```

Ready to verify.
