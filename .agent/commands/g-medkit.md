Activate the **g-medkit** skill.

Self-diagnosing .galdr/ health tool. Detects what's needed and does it:
- Version mismatch → UPGRADE mode (full structural migration + version bump)
- Missing files/folders → REPAIR mode (structure fix + per-file health)
- Everything OK → MAINTAIN mode (TTL resets, health score, backlog)

Default: dry-run on UPGRADE/REPAIR. MAINTAIN runs immediately.
Pass 'apply' to execute UPGRADE or REPAIR changes.