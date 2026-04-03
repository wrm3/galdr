---
name: g-experiment
description: Scientific experiment lifecycle — create, run stages, check gates, generate autopsies, chain experiments. For research/ML projects with repeatable hypothesis testing.
---
# galdr-experiment

## When to Use
Managing scientific experiments with stage gates, hypothesis testing, and experiment chaining.
Triggered by `@g-experiment-new`, `@g-experiment-run`, `@g-experiment-status`, `@g-experiment-autopsy`,
or phrases like "run experiment", "check gate", "new experiment", "experiment chain".

**Not for galdr self-evolution** — that uses `SELF_EVOLUTION.md` owned by `g-self-improvement`.

## Key Files
- `.galdr/experiments/EXPERIMENTS.md` — master registry
- `.galdr/experiments/HYPOTHESIS.md` — hypothesis tracker
- `.galdr/experiments/EXPERIMENT_TEMPLATE.md` — stage-gate template
- `.galdr/experiments/EXP-NNN.md` — individual experiment files

## Workflow Overview

```
HYPOTHESIS.md ──> EXPERIMENTS.md ──> EXP-NNN.md (stages with gates)
                                         |
                                    TASKS.md (engineering work to support stages)
```

Tasks build code. Experiments run that code with different configurations.
Once code exists, experiments re-run it — the experiment file documents
what configuration to use; the task file documents how the code was built.

---

## g-experiment-new

Create a new experiment from template.

### Steps

1. **Read EXPERIMENTS.md** — get last EXP ID, increment
2. **Read HYPOTHESIS.md** — identify which hypothesis to test
3. **Check for chaining**: if user specifies a previous experiment:
   - Read the previous EXP file
   - Pre-fill `previous_experiment` and prompt for `change_from_previous`
   - Copy `carry_forward` findings from the previous experiment
4. **Copy EXPERIMENT_TEMPLATE.md** to `.galdr/experiments/EXP-NNN.md`
5. **Fill YAML frontmatter**: id, title, hypothesis_ids, experiment_type, previous_experiment, change_from_previous
6. **Add to EXPERIMENTS.md** Active table
7. **Update ID Registry** in EXPERIMENTS.md
8. **Update HYPOTHESIS.md**: set hypothesis status to `testing` with experiment reference

### Chaining Rules
- One variable per experiment — if you need to change two things, create two experiments
- Document the change in `change_from_previous` (single sentence)
- Carry forward validated findings from previous experiment

---

## g-experiment-run

Advance a stage of an active experiment.

### Steps

1. **Read experiment file** (EXP-NNN.md)
2. **Identify current stage** — find first stage with `[ ]` or `[🔄]` status
3. **Mark stage running**: change `[ ]` to `[🔄]`
4. **Execute or guide execution** of stage steps
5. **Check gate conditions**: evaluate each metric against target
6. **Gate decision**:
   - **ALL gates pass** → mark stage `[✅]`, proceed to next stage
   - **ANY gate fails** → mark stage `[❌]`, mark all subsequent stages `[⏭️]` (skipped)
7. **On failure**: trigger autopsy workflow (see g-experiment-autopsy)
8. **On final stage pass**: mark experiment `status: completed`, `outcome: validated|invalidated`
9. **Update EXPERIMENTS.md**: move to Completed or Failed table
10. **Update HYPOTHESIS.md**: set hypothesis to `validated` or `invalidated`

### Stage Status Indicators
| Indicator | Meaning |
|-----------|---------|
| `[ ]` | Not started |
| `[🔄]` | Running |
| `[✅]` | Passed gate |
| `[❌]` | Failed gate |
| `[⏭️]` | Skipped (prerequisite failed) |

### Gate Rules
1. Gates are mandatory — no stage proceeds without checking
2. Gates are binary — pass or fail, no "close enough"
3. Failed gates stop the experiment — do not proceed
4. Gate metrics must be measurable — no subjective assessments

---

## g-experiment-status

Show status of all active experiments.

### Steps

1. **Read EXPERIMENTS.md** — get active experiments list
2. **For each active experiment**: read EXP file, count stages, determine progress
3. **Display**:
```
EXPERIMENTS
Active: EXP-001 — {title} (Stage 3/6 ✅✅🔄[ ][ ][ ])
  Hypothesis: HYP-001 ({status})
  Next gate: Stage 3 — {name}
  Last updated: {date}

Planned: EXP-002 — {title} (not started)
  Chains from: EXP-001
  Change: {change_from_previous}
```
4. **Flag stale experiments**: any running >48h without stage update

---

## g-experiment-autopsy

Generate a structured failure autopsy for a failed stage.

### Steps

1. **Read experiment file** — find the failed stage (marked `[❌]`)
2. **Collect gate data**: expected vs actual for each metric
3. **Generate autopsy** in the experiment file:

```markdown
## Failure Autopsy

### Stage {N}: {Stage Name}
**What happened**: {Factual description}
**Root cause**: {Analysis}
**What the metrics showed**:
| Metric | Expected | Actual |
|--------|----------|--------|
| {metric} | {target} | {actual} |

**Suggested fix for next experiment**: {Recommendation}
**Suggested experiment change**: {Single variable to change in EXP-NNN+1}
**Confidence in fix**: High | Medium | Low
**Alternative approaches if fix fails**: {Backup plan}
```

4. **Update experiment status**: `status: failed`, `outcome: invalidated|inconclusive`
5. **Offer to chain**: "Create EXP-{NNN+1} with the suggested change?"

### Autopsy Rules
- Be specific — "loss diverged" is not enough; include epoch, batch, values
- Include data — metrics table with expected vs actual
- One suggested change — pick the most likely root cause
- Confidence level — be honest about whether the fix is a guess

---

## g-experiment-chain

Create EXP-N+1 from a failed or completed experiment.

### Steps

1. **Read source experiment** (EXP-N)
2. **Extract**: carry_forward findings, failure autopsy suggestion
3. **Run g-experiment-new** with:
   - `previous_experiment: EXP-N`
   - `change_from_previous: {from autopsy or user}`
   - `carry_forward: {validated findings from EXP-N}`
4. **Update EXPERIMENTS.md chain diagram**

---

## Registry Management

When creating/completing/failing experiments, always update:
1. `EXPERIMENTS.md` — move between Active/Completed/Failed tables
2. `HYPOTHESIS.md` — update hypothesis status
3. Experiment chain diagram in EXPERIMENTS.md

---

## Relationship to Tasks

- Experiment stages MAY reference tasks: "Requires Task 500 to be complete"
- Tasks MAY reference experiments: "Built for EXP-001 Stage 3"
- They are tracked in separate files — experiments are NOT tasks
- When a stage needs new code, create a task first, then run the stage
