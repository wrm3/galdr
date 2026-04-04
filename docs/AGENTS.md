# galdr Agents Reference

galdr includes specialized agents for different development roles. All galdr system agents use the `g-agnt-` prefix. Development persona agents use their role name directly.

## galdr System Agents

These agents are the core of the galdr system. Activate them explicitly for structured workflows.

| Agent | File | Description | Best For |
|-------|------|-------------|----------|
| Agent | File | Description | Best For |
|-------|------|-------------|----------|
| `g-agnt-task-manager` | `g-agnt-task-manager.md` | Task lifecycle management | Creating, updating, completing tasks |
| `g-agnt-project` | `g-agnt-project.md` | Project init, grooming, planning, PRDs | Project planning, PRD creation |
| `g-agnt-qa-engineer` | `g-agnt-qa-engineer.md` | Bug tracking, quality assurance | Bug reports, QA workflows |
| `g-agnt-code-reviewer` | `g-agnt-code-reviewer.md` | Code quality and security review | Pull request review, audits |
| `g-agnt-infrastructure` | `g-agnt-infrastructure.md` | Project structure, scope | File organization, boundaries |
| `g-agnt-ideas-goals` | `g-agnt-ideas-goals.md` | Idea capture and goal management | Brainstorming, goal setting |
| `g-agnt-verifier` | `g-agnt-verifier.md` | Task verification | Checking completed work |
| `g-agnt-project-initializer` | `g-agnt-project-initializer.md` | New project setup | First-time galdr install |

## Development Persona Agents

These agents adopt development roles. Use them for actual coding work.

### Core Development

| Agent | Description | Best For |
|-------|-------------|----------|
| `backend-developer` | API design, server logic, database integration | Backend APIs, business logic |
| `frontend-developer` | React, TypeScript, UI components | User interfaces, responsive design |
| `full-stack-developer` | End-to-end implementation | Complete features |
| `api-designer` | REST/GraphQL API design | API contracts |
| `solution-architect` | System architecture, tech selection | Architectural decisions |

### Quality & Testing

| Agent | Description | Best For |
|-------|-------------|----------|
| `qa-engineer` | Test planning, quality metrics | Quality assurance |
| `code-reviewer` | Code quality, best practices | Code reviews |

### AI & ML

| Agent | Description | Best For |
|-------|-------------|----------|
| `ai-model-developer` | AI/ML model development | Model creation |
| `ai-model-trainer` | Model training and fine-tuning | Training pipelines |
| `mlops-engineer` | ML operations and deployment | ML infrastructure |

### IDE & Config

| Agent | Description | Best For |
|-------|-------------|----------|
| `claude-cli` | Claude CLI operations | Claude Code automation |
| `cursor-cli` | Cursor CLI operations | Cursor IDE automation |
| `claude-config-maintainer` | .claude/ config management | Claude project setup |
| `cursor-config-maintainer` | .cursor/ config management | Cursor project setup |

### Specialized

| Agent | Description | Best For |
|-------|-------------|----------|
| `orchestrator` | Multi-agent coordination | Complex multi-agent tasks |
| `agent-creator` | Create new agent definitions | Meta/system |
| `skill-creator` | Create new skill definitions | Meta/system |
| `codebase-analyst` | Deep merge your own projects | Project integration |
| `harvest-analyst` | Harvest ideas from external sources | Selective improvements |

---

## Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| galdr system agents | `g-agnt-{name}.md` | `g-agnt-task-manager.md` |
| Skills | `g-skl-{name}/SKILL.md` | `g-skl-code-review/SKILL.md` |
| Commands (Cursor/Claude/OpenCode) | `g-{name}.md` | `g-code-review.md` |
| Workflows (Gemini `.agent/workflows/`) | `g-wkflw-{name}.md` | `g-wkflw-code-review.md` |
| Rules | `g-rl-{nnn}-{name}.mdc` | `g-rl-00-always.mdc` |
| Hooks | `g-hk-{name}.ps1` | `g-hk-session-start.ps1` |

> **Note**: Development persona agents (backend-developer, frontend-developer, etc.) do not use the `g-agnt-` prefix — they are role identities, not galdr system components.
