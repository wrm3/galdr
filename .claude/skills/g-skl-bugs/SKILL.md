---
name: g-skl-bugs
description: Own and manage all bug data — BUGS.md index, bugs/ individual files, bug fixes, quality metrics. Single source of truth for everything bug and quality related.
---
# g-bugs

**Files Owned**: `.galdr/BUGS.md`, `.galdr/bugs/bugNNN_*.md`

**Activate for**: report bug, fix bug, quality metrics, "BUG-NNN", any mention of error/defect/warning.

**Auto-trigger (mandatory — no exceptions):**
- A task is moved back to `[📋]` by `@g-go-review` → immediately file a bug for each failing criterion
- A fix is applied in a session without a prior bug report → retroactively file the bug before the response ends
- Any error, warning, or "pre-existing" mention appears in a response → file a bug (g-rl-33)

**Zero tolerance rule**: if you mention it, you log it. Pre-existing and unrelated bugs still get logged.

---

## Operation: REPORT BUG

1. **Determine next ID**: read `BUGS.md`, find highest BUG-NNN → increment by 1

2. **Classify severity**:
   - **Critical**: crash, data loss, security vulnerability
   - **High**: major feature failure, >50% perf regression
   - **Medium**: minor feature issue, usability problem
   - **Low**: cosmetic, pre-existing, out-of-scope

3. **Create bug file** at `.galdr/bugs/bugNNN_descriptive_name.md`:
```yaml
---
id: NNN
title: 'Bug Title'
severity: critical | high | medium | low
status: open
source: development | testing | production | user_reported
subsystems: [affected-subsystems]
file: 'path/to/file.ext'
line: null
task_reference: null
prd_reference: null
created_date: 'YYYY-MM-DD'
resolved_date: ''
---
# BUG-NNN: Bug Title

## Description
[What's wrong]

## Reproduction
1. Step one
2. Step two

## Expected vs Actual
- **Expected**: [what should happen]
- **Actual**: [what actually happens]

## Root Cause
[Filled in when resolved]

## Fix
[Filled in when resolved]

## Status History

| Timestamp | From | To | Message |
|-----------|------|----|---------|
| YYYY-MM-DD | — | open | Bug filed |
```

4. **Add to BUGS.md** (atomic — same response):
   ```
   | [🔴] | BUG-NNN | Brief description | Critical | subsystem |
   ```
   Update "Next Bug ID" counter at bottom.

5. **Update subsystem Activity Log** for each affected subsystem (see g-subsystems)

6. **Create task for Medium/High/Critical bugs** — activate g-tasks CREATE with `type: bug_fix` and `bug_reference: BUG-NNN`

7. **Confirm**: `✅ Logged as BUG-NNN: {title} [{severity}]`

---

## Operation: VERIFICATION FAILURE → AUTO BUG

Triggered when `@g-go-review` marks a task back to `[📋]` for failing one or more criteria.

1. **For each failing criterion** in the verification result:
   - Classify severity: criterion about core behavior → Medium; cosmetic/doc → Low
   - File a bug using REPORT BUG operation with:
     - `title`: "{task title} — {criterion description} unmet at verification"
     - `source: testing`
     - `task_reference: task{NNN}`
     - `subsystems`: same as the failed task

2. **Link task ↔ bug**: update the task file to include `bug_reference: BUG-NNN`

3. **Note in bug file** whether the root cause is:
   - **Missing implementation** (agent didn't build it) → `type: missed_implementation`
   - **Broken implementation** (built but wrong) → `type: regression`
   - **Process gap** (workflow didn't enforce it) → `type: process_gap`

**This ensures every verification failure leaves a traceable quality record, not just
a task moved silently back to [📋].**

---

## Operation: RETROACTIVE BUG (fix without prior report)

When a fix was applied in this session but no bug was filed before or during the fix:

1. File the bug using REPORT BUG with `status: resolved`, `resolved_date: today`
2. Fill in Root Cause and Fix sections immediately (you just did the fix — document it)
3. Note in bug file: "Retroactively filed — fix applied before bug was logged"
4. Link bug to any associated task via `task_reference`

**Retroactive bugs still count.** The audit trail matters even after the fact.

---

## Operation: FIX BUG

1. **Read** `.galdr/bugs/bugNNN_*.md` — reproduction steps, expected/actual
2. **Read linked task** (if any) — check acceptance criteria
3. **Implement fix**
4. **Update bug file**:
   ```yaml
   status: resolved
   resolved_date: 'YYYY-MM-DD'
   ```
   Fill in "Root Cause" and "Fix" sections.

5. **Update BUGS.md**: change indicator from `[🔴]` to `[✅]`
6. **Update subsystem Activity Log** — append: `| YYYY-MM-DD | BUG | NNN | Fixed: {brief} |`
7. **Append to Status History** in the bug file (REQUIRED):
   ```
   | YYYY-MM-DD | open | resolved | Fix applied: {brief description of fix} |
   ```
   If bug was reopened: `| YYYY-MM-DD | resolved | open | Reopened: {reason} |`
8. **Update linked task** (if any) → `status: awaiting-verification` via g-tasks UPDATE
9. **Offer git commit**:
   ```
   fix({subsystem}): resolve BUG-NNN — {brief description}
   Bug: BUG-NNN | Root cause: {brief}
   ```

**Fast path (pre-existing/Low severity)**:
- Fix inline, update bug file + BUGS.md status, append Activity Log — no separate task needed

---

## Operation: QUALITY REPORT

1. **Read BUGS.md** — parse all entries, group by severity and status
2. **Collect metrics**:
   - Total: open / resolved / in-progress
   - Severity distribution: critical/high/medium/low
   - Resolution rate: resolved / total × 100
   - Average age of open bugs (days since created)
3. **Subsystem impact**: which subsystems have the most open bugs?
4. **Output**:
```markdown
# Quality Metrics
Generated: YYYY-MM-DD

## Bug Summary
| Metric | Value |
|---|---|
| Total | N |
| Open | N |
| Resolved | N |
| Resolution Rate | N% |

## Severity Distribution
| Severity | Open | Resolved |
|---|---|---|
| Critical | N | N |
| High | N | N |
| Medium | N | N |
| Low | N | N |

## Hottest Subsystems
| Subsystem | Open Bugs |
|---|---|
| {name} | N |

## Quality Score: N/100
Healthy (≥80) | Degraded (50-79) | Critical (<50)
```

---

## Severity Indicators Reference

| Indicator | Severity | BUGS.md |
|---|---|---|
| `[🔴]` | Critical | Open |
| `[🟠]` | High | Open |
| `[🟡]` | Medium | Open |
| `[⚪]` | Low | Open |
| `[✅]` | Any | Resolved |
| `[🔄]` | Any | In Progress |
| `[🚨]` | Any | Requires User Attention |

---

## Circuit-Breaker Rule: Stuck Bug Detection

When any bug fix has been verified and **FAILED 3 or more times**:

1. **Count FAIL rows** in the bug's `## Status History` table (rows where Message contains "FAIL:")
2. **If count ≥ 3** → mark the bug `[🚨]` (requires-user-attention) instead of returning to `[📋]`
3. **Append stuck note** to the bug file:

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

4. **Never autonomously reset** `[🚨]` back to `[📋]` — only a human can do this.

This prevents infinite fix→verify→fail loops from burning agent tokens.
