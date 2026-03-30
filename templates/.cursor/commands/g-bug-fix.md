Fix a reported bug: $ARGUMENTS

## What This Command Does

Works on and resolves a bug that was previously reported in the galdr QA system.

## Bug Fix Workflow

### 1. Identify the Bug
I'll:
- Look up the bug in `.galdr/BUGS.md`
- Find the associated task file in `.galdr/tasks/`
- Review bug details: reproduction steps, expected vs actual behavior
- Check severity and priority

### 2. Analyze Root Cause
I'll:
- Locate the problematic code
- Understand why the bug occurs
- Identify all affected areas
- Consider edge cases

### 3. Implement the Fix
I'll:
- Make minimal, focused changes
- Follow project coding standards
- Add comments explaining non-obvious fixes
- Ensure fix doesn't introduce new issues
- Consider backward compatibility

### 4. Verify the Fix
I'll:
- Test the fix resolves the reported issue
- Run existing tests to prevent regressions
- Add new tests if needed
- Verify edge cases mentioned in bug report

### 5. Update All Tracking Files

**BUGS.md** - Update bug status:
```markdown
### Bug ID: BUG-XXX
- **Status**: Closed ✅
- **Resolution**: Fixed in task{ID}
- **Fixed Date**: [Date]
```

**Task File** - Update to completed:
```yaml
---
status: completed
completed_date: '2026-01-26'
resolution_notes: 'Brief description of fix'
---
```

**TASKS.md** - Update status indicator:
```markdown
- [✅] Task XXX: [BUG] Fix description
```

## CRITICAL: Triple Update Required

**I MUST update ALL THREE files:**
1. ✅ BUGS.md - Mark bug as Closed
2. ✅ Task file - Set status to completed
3. ✅ TASKS.md - Change indicator to [✅]

## Bug Lifecycle

```
Report Bug (galdr-report-bug)
    ↓
Bug documented in BUGS.md [Open]
Task created [📋]
    ↓
Start Fix (galdr-fix-bug)
    ↓
Task in progress [🔄]
Bug status: Fixing
    ↓
Fix Complete
    ↓
Bug closed [Closed]
Task completed [✅]
```

## What I Need From You
- Bug ID (e.g., BUG-001) or description
- Any additional context about the bug
- Preferred approach (if you have one)

Let's fix this bug!
