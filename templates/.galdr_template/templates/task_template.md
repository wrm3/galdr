# Task Template (vNext)

This is the canonical single-task file template for galdr vNext. Copy this file, rename it to
`task{NNN}_descriptive_name.md` (or `task{NNN}-{sub}_descriptive_name.md` for subtasks), and
fill in every required field before starting work.

---

## Status Progression

```
                                    Happy Path
[ ] --> [📝] --> [📋] --> [🔄] --> [🔍] --> [✅]
 ^       ^        ^        ^        ^        ^
 |       |        |        |        |        Completed (verified by different agent)
 |       |        |        |        Awaiting verification (different agent required)
 |       |        |        In-progress (agent claimed, has TTL)
 |       |        Spec written, task file exists, ready to implement
 |       Spec being written (TTL: 1 hour)
 Listed in TASKS.md only — NO file yet, BLOCKED

                                    Branching Statuses
                         [🔄] --> [⏸️]  Paused (deprioritized, checkpoint preserved)
                         [🔄] --> [❌]  Failed (max retries or permanently blocked)
                         [📋] --> [⏳]  Resource-Gated (waiting on GPU/API/credential/human)
                         [🔍] --> [📋]  Verification failed — reset to ready
                         [✅] --> [🌾]  Harvested (approach superseded, preserved as reference)
```

| Indicator | YAML Status | Meaning |
|-----------|-------------|---------|
| `[ ]` | *(no file)* | Listed in TASKS.md only — coding blocked, do not start |
| `[📝]` | `speccing` | Agent writing the spec (TTL: 1 hour) |
| `[📋]` | `pending` | Task file created, ready to implement |
| `[🔄]` | `in-progress` | Agent actively working (claimed, has TTL) |
| `[🔍]` | `awaiting-verification` | Implementation done, reviewer pending |
| `[⏳]` | `resource-gated` | Waiting on external resource (GPU, API key, credential, human) |
| `[✅]` | `completed` | Done and verified |
| `[❌]` | `failed` | Blocked permanently or abandoned after max retries |
| `[⏸️]` | `paused` | Deprioritized mid-work, preserves checkpoint state |
| `[🌾]` | `harvested` | Task body reused as input for different task; original archived |

---

## Required vs Optional Fields

**Required (must be set before `[🔄]`):**
`id`, `title`, `type`, `status`, `priority`, `phase`, `subsystem`, `concern`,
`ai_safe`, `blast_radius`, `requires_verification`, `project_context`

**Required on completion:**
`completed_date`, `rules_version`, `actual_files_changed`
If `requires_verification: true` — also `verified_by`, `verified_date`, `evidence_of_completion`

**Auto-computed (agent fills, not human):**
`claim_expires_at` (= `claimed_at` + `claim_ttl_minutes`),
`claim_ttl_minutes` (= `estimated_duration_minutes` * 1.5)

**Optional / situational:**
`milestone`, `requires_solo_agent`, `blast_radius_reason`, `spec_dependencies`,
`failure_history`, `execution_progress`, `execution_cost`, `tags`

---

## spec_dependencies Format

`spec_dependencies` lists other task IDs whose spec sections this task's implementation depends on.
This is distinct from `dependencies` (execution order). Use it when your implementation
must be consistent with decisions made in another task's spec, even if that task runs in parallel.

```yaml
spec_dependencies:
  - 42          # Must read task042's "Implementation Notes" before writing code
  - INFRA-007   # Must align with infrastructure task INFRA-007 API contract
```

---

## failure_history Entry Format

Each entry records one failed attempt. Append; never delete.

```yaml
failure_history:
  - attempt: 1
    failed_at: "2026-03-05T14:22:00Z"
    agent_id: "cursor-agent-A"
    reason: "Dependency service was down; migration script could not connect to DB"
    error_snippet: "ConnectionRefusedError: [Errno 111] Connection refused"
    resolution_tried: "Retried 3 times with 30s backoff, all failed"
    escalated: false
```

---

## Template

```yaml
---
# =============================================================================
# === IDENTITY ===
# =============================================================================

id: {number or SUBSYSTEM-NNN}
# Numeric (e.g., 42) for standard tasks; namespaced (e.g., INFRA-007) for
# subsystem-scoped tasks. Subtask format: {parent}-{sub} (e.g., 42-1).

title: 'Task Title'
# Concise, action-oriented. Start with a verb. Max ~80 chars.

type: feature | bug_fix | refactor | documentation | research | retroactive_fix
# feature       — new capability
# bug_fix        — corrects defective behavior; link BUG-NNN in project_context
# refactor       — structural improvement, no behavior change
# documentation  — docs-only change
# research       — investigation/spike; output is a decision or design doc
# retroactive_fix — documents work already completed in chat (use sparingly)

status: pending | in-progress | awaiting-verification | completed | failed | harvested | paused | resource-gated
# See status progression at top of this file.

# =============================================================================
# === PRIORITY & PHASE ===
# =============================================================================

priority: critical | high | medium | low
# critical — blocks release or causes data loss; drop everything
# high     — important, address in current sprint
# medium   — normal priority
# low      — nice-to-have, defer if needed

phase: 0
# Numeric phase this task belongs to. Phase 0 = setup/infrastructure (IDs 1-99),
# Phase 1 = foundation (100-199), Phase N = N*100 to N*100+99.

subsystem: subsystem-name
# Primary subsystem identifier (stable, not temporal). Matches an entry in
# SUBSYSTEMS.md. One value only; use tags for secondary systems.

milestone: milestone-name
# Optional. Delivery target label (e.g., "beta-launch", "v2.0"). Temporal;
# milestones come and go but subsystems are stable. Omit if not applicable.

concern: feature | bug | refactor | experiment | maintenance
# Cross-cutting concern category. Complements `type` for filtering and metrics.
# feature     — adds user-visible value
# bug         — corrects wrong behavior
# refactor    — internal quality improvement
# experiment  — exploratory; may be discarded
# maintenance — keep-the-lights-on work (deps updates, housekeeping)

# =============================================================================
# === AUTONOMY FLAGS ===
# =============================================================================

ai_safe: true | false
# true  — agent may execute this task unattended without human checkpoint
# false — requires human review at at least one step; agent must pause and report

requires_solo_agent: true | false
# true  — no other agent may claim tasks in the same subsystem simultaneously.
# false — parallel agents are allowed (default).
# Set true for tasks that rewrite shared interfaces or perform destructive migrations.

blast_radius: low | medium | high
# Estimated scope of potential breakage if this task goes wrong.
# low    — isolated to one file or one module
# medium — touches multiple files; possible regression in adjacent modules
# high   — cross-subsystem impact; could break unrelated features

blast_radius_reason: "Why this blast radius"
# Required when blast_radius is medium or high. One sentence explaining the risk.

affected_files_estimate: 3
# Agent's best-guess count of files that will be modified. Set before starting.
# Used for retrospective calibration.

actual_files_changed: null
# Exact count filled in by the implementing agent on completion.

# =============================================================================
# === CLAIM / TTL (Resilience) ===
# =============================================================================

claimed_by: null
# Agent ID string that claimed this task (e.g., "cursor-agent-B", "claude-code-1").
# Null = available for pickup.

claimed_at: null
# ISO-8601 timestamp of when the claim was made (e.g., "2026-03-05T14:00:00Z").
# Null = unclaimed.

estimated_duration_minutes: 60
# Agent's time estimate before starting. Used to compute claim_ttl_minutes.

claim_ttl_minutes: 90
# Auto-computed: estimated_duration_minutes * 1.5. After this duration has
# elapsed since claimed_at, any agent may treat this task as abandoned and
# reclaim it. Update if significant scope change occurs mid-task.

claim_expires_at: null
# Auto-computed: claimed_at + claim_ttl_minutes (ISO-8601).
# Set by agent when claiming. Any agent may reclaim after this timestamp.

last_heartbeat: null
# ISO-8601 timestamp. Updated by the implementing agent every 15 minutes on
# long-running tasks to prove the claim is still alive. If last_heartbeat is
# older than claim_ttl_minutes and task is still in-progress, treat as stale.

# =============================================================================
# === VERIFICATION ===
# =============================================================================

requires_verification: true
# Default true for all tasks that produce code or configuration changes.
# Set false only for documentation-only or research tasks where verification
# is impractical (must add comment explaining why).

verified_by: null
# Agent ID of the verifier. MUST be different from claimed_by.
# The implementing agent may not self-verify.

verified_date: null
# ISO-8601 date when verification was completed (e.g., "2026-03-05").

evidence_of_completion:
  type: null
  # One of: test_output | compile_log | runtime_log | manual_check
  # test_output  — passing test suite output captured to log file
  # compile_log  — clean build log with no errors
  # runtime_log  — application started and responded correctly
  # manual_check — human or agent stepped through acceptance criteria manually

  path: null
  # Relative path to evidence file (e.g., ".galdr/logs/task042_evidence.log").
  # Required when type is test_output, compile_log, or runtime_log.

# =============================================================================
# === SPEC MANAGEMENT ===
# =============================================================================

spec_version: 1
# Increment when the Implementation Notes section changes substantially enough
# that an agent mid-execution should re-read the spec before continuing.

spec_last_verified: "YYYY-MM-DD"
# Date the spec was last reviewed and confirmed still accurate. An agent starting
# this task more than 30 days after spec_last_verified should validate it first.

allow_spec_update: true
# If true, the implementing agent may update Implementation Notes if the planned
# approach is discovered to be incorrect or outdated — and must increment
# spec_version when doing so.
# If false, spec is locked; agent must escalate rather than modify.

spec_dependencies: []
# List of task IDs whose spec sections must be read before implementing this task.
# See "spec_dependencies Format" section above for detail and examples.

# =============================================================================
# === FAILURE HISTORY ===
# =============================================================================

failure_history: []
# Append an entry for each failed attempt. Never delete entries.
# See "failure_history Entry Format" section above for the entry schema.
# When failure_history length reaches 3, task must be escalated to human review
# before another attempt is made.

# =============================================================================
# === PROGRESS CHECKPOINTING ===
# =============================================================================

execution_progress:
  last_checkpoint: null
  # Short label for what step was last completed (e.g., "schema created").

  checkpoint_date: null
  # ISO-8601 datetime of the last checkpoint update.

  completed_steps: []
  # Ordered list of steps that have been finished. Populated by agent.
  # Example: ["Created DB migration", "Wrote service layer"]

  remaining_steps: []
  # Ordered list of steps not yet started. Populated from Implementation Notes
  # when task is first claimed. Kept current as steps complete.

  checkpoint_note: null
  # Free-text note for a paused task. Explains what was done, what state things
  # were left in, and what the next agent needs to know to resume safely.

# =============================================================================
# === COST TRACKING ===
# =============================================================================

execution_cost:
  model_used: null
  # Model ID used for implementation (e.g., "claude-sonnet-4-6", "gpt-4o").

  input_tokens: null
  # Total input tokens consumed across all agent turns for this task.

  output_tokens: null
  # Total output tokens generated across all agent turns for this task.

  estimated_cost_usd: null
  # Computed cost of implementation in USD (input + output token cost).

  review_cost_usd: null
  # Cost of the verification/review pass if done by a separate agent call.

  total_cost_usd: null
  # estimated_cost_usd + review_cost_usd

# =============================================================================
# === STANDARD FIELDS ===
# =============================================================================

project_context: "How this task connects to project goals"
# One or two sentences. Reference a goal ID from PROJECT_GOALS.md if applicable
# (e.g., "Supports G-01: reduce onboarding time by enabling SSO login").

dependencies: []
# Task IDs that MUST be in [✅] status before this task may start.
# Example: [10, 23, 42-2]
# Do not list spec_dependencies here; those are read-only references, not blockers.

tags: []
# Freeform labels for filtering and search. Examples: [auth, perf, frontend, api-contract]

created_date: "YYYY-MM-DD"
# Date this task file was created.

completed_date: null
# Date this task reached [✅] status. Filled atomically with status: completed.

rules_version: null
# the galdr rules version in effect when this task was completed.
# Example: "5.0.0". Helps diagnose behavior drift across long-lived projects.
---
```

---

# Task {id}: {Title}

## Objective

{One to three sentences. State exactly what must be true when this task is done.
Start with an action verb. Be specific enough that a different agent, reading only
this section, could determine whether the task succeeded.}

## Context

{Why does this task exist? What problem does it solve? What breaks or stays broken
if this task is skipped? Provide any background a new agent needs to understand
the decision to create this task. Reference relevant task IDs, bug IDs, or PRD
sections by number.}

## Acceptance Criteria

- [ ] {Verifiable outcome 1 — must be provable without asking the implementer}
- [ ] {Verifiable outcome 2}
- [ ] {Verifiable outcome 3}
- [ ] All existing tests continue to pass (no regressions)
- [ ] Evidence file created at `.galdr/logs/task{id}_evidence.log`

## Implementation Notes

{Technical approach. Describe the plan clearly enough that an agent can execute it
without needing to ask clarifying questions. Include:
- File(s) to create or modify
- Key functions, classes, or endpoints involved
- Libraries or patterns to use
- Known constraints (e.g., must not change public API, must stay under N lines)
- Data flow or sequence if non-obvious

If the approach later proves incorrect, update this section and increment spec_version.}

## Verification

{What the reviewer (a different agent or human) should check independently of the
implementer. This section drives the evidence_of_completion.

Examples:
- Run `{test command}` and confirm all {N} tests pass
- Start the application and hit `{endpoint}` — expect HTTP 200 with `{field}` in response
- Open `{file}` and confirm `{function}` does not contain `{anti-pattern}`
- Review migration file — confirm rollback path exists and is tested}

## When Stuck

**If `{specific error or symptom}`:**
{Diagnostic step — what to check first, what log to read, what to verify}

**If `{second specific failure mode}`:**
{Alternative diagnostic approach}

**If the planned approach fails after 2 attempts:**
{Describe the fallback approach — a simpler or more conservative implementation
that still satisfies the acceptance criteria, even if not ideal}

**Escalation trigger:**
Escalate to human review if any of the following occur:
- Three consecutive failed attempts (failure_history length >= 3)
- A required external dependency (API, service, credential) is unavailable
- The task would require modifying files outside this task's declared subsystem
- Acceptance criteria cannot be met without changing the spec

**Safe to skip if:**
{Conditions under which this task can be deferred without blocking downstream work.
Example: "Safe to skip if milestone is alpha; required before beta."
If the task can never be skipped, write: "Not deferrable — blocks tasks: {list}."}
