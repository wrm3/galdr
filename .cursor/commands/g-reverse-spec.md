---
description: Analyze an external repository and produce a structured feature harvest report. Agents are reporters; humans are editors.
---
# /g-reverse-spec

Activates `g-skl-reverse-spec`. Analyzes any external repository and produces `research/harvests/{slug}/FEATURES.md` — no `.galdr/` writes until you run APPLY.

```
/g-reverse-spec ANALYZE https://github.com/user/repo
/g-reverse-spec RESUME user__repo
/g-reverse-spec APPLY user__repo
/g-reverse-spec APPLY --dry-run user__repo
/g-reverse-spec STATUS user__repo
```

**Passes**: Skeleton → Module Map → Feature Scan → Deep Dives → Synthesis

**Reporter rule**: Document everything. Never filter by "galdr already has this."
