# Maintainer export — slim template

**Generated**: 2026-04-08  
**Source**: `galdr_full/template_full/` (canonical installable tree)  
**This file is safe to delete** after you review the checklist.

## Release checklist

1. Open `CHANGELOG.md` — move `[Unreleased]` items under a new version heading (Keep a Changelog).
2. Update version badges in `README.md` if present.
3. `git init` (if this folder is not yet a repo):
   ``
   git init
   git add .
   git commit -m "chore: import galdr template snapshot"
   ``
4. Tag (example): `git tag -a v1.0.1 -m "Template release"`
5. Use `@g-git-commit` / `g-skl-git-commit` for conventional commit style on future changes.

## Parity

This export assumes **C-009** parity was clean when you ran the script (unless `-Force`).

## Not included

galdr_full-only paths (`docker/`, `skill_packs/`, monorepo scripts) are intentionally omitted — only `template_full` content is mirrored.
