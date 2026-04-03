---
name: g-bug-fix
description: Fix a reported bug — document the fix, update BUGS.md status, and create a retroactive task if work was done in-chat.
---
# galdr-bug-fix

## When to Use
@g-bug-fix or "fix bug BUG-NNN". Documents a bug fix with evidence.

## Steps

1. **Read bug entry** from BUGS.md: get reproduction steps, expected/actual behavior

2. **Read linked task** if any: check acceptance criteria

3. **Implement fix**

4. **Document the fix** in the task file:
   ```yaml
   implementation_notes: 'Root cause: [what caused it]. Fix: [what was changed].'
   evidence_of_completion:
     type: runtime_log | test_output | compile_log
     path: '.galdr/logs/taskNNN_evidence.log'
   ```

5. **Create evidence log** at `.galdr/logs/taskNNN_evidence.log`:
   ```
   === BUG FIX EVIDENCE — BUG-NNN ===
   Date: {timestamp}
   Bug: {title}
   
   === ROOT CAUSE ===
   {explanation}
   
   === FIX APPLIED ===
   File: {filepath}
   Change: {what changed}
   
   === VERIFICATION ===
   Before: {error/wrong behavior}
   After: {correct behavior}
   
   === SIGN-OFF ===
   Status: FIXED
   ```

6. **Update BUGS.md**:
   - Change `Status: Open` → `Status: Closed`
   - Add `Resolution date: YYYY-MM-DD`
   - Add `Resolution: Brief description of fix`

7. **Update task file** to `status: awaiting-verification` (bug fixes require verification)

8. **Update TASKS.md**: `[🔄]` → `[🔍]`

9. **Offer git commit**:
   ```
   fix({subsystem}): resolve BUG-NNN — {brief description}
   
   Bug: BUG-NNN
   Task: #NNN
   Root cause: {brief}
   ```

## For Pre-existing / Low-severity Bugs (Fast Path)
1. Add fix to current implementation
2. Update BUGS.md `Status: Closed`
3. Note in current task's implementation notes
4. No separate task needed
