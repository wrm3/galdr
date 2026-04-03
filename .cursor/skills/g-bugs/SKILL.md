---
name: g-bugs
description: Own and manage all bug data — BUGS.md index, bugs/ individual files, bug fixes, quality metrics. Single source of truth for everything bug and quality related.
---
# g-bugs

**Files Owned**: `.galdr/BUGS.md`, `.galdr/bugs/bugNNN_*.md`

**Activate for**: report bug, fix bug, quality metrics, "BUG-NNN", any mention of error/defect/warning.

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
7. **Update linked task** (if any) → `status: awaiting-verification` via g-tasks UPDATE
8. **Offer git commit**:
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
