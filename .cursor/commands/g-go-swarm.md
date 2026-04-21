Alias for `@g-go --swarm`: $ARGUMENTS

Runs the full **pipeline orchestrator** in swarm mode:
- **Phase 1**: N parallel implementation agents (subsystem-boundary partition)
- **Phase 2**: M parallel reviewer agents (round-robin, fresh context each)

This is exactly `@g-go --swarm`. Use this command for discoverability.

## Usage

```
@g-go-swarm
@g-go-swarm tasks 7, 9, 10, 11, 12
@g-go-swarm bugs-only
```

All filter arguments pass through to `@g-go --swarm`.

See `@g-go` for full pipeline documentation and swarm agent count / partition rules.

Let's go.