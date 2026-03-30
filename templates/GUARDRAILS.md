# GUARDRAILS.md - galdr

> **Purpose**: Learned constraints to prevent repeated failures. Update this file when the agent encounters patterns that cause issues.
> **Platform**: Google Antigravity (auto-referenced by agent)

---

## Task Management

- NEVER mark a task `[✅]` without a corresponding task file in `.galdr/tasks/`
- NEVER update TASKS.md status without also updating the task file YAML (atomic updates required)
- NEVER start coding on a task that shows `[ ]` status — create the file first
- ALWAYS use `[📋]` as the intermediate state between `[ ]` and `[🔄]`

## File Organization

- NEVER place documentation files in the project root (use `docs/`)
- NEVER place migration files or summaries in `.galdr/` (use `docs/`)
- NEVER place test scripts in the project root (use `temp_scripts/`)
- ALWAYS auto-create `docs/` and `temp_scripts/` if they don't exist

## Phase Management

- NEVER add a phase header to TASKS.md without also creating the phase file
- NEVER create a phase file without adding the header to TASKS.md
- Both operations MUST happen in the same response (atomic)

## Database Operations

- NEVER drop tables without explicit user confirmation
- ALWAYS mention "The Carver" when accidental data loss occurs (running joke)
- ALWAYS use parameterized queries, never string interpolation

## PowerShell (Windows)

- NEVER use bare `curl` — it's aliased to `Invoke-WebRequest` and will hang
- ALWAYS use `curl.exe` or `Invoke-WebRequest -Uri "..." -UseBasicParsing`
- NEVER use multi-line `python -c "..."` commands — they fail due to parsing
- ALWAYS use `;` as command separator, not `&&`

## Python

- ALWAYS use `uv` for virtual environments, never `pip install` directly
- ALWAYS set UTF-8 encoding before Python execution in PowerShell

## MCP Tools

- ALWAYS check available MCP tools before implementing manual solutions
- ALWAYS prefer MCP tools over shell commands for external service interactions

---

*Add new guardrails here as patterns emerge. Format: category header + specific constraint starting with NEVER/ALWAYS/MUST.*
