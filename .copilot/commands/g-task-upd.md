Update task status or fields. Activates **g-skl-tasks** → UPDATE STATUS operation.

```
@g-task-upd TASK-NNN status in-progress
@g-task-upd TASK-NNN priority high
@g-task-upd TASK-NNN add-dependency TASK-MMM
```

The skill handles: file update, TASKS.md sync, Status History append, subsystem Activity Log update.

> **Alias**: `@g-task-update` also works (deprecated; use `@g-task-upd` for new work).
