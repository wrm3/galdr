# galdr-task-sync-check Command

Validate synchronization between TASKS.md and individual task files.

## Usage

```
@g-task-sync-check
```

## What This Command Does

1. **Reads TASKS.md** to get all task entries and their status indicators
2. **Scans .galdr/tasks/** to find all task files
3. **Compares** each task's TASKS.md indicator against its file's YAML status
4. **Reports** any mismatches, orphans, or phantoms
5. **Offers to fix** any synchronization issues found

## Expected Output

### All Synced
```markdown
📋 TASK SYNCHRONIZATION REPORT

## Validation Results

| Task ID | TASKS.md | Task File | Status |
|---------|----------|-----------|--------|
| 001 | [📋] | pending | ✅ SYNCED |
| 002 | [🔄] | in-progress | ✅ SYNCED |
| 003 | [✅] | completed | ✅ SYNCED |

**Summary**: 3/3 tasks synchronized ✅
**Orphan Files**: None
**Phantom Entries**: None

All tasks are properly synchronized!
```

### With Issues
```markdown
📋 TASK SYNCHRONIZATION REPORT

## Validation Results

| Task ID | TASKS.md | Task File | Status |
|---------|----------|-----------|--------|
| 001 | [📋] | pending | ✅ SYNCED |
| 002 | [🔄] | completed | ⚠️ MISMATCH |
| 003 | [✅] | completed | ✅ SYNCED |

**Summary**: 2/3 tasks synchronized
**Mismatches Found**: 1

### Mismatches
- **Task 002**: TASKS.md shows [🔄] but file has `status: completed`
  - Recommendation: Update TASKS.md to [✅]

### Orphan Files (in .galdr/tasks/ but not in TASKS.md)
- task099_forgotten_feature.md

### Phantom Entries (in TASKS.md but no file exists)
- Task 055: Setup caching [📋]

---
**Fix these issues?** Reply "fix" to auto-correct all mismatches.
```

## Status Mapping Reference

| TASKS.md Indicator | Task File YAML Status |
|--------------------|-----------------------|
| `[ ]` | (file may not exist) |
| `[📋]` | `status: pending` |
| `[🔄]` | `status: in-progress` |
| `[✅]` | `status: completed` |
| `[❌]` | `status: failed` |

## Auto-Fix Behavior

When user replies "fix":
1. Update TASKS.md indicators to match task file statuses (file is source of truth)
2. Report orphan files for user decision (add to TASKS.md or delete)
3. Report phantom entries for user decision (create file or remove entry)

## When to Run This Command

- At the start of a work session
- Before generating status reports
- After bulk task operations
- When task status seems inconsistent
- Before phase completion reviews

## Implementation Notes

This command should:
1. Use glob to find all `task*.md` files in `.galdr/tasks/`
2. Parse YAML frontmatter from each file to get `status` field
3. Parse TASKS.md to extract task IDs and their indicators
4. Compare and report differences
5. Offer atomic fixes that update both files together
