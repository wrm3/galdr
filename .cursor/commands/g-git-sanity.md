# @g-git-sanity — Pre-commit sanity check

Run a quick sanity check on staged changes before committing. Covers secrets detection, large files, and galdr sync drift.

---

## Usage

```
@g-git-sanity          # Check all staged changes
@g-git-sanity secrets  # Secrets check only
@g-git-sanity size     # Large file check only
@g-git-sanity sync     # galdr task sync check only
```

---

## Execution Protocol

### 1. Secrets Check (BLOCK)

```powershell
git diff --cached | Select-String -Pattern "sk-[a-zA-Z0-9]{20,}|Bearer\s+[a-zA-Z0-9._-]{20,}|AKIA[A-Z0-9]{16}|password\s*=\s*\S+|api_key\s*=\s*\S+|secret\s*=\s*\S+"
```

If any match: **BLOCK** — print matching line(s) and halt. Do not proceed.

Also check staged filenames:
- `.env` or `.env.*` with actual content staged → BLOCK

### 2. Large File Check (WARN)

```powershell
git diff --cached --name-only | Where-Object { (Test-Path $_) -and ((Get-Item $_).Length -gt 5MB) }
```

If any file > 5 MB: **WARN** — list the file(s) and suggest adding to `.gitignore` or using Git LFS.

### 3. galdr Sync Drift (WARN)

Check if `.galdr/` is present and has pending drift:

```powershell
# TASKS.md staged but no tasks/ files staged?
$tasksMdStaged = (git diff --cached --name-only) -match "TASKS\.md"
$taskFilesStaged = (git diff --cached --name-only) -match "\.galdr/tasks/"
```

If `TASKS.md` staged but no tasks/ files (or vice versa): **WARN** — suggest running `@g-task-sync-check`.

### 4. Report

Print summary:

```
Pre-commit sanity check
=======================
Secrets:    PASS / BLOCK (N patterns matched)
Large files: PASS / WARN (N files > 5 MB)
galdr sync: PASS / WARN (drift detected)
```

- Any BLOCK → exit with instruction to fix and re-run
- Only WARNs → print warnings and ask "Proceed anyway? (y/N)"

---

## Hook Integration

This check is also available as an automatic `pre-commit` hook:

```powershell
# Enable hook-based automation
git config core.hooksPath .cursor/hooks

# Disable
git config --unset core.hooksPath
```

Hook file: `.cursor/hooks/g-hk-pre-commit.ps1`

> Hook is soft-fail for WARNs (exit 0) and hard-fail for BLOCKs (exit 1).
