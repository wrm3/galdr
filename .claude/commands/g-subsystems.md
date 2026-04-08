Manage the subsystem registry. Activates **g-skl-subsystems**.

## Usage

```
@g-subsystems [check | add <name> | update <name>]
```

## Operations

| Argument | What it does |
|----------|-------------|
| *(no args)* | **SYNC CHECK** — audit all task files' `subsystems:` fields against SUBSYSTEMS.md; report missing entries; create stub specs for any that don't exist |
| `check` | Same as no-args — explicit sync check alias |
| `add <name>` | CREATE SUBSYSTEM SPEC — scaffold `.galdr/subsystems/<name>.md` and add entry to SUBSYSTEMS.md index |
| `update <name>` | UPDATE ACTIVITY LOG — append latest task/bug completions to `<name>.md` Activity Log |

## When to Use

- After completing a batch of tasks: `@g-subsystems update cross-project`
- When the registry looks stale: `@g-subsystems check`
- When adding a new functional area to the project: `@g-subsystems add <name>`
- During `@g-grooming` or `@g-cleanup` to catch subsystem drift

## Integrity Rule

**Every task file must reference ≥1 subsystem in its `subsystems:` field, and every
referenced subsystem must have an entry in SUBSYSTEMS.md.**  
`@g-subsystems check` enforces this invariant.

Activate the **g-skl-subsystems** skill, matching operation to the argument given.

