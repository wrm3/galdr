---
name: g-bug-report
description: Document a new bug in BUGS.md and create an individual bug file in bugs/. Use for any defect — even pre-existing or out-of-scope ones.
---
# galdr-bug-report

## When to Use
Any time a defect, error, or warning is identified — even "pre-existing" or "unrelated to current task".

**Zero tolerance**: If you mention it, you log it.

## Steps

1. **Determine next bug ID**: read `.galdr/BUGS.md`, find highest BUG-NNN, increment by 1

2. **Classify severity**:
   - **Critical**: crash, data loss, security vulnerability
   - **High**: major feature failure, >50% perf regression
   - **Medium**: minor feature issue, usability problem
   - **Low**: cosmetic, pre-existing/out-of-scope

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
   - Add row: `| [📋] | BUG-NNN | Brief description | Severity | subsystem1, subsystem2 |`
   - Update "Next Bug ID" at bottom

5. **Append to subsystem Activity Log** for each affected subsystem:
   - Read `.galdr/subsystems/{subsystem}.md`
   - Append row to Activity Log table: `| YYYY-MM-DD | BUG | NNN | {title} | PRD-NNN |`

6. **Create task** (for Medium/High/Critical bugs):
   - Follow g-task-new steps with `type: bug_fix` and `bug_reference: BUG-NNN`

7. **Confirm**: "Bug logged as BUG-NNN: {title}"
