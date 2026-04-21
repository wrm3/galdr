Alias for `@g-go-review --swarm`: $ARGUMENTS

Runs **verification only** in swarm mode — splits the `[🔍]` queue across M parallel
reviewer agents (round-robin). Includes both **tasks** and **bugs** awaiting verification.
Coordinator batch-writes TASKS.md and BUGS.md after all reviewers complete.

This is exactly `@g-go-review --swarm`. Use this command for discoverability.

> ⚠️  **Run this in a NEW agent session** — different window, different invocation.
> If you implemented any of these tasks or bug fixes in this session, skip them.

## Usage

```
@g-go-review-swarm
@g-go-review-swarm tasks 14 15 16 17 18
@g-go-review-swarm bugs BUG-013 BUG-014
@g-go-review-swarm tasks 14 15 bugs BUG-013
```

All filter arguments pass through to `@g-go-review --swarm`.

See `@g-go-review` for full review protocol and swarm coordinator rules.

Ready to review.
