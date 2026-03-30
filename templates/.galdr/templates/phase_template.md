---
phase: {N}
name: '{Phase Name}'
purpose: milestone | experiment | domain | maintenance

# --- DELIVERY PROJECT FIELDS ---
# purpose: milestone
# milestone_name: '{Short name for this milestone — e.g., "Alpha Release"}'
# status: planning|in_progress|completed|cancelled|paused

# --- RESEARCH PROJECT FIELDS ---
# purpose: experiment
# experiment_type: proof_of_concept | comparison | parameter_sweep | ablation | baseline
# hypothesis: '{One sentence: "We believe that X will Y because Z"}'
# outcome: validated | invalidated | inconclusive | superseded | in_progress
# lessons_learned: ''

# --- SHARED FIELDS ---
subsystems: []          # Which subsystems this phase touches
task_range: '{N*100}-{N*100+99}'
prerequisites: []       # Phase numbers that must complete first
started_date: ''
completed_date: ''
pivoted_from: null      # Phase number if this is a pivot
pivot_reason: ''
---

# Phase {N}: {Phase Name}

## Overview
{Brief description of the phase goals and scope — 2-4 sentences}

## Objectives
- {Objective 1}
- {Objective 2}

## Deliverables
- [ ] {Deliverable 1}
- [ ] {Deliverable 2}

## Acceptance Criteria
- [ ] {Criterion 1: specific, measurable, verifiable}
- [ ] {Criterion 2: specific, measurable, verifiable}

---

<!-- DELIVERY PHASES: use Milestone section below -->
<!--
## Milestone: {milestone_name}

**Target Date**: YYYY-MM-DD
**Definition of Done**:
- All acceptance criteria above are met
- Code reviewed by a different agent
- No open blockers in subsystems: {list}
- Handoff document in docs/ if needed
-->

---

<!-- RESEARCH PHASES: use Experiment section below -->
<!--
## Experiment Details

**Hypothesis**: {Same as YAML}
**Experiment Type**: {Same as YAML}

### Setup / Prerequisites
- {Data required}
- {Hardware / resource requirements}
- {Environment setup}

### Configuration
- {Key parameter 1}: {value}
- {Key parameter 2}: {value}

### Success Metric
- {Metric}: {target value} — measured by {method}

### Failure Conditions
- {What constitutes a clear failure — stop early if this happens}

### Results
*(Filled in after completion)*

**Outcome**: validated | invalidated | inconclusive
**Summary**: {2-4 sentences on what happened}

### Carry Forward
*(If validated — what to bring into the next experiment)*
- {Finding 1}

### Archive
*(If invalidated or superseded — what to preserve for context)*
- {Context note 1}
-->

---

## Notes
{Architecture decisions, risks, technical debt, constraints — free-form}
