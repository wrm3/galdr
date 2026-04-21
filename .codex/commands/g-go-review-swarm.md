Alias for `@g-go-review --swarm`: $ARGUMENTS

Runs **verification only** in swarm mode — splits the `[🔍]` queue across M parallel
reviewer agents (round-robin). Coordinator batch-writes TASKS.md after all reviewers complete.

This is exactly `@g-go-review --swarm`. Use this command for discoverability.

> ⚠️  **Run this in a NEW agent session** — different window, different invocation.
> If you implemented any of these tasks in this session, skip them.

## Usage

```
@g-go-review-swarm
@g-go-review-swarm tasks 14 15 16 17 18
```

All filter arguments pass through to `@g-go-review --swarm`.

See `@g-go-review` for full review protocol and swarm coordinator rules.

Ready to review.