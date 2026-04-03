---
description: "Post-run KPI tracking — view reports, record observations, check anomalies"
---

# g-kpi

Track and analyze agent performance metrics.

## Usage

- `@g-kpi report <routine>` — Show trend summary for a routine
- `@g-kpi observe <routine> "<observation>"` — Record a human observation
- `@g-kpi baselines` — Recalculate all baselines
- `@g-kpi anomalies` — List recent anomalies

## Behavior

1. Read the `g-kpi` skill at `.cursor/skills/g-kpi/SKILL.md`
2. For `report`: run `python .cursor/skills/g-kpi/scripts/kpi_capture.py report <routine>`
3. For `observe`: run `python .cursor/skills/g-kpi/scripts/kpi_capture.py observe <routine> "<text>"`
4. For `baselines`: run `python .cursor/skills/g-kpi/scripts/kpi_capture.py baselines`
5. For `anomalies`: run `python .cursor/skills/g-kpi/scripts/kpi_capture.py anomalies`
