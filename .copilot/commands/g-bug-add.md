Report a new bug. Activates **g-skl-bugs** → REPORT BUG operation.

```
@g-bug-add "Description of the bug"
@g-bug-add "Description" --severity high --file path/to/file.py --line 42
```

Zero-tolerance: pre-existing and unrelated bugs still get logged. Describe the bug and the skill handles BUG-NNN ID assignment, file creation, BUGS.md index entry.

> **Alias**: `@g-bug-report` also works (deprecated; use `@g-bug-add` for new work).
