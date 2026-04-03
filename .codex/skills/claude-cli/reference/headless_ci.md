# Headless & CI/CD Integration

Running Claude Code non-interactively in pipelines, scripts, and containers.

Official docs: https://docs.anthropic.com/en/docs/claude-code/headless

---

## Basic Headless Usage

```bash
claude -p "Find all TODO comments"

cat src/app.ts | claude -p "Review for security issues"

claude -p "List all API endpoints" --output-format json

claude -p "Run tests and fix failures" \
  --allowedTools "Read" "Edit" "Bash(npm test)" \
  --output-format json
```

---

## Multi-Turn Headless

```bash
claude -p "Create a user model" --output-format json > turn1.json

claude -p "Add validation to the model" --continue --output-format json

claude -p "Add tests" --resume "session-abc123"
```

---

## CI/CD Pipeline Pattern

```bash
claude -p "Fix all ESLint errors in src/" \
  --dangerously-skip-permissions \
  --allowedTools "Read" "Edit" "Bash(npx eslint *)" \
  --max-turns 20 \
  --output-format json
```

Always set `--max-turns` and `--max-budget-usd` in CI to prevent runaway costs.
