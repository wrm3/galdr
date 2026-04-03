---
id: EXP-{NNN}
title: '{Short experiment title}'
status: planned | running | completed | failed | abandoned
hypothesis_ids: [HYP-NNN]
experiment_type: proof_of_concept | comparison | parameter_sweep | ablation | baseline
started_date: ''
completed_date: ''
outcome: in_progress | validated | invalidated | inconclusive | superseded
carry_forward: []
previous_experiment: null
change_from_previous: 'N/A — first experiment (or: single sentence describing the ONE variable changed)'
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

### Artifacts (Inputs)
- [ ] {Pre-trained model, embeddings, or other artifacts needed}

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
*(The ONLY thing that changes — one variable per experiment)*
- {Variable}: {range or options}

---

## Stages

### Stage 1: {Name}
**Goal**: {One sentence}

**Steps**:
1. {Specific action or command}
2. {Next action}

**Gate**:
| Metric | Target | Stop If |
|--------|--------|---------|
| {metric} | {target value} | {failure condition} |

**Pass condition**: {What must be true to proceed to Stage 2}
**Fail condition**: {What triggers a stop and failure autopsy}

---

### Stage 2: {Name}
**Goal**: {One sentence}

**Steps**:
1. {Step}

**Gate**:
| Metric | Target | Stop If |
|--------|--------|---------|
| {metric} | {target} | {failure condition} |

**Pass condition**: {criteria}
**Fail condition**: {criteria}

---

*(Add more stages as needed. Each stage MUST have a gate.)*

---

## Success Criteria (Overall)

| Metric | Target | Minimum Acceptable |
|--------|--------|-------------------|
| {metric_1} | {target} | {floor} |
| {metric_2} | {target} | {floor} |

**Stop Early If**: {Condition that makes continuing pointless}

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

| Stage | Duration | VRAM Peak | Notes |
|-------|----------|-----------|-------|
| 1. {name} | — | — | |
| 2. {name} | — | — | |

**Total compute**: —
**Total wall time**: —

---

## Failure Autopsy
*(Fill this in if ANY stage fails — do not skip)*

### Stage {N}: {Stage Name}
**What happened**: {Factual description of the failure}
**Root cause**: {Analysis — why did it fail?}
**What the metrics showed**:
| Metric | Expected | Actual |
|--------|----------|--------|
| {metric} | {target} | {actual value} |

**Suggested fix for next experiment**: {Actionable recommendation}
**Suggested experiment change**: {The single variable to change in EXP-NNN+1}
**Confidence in fix**: High | Medium | Low
**Alternative approaches if fix fails**: {Backup plan}

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
