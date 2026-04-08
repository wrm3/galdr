Implementation-only backlog execution: $ARGUMENTS

## Mode: IMPLEMENT ONLY

This command runs **coding and bug-fixing** — it does NOT verify. Every completed item is
marked `[🔍]` (Awaiting Verification) so a **separate agent session** can independently confirm it.

---

## Execution Protocol

### 1. Load Context (Before Touching Anything)

Read in this order:
- `.galdr/PROJECT.md` — mission, goals, ecosystem context
- `.galdr/PLAN.md` — current milestones
- `.galdr/BUGS.md` — open bugs (**read before TASKS** — bugs run first)
- `.galdr/TASKS.md` — master task list
- `.galdr/CONSTRAINTS.md` — guardrails (if exists)
- `.galdr/DECISIONS.md` — past decisions (if exists, read-only)
- `git log --oneline -10` — recent changes

### 2. Build the Work Queue

**Bugs first (Tier 1), then tasks (Tier 2).**

**Tier 1 — Open bugs:**
- From `BUGS.md` + `bugs/` files; Critical → High → Medium → Low
- Skip bugs with external blockers
- **Skip `[🚨]` bugs** — log in Skipped section as "Requires-User-Attention — human review needed"

**Tier 2 — Pending tasks:**
- Status `[ ]` (pending) or `[📋]` (ready)
- **NOT** `[🚨]` (requires-user-attention) — **skip entirely**, log in Skipped section as "Requires-User-Attention — human review needed"
- No unmet dependencies
- Not `ai_safe: false`
- Priority: Critical → High → Medium → Low

Supported `$ARGUMENTS` filters:
- Task IDs: `@g-go-code tasks 7, 9`
- Bug IDs: `@g-go-code bugs BUG-003`
- Subsystem: `@g-go-code subsystem vault-hooks-automation`
- `@g-go-code bugs-only` / `@g-go-code tasks-only`

### 3. Work Through Items Sequentially

For each item:

**a)** Read the task/bug file — understand objective and acceptance criteria  
**b)** Implement the solution — write code, make changes  
**b2) AC gate** — before moving on, walk every `- [ ]` acceptance criterion in the task spec:
  - Is this criterion now satisfied? Check the actual files, not just intent.
  - Any unmet criterion → return to **(b)** and address it.
  - Cannot meet a criterion this session → log as a Blocker in step 5 and **skip this task entirely** (do not mark `[🔍]` for partial work).
  - **Stub/TODO scan**: search files modified for this task for bare `# TODO`, `// TODO`, `pass` (non-abstract), `raise NotImplementedError`, `throw new Error("not implemented")` — each is an unmet criterion until annotated `TODO[TASK-X→TASK-Y]` with a follow-up task created (see `g-rl-34`)
  - **Bug-discovery check**: any pre-existing bug encountered while implementing must have a BUG entry + `BUG[BUG-{id}]` comment before `[🔍]`; bugs introduced by this task must be fixed inline (see `g-rl-35`)
  - **Constraint check**: run `@g-constraint-check` mentally — does this implementation violate any active constraint? Any `🚫 VIOLATION` blocks `[🔍]`
  - All criteria confirmed met → continue.
**b3) Status History** — before marking `[🔍]`, append a row to the `## Status History` table at the bottom of the task file:
  ```
  | YYYY-MM-DD | pending | awaiting-verification | Implementation complete; {1-line summary} |
  ```
  If the task file has no `## Status History` section yet, add it first (backfill row: `| {created_date} | — | pending | Task created (backfill) |`).
**c)** Validate — lint, test, check files exist  
**d)** Record decisions — if you chose approach A over B, append to `.galdr/DECISIONS.md`  
**e)** Update subsystem Activity Log — for each subsystem in the task's `subsystems:` field, append to `.galdr/subsystems/{name}.md` Activity Log: `| {date} | TASK | {id} | {title} | — |`. Create a stub spec if the file doesn't exist.  
**f)** Update status → mark `[🔍]` (NOT `[✅]`) in both task file and TASKS.md  
**g)** Move to next item

> **IMPORTANT**: Mark every completed item `[🔍]`, never `[✅]`.  
> `[✅]` requires a separate agent session running `@g-go-verify`.

### 4. Docs Check (Per Task)

After each task, ask: does this add/remove/change user-facing behavior?
- **YES** → Append entry to `CHANGELOG.md` (root); update `README.md` if relevant section exists
- **NO** (internal refactor only) → skip

### 5. Question & Blocker Collection

DO NOT stop to ask. Collect silently:

```markdown
## Deferred Items

### Questions (Need Human Answer)
- Q1: [question] (task #X)

### Blockers (Could Not Proceed)
- B1: Task #X — [reason]

### Decisions Made (FYI)
- D1: Task #X — chose A over B because [reason]
```

### 5. Record Decisions

Before the handoff message, append any new decisions to `.galdr/DECISIONS.md`:
- Use the next sequential ID after the last entry (`D{NNN}`)
- Include: Date | Decision | Rationale | this-agent

### 6. Session Summary + Handoff

```markdown
## Implementation Session Summary

### Moved to [🔍] (Awaiting Verification)
- [🔍] Task #X: {title}
- [🔍] Bug BUG-00N: {title}

### Skipped (Blocked)
- Task #Y: {reason}

### Deferred Questions & Blockers
{collected items from step 5}

### Decisions Made This Session
{append these to .galdr/DECISIONS.md}

### Handoff
{N} task(s) / {M} bug(s) moved to [🔍].
For independent verification: open a NEW agent session and run @g-go-verify.
```

## Behavioral Rules

| Rule | Why |
|------|-----|
| Never ask questions mid-execution | Uninterrupted autonomous work |
| Mark completed items `[🔍]`, never `[✅]` | Enforce independent verification gate |
| Log every decision made | Future agents and humans need the audit trail |
| Skip tasks you can't complete | Maximize total output |
| Respect CONSTRAINTS.md | Never violate project guardrails |
| Abort if destructive (schema drop, data loss) | Safety first — log it as a blocker |

## Usage Examples

```
@g-go-code
@g-go-code tasks 14, 15
@g-go-code bugs BUG-001, BUG-002
@g-go-code subsystem cross-project
@g-go-code bugs-only
```

Let's implement.
