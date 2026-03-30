---
name: g-bug-report
description: Document a new bug in BUGS.md and create a corresponding task. Use for any defect — even pre-existing or out-of-scope ones.
---
# galdr-bug-report

## When to Use
Any time a defect, error, or warning is identified — even "pre-existing" or "unrelated to current task".

**Zero tolerance**: If you mention it, you log it.

## Steps

1. **Determine next bug ID**: read `.galdr/BUGS.md`, find highest BUG-NNN, increment

2. **Classify severity**:
   - **Critical**: crash, data loss, security vulnerability
   - **High**: major feature failure, >50% perf regression
   - **Medium**: minor feature issue, usability problem
   - **Low**: cosmetic, pre-existing/out-of-scope

3. **Fast-path for pre-existing/out-of-scope** (30 seconds):
```markdown
### Bug ID: BUG-NNN
- **Title**: [Brief description]
- **Severity**: Low
- **Source**: Development (noticed during Task #NNN)
- **Status**: Open
- **File**: path/to/file.ext (line N if known)
- **Note**: Pre-existing. Not blocking current task.
- **Created**: YYYY-MM-DD
```

4. **Full entry for active bugs**:
```markdown
### Bug ID: BUG-NNN
- **Title**: [BUG] Brief description
- **Severity**: Critical | High | Medium | Low
- **Source**: user_reported | development | testing | production
- **Phase Impact**: [Phase N]
- **Status**: Open
- **Task Reference**: Task #NNN (create below)
- **Created**: YYYY-MM-DD
- **Description**: What's wrong
- **Steps to Reproduce**: 
  1. Step one
  2. Step two
- **Expected**: What should happen
- **Actual**: What actually happens
```

5. **Create task** (for Medium/High/Critical bugs):
   - Add `| [📋] | NNN | [BUG] {title} |` to TASKS.md
   - Create task file with `type: bug_fix`, `bug_reference: BUG-NNN`

6. **Confirm**: "Bug logged as BUG-NNN: {title}"
