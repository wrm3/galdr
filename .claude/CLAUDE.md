# Claude Code — galdr System Instructions

@AGENTS.md

---

## Claude Code-Specific galdr Guidance

### Command Prefix
Use `/g-` for all galdr commands. See `docs/COMMANDS.md` for the full reference.

| Command | Description |
|---------|-------------|
| `/g-setup` | Initialize galdr in this project |
| `/g-status` | Project status overview |
| `/g-task-new` | Create a new task |
| `/g-task-update` | Update task status |
| `/g-task-sync-check` | Validate task sync |
| `/g-workflow` | Task expansion and sprint planning |
| `/g-bug-report` | Report a bug |
| `/g-bug-fix` | Document a bug fix |
| `/g-qa` | Quality assurance activation |
| `/g-code-review` | Comprehensive code review |
| `/g-plan` | Create or update project plan |
| `/g-sprint` | Run a 2-hour autonomous sprint |
| `/g-go` | Run backlog autonomously |
| `/g-git-commit` | Structured git commit |
| `/g-idea-capture` | Capture an idea |
| `/g-idea-review` | Review and promote ideas |
| `/g-medkit` | Health check and repair `.galdr/` |
| `/g-swot-review` | SWOT analysis |
| `/g-dependency-graph` | Generate task dependency graph |
| `/g-report` | Project report |
| `/g-goal-update` | Update project goals |

### Agents
Invoke specialized agents with `@agent-name` syntax:

| Agent | Purpose |
|-------|---------|
| `@g-agnt-task-manager` | Task lifecycle — create, update, complete |
| `@g-agnt-project` | PRD writing, planning, PROJECT.md, CONSTRAINTS.md |
| `@g-agnt-qa-engineer` | Bug tracking and quality assurance |
| `@g-agnt-code-reviewer` | Code quality and security review |
| `@g-agnt-infrastructure` | File organization, scope boundaries, SUBSYSTEMS.md |
| `@g-agnt-ideas-goals` | Idea capture, IDEA_BOARD.md, goal management |
| `@g-agnt-verifier` | Verify completed task work |
| `@g-agnt-project-initializer` | First-time galdr project setup |

### Rules
Rules live in `.claude/rules/g-rl-*.md` and load at every session. Do not edit them unless updating the galdr system itself.

### Skills
Skills are in `.claude/skills/g-skl-*/SKILL.md`. They load when you invoke a command or when Claude determines they're relevant. All 17 core galdr skills are present.

### Hooks
Claude Code hooks live in `.claude/hooks/`. They fire on session start, agent complete, and before shell execution. Session start injects `.galdr/` context and `GUARDRAILS.md`.

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
