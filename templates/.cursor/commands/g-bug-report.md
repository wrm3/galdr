Report a bug: $ARGUMENTS

## What This Command Does

Documents a bug in the galdr QA system and creates a corresponding fix task.

## Bug Reporting Workflow

### 1. Gather Bug Details
I'll ask for:
- **Severity**: Critical, High, Medium, or Low
- **Source**: User Reported, Development, Testing, or Production
- **Reproduction Steps**: How to reproduce the bug
- **Expected vs Actual**: What should happen vs what does happen
- **Environment**: Browser, OS, version info (if applicable)
- **Phase Impact**: Which project phases are affected

### 2. Create BUGS.md Entry
I'll add to `.galdr/tracking/BUGS.md`:
```markdown
### Bug ID: BUG-XXX
- **Title**: [Brief description]
- **Severity**: [Critical/High/Medium/Low]
- **Source**: [User Reported/Development/Testing/Production]
- **Phase Impact**: [Affected phases]
- **Status**: Open
- **Task Reference**: task{ID}
- **Created**: [Date]
- **Assigned**: [Developer]

**Description**: [Detailed description]

**Reproduction Steps**:
1. Step one
2. Step two

**Expected**: [What should happen]
**Actual**: [What actually happens]
```

### 3. Create Bug Fix Task
I'll generate a task file with:
- Filename: `task{ID}_bug_fix_description.md`
- Title prefix: `[BUG]`
- Type: `bug_fix`
- Priority: Matches severity
- Bug reference linking to BUGS.md

### 4. Update TASKS.md
I'll add the bug fix task under the appropriate phase.

## Severity Guidelines
- **Critical**: System crashes, data loss, security issues → Fix same day
- **High**: Major feature broken, >50% performance loss → Fix 1-2 days
- **Medium**: Minor issues, usability problems → Fix 3-7 days
- **Low**: Cosmetic issues, enhancements → Fix next release

## CRITICAL: Triple Update
**I MUST update ALL THREE:**
1. ✅ BUGS.md - Add bug entry
2. ✅ Task file - Create bug fix task
3. ✅ TASKS.md - Add task entry

## What I Need From You
- Description of the bug
- How to reproduce it
- What you expected vs what happened
- Severity assessment
- Which phase(s) are affected

Let's document this bug!
