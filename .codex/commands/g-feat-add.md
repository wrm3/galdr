Stage a new feature. Activates **g-skl-features** → STAGE operation.

```
@g-feat-add "Feature Name"
@g-feat-add "Feature Name" --goal G-01
@g-feat-add "Feature Name" --tier full
@g-feat-add "Feature Name" --from-harvest research/harvests/repo_slug/
```

Creates `features/featNNN_slug.md` with `status: staging`. Does NOT create tasks.
Feature stays in staging until manually promoted with `/g-feat-promote`.

> **Alias**: `@g-feat-new` also works (deprecated; use `@g-feat-add` for new work).
