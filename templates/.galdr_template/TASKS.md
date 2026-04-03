# {PROJECT_NAME} — Master Task List

**Project**: {project_name}
**Type**: delivery | research | maintenance | exploration  *(set during @g-setup)*
**Plan**: `PLAN.md`
**PRDs**: `prds/`
**Project overview**: `PROJECT.md`
**Constraints**: `CONSTRAINTS.md`
**Bugs**: `BUGS.md`
**Subsystems**: `SUBSYSTEMS.md`

---

## Status Indicators
- `[ ]` = Pending (no task file yet) — CODING BLOCKED
- `[📋]` = Task file created, ready to start
- `[📝]` = Spec being written (TTL: 1 hour)
- `[🔄]` = In Progress (claimed by agent, has TTL)
- `[🔍]` = Awaiting Verification (impl done, reviewer pending — different agent required)
- `[⏳]` = Resource-Gated (waiting on GPU/storage/API credits/external service)
- `[✅]` = Completed (verified by different agent)
- `[❌]` = Failed/Cancelled
- `[⏸️]` = Paused
- `[🌾]` = Harvested (done but approach superseded — preserved as reference)

---

## Task backlog (sequential IDs)

*v3 uses sequential task IDs in `tasks/task{id}_*.md`. Link PRDs from `PLAN.md`.*

### Subsystem: {subsystem-name-1}
- [ ] **Task 001**: {Task description} — {brief acceptance summary}
- [ ] **Task 002**: {Task description} — {brief acceptance summary}

### Subsystem: {subsystem-name-2}
- [ ] **Task 010**: {Task description}
- [ ] **Task 011**: {Task description}

---

## Bugs
*(See `BUGS.md` and individual files under `bugs/` for full detail.)*

---

## Completed Tasks
*(Tasks moved here when fully verified)*

---

## Harvested Tasks
*(Tasks that were completed but whose approach was superseded — preserved for reference)*

---

**Last Updated**: {YYYY-MM-DD}
**Open Tasks**: {n}
**Overall Progress**: {completed}/{total} tasks
