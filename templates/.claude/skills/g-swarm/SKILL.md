---
name: g-swarm
description: >-
  Coordinate multiple agents working in parallel on independent tasks. Assigns
  work from SPRINT.md to available agent slots, respects subsystem boundaries,
  and manages parallel execution lifecycle.
---

# g-swarm

Coordinate multiple AI agents working in parallel on independent tasks.

## When to Use

- When multiple independent tasks are ready for implementation
- Manual trigger: `@g-heartbeat swarm`
- When the heartbeat scheduler has swarm mode enabled

## Prerequisites

- Task 600 (heartbeat scheduler) must be operational
- SPRINT.md must exist with queued tasks
- Tasks must have `ai_safe: true` and no unresolved dependencies

## Swarm Configuration

In `.galdr/HEARTBEAT.md` YAML frontmatter, add swarm settings:

```yaml
swarm:
  enabled: true
  max_agents: 3
  subsystem_isolation: true
  assignment_strategy: priority_first
```

### Assignment Strategies

| Strategy | Behavior |
|----------|----------|
| `priority_first` | Pick highest priority unblocked task |
| `round_robin` | Distribute evenly across subsystems |
| `subsystem_balanced` | Minimize subsystem conflicts |

## Swarm Coordinator Workflow

1. **Read SPRINT.md** — identify available tasks (`ai_safe`, unblocked, unclaimed)
2. **Read active locks** — count running agents from `.galdr/logs/heartbeat/locks/`
3. **While** running_agents < max_agents AND tasks available:
   a. Pick next task (by assignment strategy)
   b. Check subsystem isolation (no overlap with running agents)
   c. Check budget (remaining daily allowance)
   d. Select adapter (round-robin across configured adapters)
   e. Claim task (update task file status to `in-progress`)
   f. Spawn agent process (async, non-blocking)
   g. Write PID lockfile with task and subsystem info
4. **Monitor** running agents every 60 seconds:
   - Check PID still alive
   - Check TTL not expired
   - Force-kill if TTL exceeded by 2x
5. **Write swarm summary** after all agents complete

## Subsystem Isolation Rules

- Each running agent "locks" the subsystems declared in its task's YAML
- New task assignment checks for subsystem overlap with running agents
- Tasks with `requires_solo_agent: true` lock ALL subsystems (exclusive mode)
- Subsystem locks release when agent completes or fails

## Swarm Status File

Updated every 60 seconds at `.galdr/SWARM_STATUS.md`:

```markdown
# Swarm Status

**Active Agents**: N/M
**Budget Remaining**: $X.XX / $Y.YY
**Last Updated**: {ISO8601}

| Agent | Task | Subsystem | Adapter | Started | TTL |
|-------|------|-----------|---------|---------|-----|
| swarm-001 | 510 | mcp-server | cursor | 14:00 | 16:00 |
| swarm-002 | 512 | skills-library | claude | 14:15 | 16:15 |

## Queue (Next Up)
| Task | Priority | Subsystem | Blocked By |
|------|----------|-----------|------------|
| 514 | high | hooks-system | -- |
```

## Agent Lifecycle

Each swarm agent:
1. Receives a single task ID and the g-sprint skill context
2. Implements the task following acceptance criteria
3. Runs verification ladder (if configured on the task)
4. Updates task status on completion/failure
5. Removes its lockfile
6. Logs KPI metrics

## Git Workflow for Swarm Agents

| Blast Radius | Git Strategy |
|--------------|-------------|
| low | Direct commit to current branch |
| medium | Create feature branch, agent commits there |
| high | Create feature branch + draft PR for human review |

For medium/high: each agent uses `git worktree add` to avoid conflicts.

## Commands

- `@g-heartbeat swarm` — Start a swarm session
- `@g-heartbeat stop` — Signal all agents to finish current task, then stop
- `@g-heartbeat swarm-status` — Show current swarm status

## Safety Guardrails

- Max concurrent agents enforced by lock count
- Budget shared across all swarm agents
- Subsystem isolation prevents file conflicts
- TTL enforcement prevents runaway agents
- Crash recovery cleans up after failures
- Only `ai_safe: true` tasks are eligible for swarm execution
