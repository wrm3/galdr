Alias for `@g-go-code --swarm`: $ARGUMENTS

Runs **implementation only** in swarm mode — partitions the work queue into conflict-safe
buckets and spawns N parallel agents. Every completed item is marked `[🔍]`.

This is exactly `@g-go-code --swarm`. Use this command for discoverability.

## Usage

```
@g-go-code-swarm
@g-go-code-swarm tasks 7, 9, 10, 11, 12
@g-go-code-swarm bugs-only
```

All filter arguments pass through to `@g-go-code --swarm`.

See `@g-go-code` for full implementation protocol and swarm coordinator rules.

Let's implement.