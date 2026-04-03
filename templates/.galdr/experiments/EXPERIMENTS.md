# Experiment Registry — {project_name}

## Active Experiments

| ID | Title | Hypothesis | Status | Outcome | Started | Completed |
|----|-------|-----------|--------|---------|---------|-----------|
| *(none yet)* | | | | | | |

## Completed Experiments

| ID | Title | Hypothesis | Outcome | Key Finding |
|----|-------|-----------|---------|-------------|
| *(none yet)* | | | | |

## Failed / Abandoned Experiments

| ID | Title | Hypothesis | Outcome | Failure Reason |
|----|-------|-----------|---------|----------------|
| *(none yet)* | | | | |

## Experiment Chain

```
(No experiments yet — chains will be documented here as experiments are created)
```

## Naming Convention

- **EXP-NNN**: Sequential experiment number
- **File**: `.galdr/experiments/EXP-NNN.md`
- **Template**: `.galdr/experiments/EXPERIMENT_TEMPLATE.md`
- **Hypotheses**: `.galdr/experiments/HYPOTHESIS.md`
- **Self-evolution**: `.galdr/experiments/SELF_EVOLUTION.md` (galdr system changes only)

## Rules

1. Each experiment tests ONE hypothesis (or one variable change from the previous experiment)
2. Experiments are SEQUENTIAL — EXP-002 builds on EXP-001's results
3. The `change_from_previous` field in YAML frontmatter documents the single variable changed
4. Failed experiments get a **Failure Autopsy** section before the next experiment is designed
5. Engineering work (new code, infrastructure) goes in `TASKS.md` — experiments go here
6. Every stage has a **gate** — pass/fail conditions checked before proceeding

## ID Registry
Last Experiment ID: EXP-000
