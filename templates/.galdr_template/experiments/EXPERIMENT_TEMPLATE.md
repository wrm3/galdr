---
id: EXP-{NNN}
title: '{Short experiment title}'
status: planned | running | completed | failed | abandoned
phase: {N}
hypothesis_ids: [HYP-NNN]    # Which hypotheses this experiment tests
experiment_type: proof_of_concept | comparison | parameter_sweep | ablation | baseline
started_date: ''
completed_date: ''
outcome: in_progress | validated | invalidated | inconclusive | superseded
carry_forward: []             # Findings to bring into next experiment
---

# Experiment {NNN}: {Title}

## Objective
{One sentence: What specific question does this experiment answer?}

**Hypothesis Being Tested**: {HYP-NNN} — {hypothesis statement one-liner}

---

## Prerequisites

### Environment
- [ ] {Environment requirement 1}
- [ ] {Environment requirement 2}

### Data
- [ ] {Dataset / data source 1} — source: {where to get it}
- [ ] {Dataset / data source 2}

### Resources
- **VRAM**: {X GB}
- **Storage**: {X GB}
- **Compute**: {estimate — e.g., "2h on RTX 4090"}
- **APIs / Credits**: {if any}

### Dependencies
- Depends on: {prior experiment or hypothesis ID}
- Blocks: {downstream experiments that need this result}

---

## Configuration

### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| {param_1} | {value} | {why this value} |
| {param_2} | {value} | {why this value} |

### Controlled Variables
*(What stays constant across runs)*
- {Variable 1}: {value held constant}

### Independent Variable
*(What we're changing/testing)*
- {Variable}: {range or options}

---

## Execution Steps

1. {Step 1 — specific command or action}
2. {Step 2}
3. {Step 3}

**Checkpoint**: After step {N}, verify {what to check} before continuing.

---

## Success Criteria

| Metric | Target | Minimum Acceptable |
|--------|--------|-------------------|
| {metric_1} | {target} | {floor} |
| {metric_2} | {target} | {floor} |

**Stop Early If**: {Condition that makes continuing pointless — e.g., "loss diverges after epoch 2"}

---

## Results
*(Filled in after execution)*

### Raw Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| {metric_1} | — | |

### Outcome: {validated | invalidated | inconclusive}
{2-4 sentences on what happened and why}

---

## Resource Log

| Stage | Duration | Cost (API/credits) | Notes |
|-------|----------|--------------------|-------|
| Setup | — | — | |
| Run 1 | — | — | |

**Total compute**: {hours}
**Total cost**: {USD if applicable}

---

## Carry Forward
*(If validated — what findings move to the next experiment)*

- {Finding 1: specific, actionable}
- {Finding 2}

---

## Archive / Lessons Learned
*(Always fill this in — even for failed experiments. This is the most valuable section.)*

**What Worked**:
- {Even partial successes worth noting}

**What Didn't Work**:
- {Specific failures and why}

**What We'd Do Differently**:
- {Recommendations for future attempts}

**Unexpected Findings**:
- {Anything surprising, even if not the original goal}
