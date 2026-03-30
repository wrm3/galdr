# Claude Code Project Rules

Detailed rules are in `.claude/rules/`. This file contains Claude Code-specific operational rules not covered there.

---

## Rate Limit Graceful Shutdown (CRITICAL)

**At ~85% daily rate limit usage, STOP accepting new tasks and wind down gracefully.**

1. **No New Tasks**: Finish only what is actively in-progress
2. **Wrap Up**: Complete in-progress edits, update TASKS.md atomically, stage completed work
3. **Handoff Report** before stopping:
   ```
   ## Graceful Shutdown - Rate Limit Approaching
   ### Completed This Session: [tasks with status]
   ### Left In-Progress: [task ID, what was done, what remains, files touched]
   ### Not Started: [task IDs planned but not begun]
   ### Files Modified: [all files changed]
   ### Git Status: [committed/uncommitted]
   ```
4. Clearly state you're stopping due to rate limits

**WHY**: Other AIs (Cursor, Gemini) coordinate with this agent. Clean shutdown prevents sync issues.

---

## Multi-Agent Concurrency (TTL-Based Locking)

Multiple AI agents may work the task backlog simultaneously. To prevent duplicate work:

**When picking up a task:**
1. Skip any task marked `[📝]` or `[🔄]` in TASKS.md
2. Picking a `[ ]` task to spec → immediately mark `[📝]`
3. Picking a `[📋]` task to code → immediately mark `[🔄]`
4. Write `status_changed` timestamp in task file YAML

**Stale task recovery (TTL expiry):**
- `[📝]` older than **1 hour** → abandoned spec, treat as `[ ]`
- `[🔄]` older than **2 hours** → abandoned coding, treat as `[📋]`
- No `status_changed` timestamp → assume stale, available for pickup

This is self-healing: dead/rate-limited agents don't create permanent locks.

---

## This Project's Default Stack
- **Backend**: FastAPI + PostgreSQL + Redis
- **Frontend**: React + TypeScript + Tailwind + Vite
- **Desktop**: Electron
- **Voice**: Edge-TTS + Whisper
