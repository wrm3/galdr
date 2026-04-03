---
name: g-bug-fix
description: Fix a reported bug — document the fix, update bug file and BUGS.md status, append subsystem activity logs, and create a retroactive task if work was done in-chat.
---
# galdr-bug-fix

## When to Use
@g-bug-fix or "fix bug BUG-NNN". Documents a bug fix with evidence.

## Steps

1. **Read bug file** from `.galdr/bugs/bugNNN_*.md`: get reproduction steps, expected/actual behavior

2. **Read linked task** if any: check acceptance criteria

3. **Implement fix**

4. **Update bug file** (`.galdr/bugs/bugNNN_*.md`):
   ```yaml
   status: resolved
   resolved_date: 'YYYY-MM-DD'
   ```
   Fill in "Root Cause" and "Fix" sections in the markdown body.

5. **Create evidence log** at `.galdr/logs/bugNNN_evidence.log`:
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

6. **Update BUGS.md**: Change status indicator from `[🔄]` to `[✅]`

7. **Append to subsystem Activity Log** for each affected subsystem:
   - Read `.galdr/subsystems/{subsystem}.md`
   - Append row: `| YYYY-MM-DD | BUG | NNN | Fixed: {brief description} | PRD-NNN |`

8. **Update task file** (if linked) to `status: awaiting-verification`

9. **Update TASKS.md** (if linked): `[🔄]` to `[🔍]`

10. **Offer git commit**:
   ```
   fix({subsystem}): resolve BUG-NNN — {brief description}
   
   Bug: BUG-NNN
   Task: #NNN
   Root cause: {brief}
   ```

## For Pre-existing / Low-severity Bugs (Fast Path)
1. Add fix to current implementation
2. Update bug file status to resolved
3. Update BUGS.md status to `[✅]`
4. Append to subsystem Activity Log
5. Note in current task's implementation notes
6. No separate task needed
