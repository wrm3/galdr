---
name: g-task-update
description: Update task status in task file and TASKS.md atomically, step by step.
---
# galdr-task-update

## When to Use
Changing task status (start working, mark complete, pause, fail).

## Status Transitions
```
[ ] -> [📋] -> [🔄] -> [🔍] -> [✅]
              |         |
             [⏸️]       [📋] (verification failed — reset)
             [❌]
```

## Steps

1. **Read current state** (both files):
   - `.galdr/tasks/taskNNN_*.md` -> current YAML `status:`
   - `.galdr/TASKS.md` -> current indicator for task NNN
   - Verify they match — if not, fix mismatch first (file is source of truth)

2. **Apply transition**:

| Action | File YAML | TASKS.md |
|---|---|---|
| Start working | `status: in-progress` | `[🔄]` |
| Submit for verification | `status: awaiting-verification` | `[🔍]` |
| Mark complete (verifier only) | `status: completed` | `[✅]` |
| Pause | `status: paused` | `[⏸️]` |
| Mark failed | `status: failed` | `[❌]` |

3. **For in-progress**: also set:
```yaml
claimed_by: "{agent_id}"
claimed_at: "YYYY-MM-DDTHH:MM:SSZ"
claim_ttl_minutes: {estimated * 1.5}
claim_expires_at: "YYYY-MM-DDTHH:MM:SSZ"
```

4. **For completed**: also set:
```yaml
completed_date: "YYYY-MM-DD"
```
   Then run full completion workflow (see galdr-task-manager):
   - Validate acceptance criteria
   - Offer git commit
   - Check project files impact

5. **Append to subsystem Activity Log** (on completion or failure):
   - Read the task's `subsystems:` field
   - For each subsystem, read `.galdr/subsystems/{subsystem}.md`
   - Append row to Activity Log table: `| YYYY-MM-DD | TASK | NNN | {title} | PRD-NNN |`

6. **Regenerate dependency graph** (if dependencies changed or task completed):
   - If the task's `dependencies` field was modified, OR the task moved to `completed`/`failed`:
     regenerate `.galdr/DEPENDENCY_GRAPH.md` using the `g-dependency-graph` skill

7. **Print sync confirmation**:
```
Task Sync Confirmation:
- Task {ID} file: status: {new_status}
- TASKS.md entry: [{indicator}]
- Subsystem logs: {updated N subsystems | skipped}
- Dependency graph: {updated | no dependency changes, skipped}
- Sync verified
```
