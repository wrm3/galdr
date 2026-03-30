---
description: Documentation file placement and naming standards
globs:
alwaysApply: true
---

# Documentation Standards

## CRITICAL: No .md Files in Project Root

**All documentation files MUST go in `docs/` folder, NOT in project root.**

### Naming Convention

**Format:** `YYYYMMDD_HHMMSS_IDE_TOPIC_NAME.md`

**Example for Claude Code:**
```
✅ docs/20251019_173407_Claude_CODE_REVIEW_ANALYSIS.md
✅ docs/20251019_143022_Claude_FEATURE_PLANNING.md
✅ docs/20251020_094523_Claude_DATABASE_DESIGN.md

❌ CODE_REVIEW_ANALYSIS.md  (wrong location)
❌ docs/code-review.md  (missing timestamp and IDE)
```

### Components

- `YYYYMMDD` - Date
- `HHMMSS` - Time (24-hour)
- `IDE` - **Claude** (for files you create)
- `TOPIC_NAME` - UPPERCASE_WITH_UNDERSCORES

### Get Timestamp (PowerShell)

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
# Creates: 20251019_173407
```

## Allowed Root Files (Exceptions)

**ONLY these files can be in root:**
- `AGENTS.md`
- `README.md`
- `LICENSE`
- `CLAUDE.md`
- `CHANGELOG.md`

**Everything else → `docs/` folder**

## Before Creating .md File

1. Is it AGENTS.md, README.md, LICENSE, CLAUDE.md or CHANGELOG? → Root is OK
2. Anything else? → **MUST** go in `docs/`
3. Use format: `docs/YYYYMMDD_HHMMSS_Claude_TOPIC.md`

---

**Always follow this convention!**
