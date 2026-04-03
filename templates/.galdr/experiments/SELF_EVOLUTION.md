# SELF_EVOLUTION.md
## galdr Self-Evolution Log

This file tracks self-evolution changes made to the galdr system itself —
rule modifications, workflow changes, template updates, and AI-initiated
improvements. It prevents re-proposing rejected ideas and captures lessons
for future AI sessions.

**Note**: This is for galdr *system-level* evolution only. For scientific/research
experiments (ML training, A/B tests, parameter sweeps), use `EXPERIMENTS.md`
and the `@g-experiment-new` command.

**Scope**: System-level changes only. Feature work goes in TASKS.md.
**Updated By**: Cleanup agent (nightly) + human + AI during sessions

---

## Active Experiments

<!-- Experiments currently being monitored. Cleanup agent moves to Completed after outcome is clear. -->

<!--
### EXP-001: [Experiment Title]
**Status**: monitoring
**Started**: YYYY-MM-DD
**Proposed By**: human | AI | {agent_id}
**Hypothesis**: [What we expect this change to improve]
**Change Made**: [What was actually changed — file, rule, template]
**Monitoring**: [How we'll know if it worked — metric, observation, timeframe]
**experiment_result**:
  outcome: (leave blank until closing)
  measured_by: []
  task_failure_rate_before: null
  task_failure_rate_after: null
  notes: ""
  closed_date: null
-->

*(No active experiments yet)*

---

## Completed Experiments

<!-- Experiments with known outcomes. -->

<!--
### EXP-000: [Completed Example]
**Status**: success | failed | partial
**Completed**: YYYY-MM-DD
**Proposed By**: human
**Hypothesis**: [Original hypothesis]
**Change Made**: [What was changed]
**Outcome**: [What actually happened]
**Lessons Learned**: [What future sessions should know]
**Reference**: [task or commit reference]
**experiment_result**:
  outcome: success | failed | partial | abandoned
  measured_by: [metric or observation used to evaluate]
  task_failure_rate_before: null
  task_failure_rate_after: null
  notes: "what actually happened in practice"
  closed_date: YYYY-MM-DD
-->

*(No completed experiments yet)*

---

## Rejected Ideas

<!-- Ideas consciously decided not to pursue. AI checks this before re-proposing. -->

<!--
### REJ-001: [Rejected Idea Title]
**Date**: YYYY-MM-DD
**Proposed By**: AI | human
**Summary**: [What was proposed]
**Why Rejected**: [Reason — too complex, not needed, conflicts with X, user declined]
**Do Not Re-Propose**: true
-->

*(No rejected ideas yet)*

---

## Experiment ID Registry
Last EXP ID: EXP-000
Last REJ ID: REJ-000
