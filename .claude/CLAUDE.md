# Claude Code — galdr System Instructions

@AGENTS.md

---

## Claude Code-Specific galdr Guidance

### Command Prefix
Use `/g-` prefix for all galdr commands:
- `/g-setup` — initialize galdr
- `/g-task-new` — create a task
- `/g-status` — project overview
- `/g-medkit` — health check and repair

See `docs/COMMANDS.md` for the full command list.

### Rules
Rules live in `.claude/rules/g-rl-*.md`. They load at every session. Do not edit them unless updating the galdr system itself.

### Agents
Invoke specialized agents with `@agent-name` syntax:
- `@g-agnt-task-manager` — task lifecycle
- `@g-agnt-qa-engineer` — bug tracking
- `@g-agnt-code-reviewer` — code review
- `@g-agnt-project` — planning and PRDs

### Hooks
Claude Code hooks live in `.claude/hooks/`. They fire on session start, agent complete, and before shell execution. Do not edit hook files unless updating the galdr system.

### Skills
Skills are in `.claude/skills/g-skl-*/SKILL.md`. Invoke them by mentioning their purpose — Claude discovers and loads them automatically.

### Multi-Agent Sessions
When multiple agents are working simultaneously:
- Skip tasks marked `[🔄]` (in-progress) — they are claimed
- `[🔄]` older than **2 hours** without a `status_changed` update is stale and available for pickup
- Always write `status_changed` timestamp to the task file when claiming a task

### Rate Limit Graceful Shutdown
At ~85% daily rate limit, stop accepting new tasks and produce a handoff report:
```
## Shutdown — Rate Limit Approaching
### Completed This Session: [tasks]
### Left In-Progress: [task ID, what was done, what remains]
### Files Modified: [list]
### Git Status: [committed/uncommitted]
```
