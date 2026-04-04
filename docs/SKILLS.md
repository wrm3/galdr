# galdr Skills Reference

Skills are the engine behind every command and agent. Each skill owns a specific domain and provides detailed, step-by-step workflows.

## Naming Convention

All galdr skills use the `g-skl-{name}` folder prefix. The entry point is always `SKILL.md` inside that folder.

---

## Core galdr Skills (File-Centric Architecture)

Each skill "owns" specific `.galdr/` files. Only its owner skill should write to those files.

| Skill | Owns | Description |
|-------|------|-------------|
| `g-skl-tasks` | `TASKS.md`, `tasks/` | Task creation, status updates, sync check, complexity scoring, sprint planning |
| `g-skl-bugs` | `BUGS.md`, `bugs/` | Bug reporting, bug fixes, quality metrics |
| `g-skl-ideas` | `IDEA_BOARD.md` | Idea capture, review, promotion to tasks, proactive scanning |
| `g-skl-plan` | `PLAN.md`, `PRDS.md`, `prds/` | Plan creation, PRD writing, phase management |
| `g-skl-project` | `PROJECT.md`, `CONSTRAINTS.md` | Project identity, goals, architectural constraints |
| `g-skl-subsystems` | `SUBSYSTEMS.md`, `subsystems/` | Subsystem discovery, spec creation, activity logging, sync |
| `g-skl-medkit` | `.galdr/` (all files) | Health check, structural repair, version migration, routine maintenance |
| `g-skl-setup` | `.galdr/.identity` (initial) | First-time galdr initialization |

---

## Workflow Skills

| Skill | Description |
|-------|-------------|
| `g-skl-code-review` | Security, quality, performance review. Scales from quick scan to full architecture audit. |
| `g-skl-status` | Project status — session context, active tasks, goals, ideas |
| `g-skl-git-commit` | Well-structured commits following galdr conventions |
| `g-skl-swot-review` | Automated SWOT analysis for the current project phase |
| `g-skl-verify-ladder` | Multi-level verification gates for completed tasks |
| `g-skl-dependency-graph` | Generate and update task dependency graph |


---

*galdr slim ships 16 core skills. Additional domain skills (cross-project linking, video/3D, business/startup, IDE config) are available in galdr full.*
