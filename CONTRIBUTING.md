# Contributing to galdr

Thank you for your interest in contributing to galdr! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository: [wrm3/galdr](https://github.com/wrm3/galdr)
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/galdr.git
   cd galdr
   ```
3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

```bash
cp .env.example .env           # Configure API keys
cd docker && docker compose up -d   # Start services
```

## Project Structure

- `.cursor/`, `.claude/`, `.agent/`, `.codex/` — IDE-specific configurations (must stay in parity)
- `templates/` — Clean copies deployed by `galdr_install`
- `docker/` — MCP server, PostgreSQL, and supporting services
- `docs/` — Reference documentation

## Contribution Guidelines

### Platform Parity

When adding or modifying agents, skills, commands, hooks, or rules, you must update **all 8 targets**:

1. `.cursor/`
2. `.claude/`
3. `.agent/`
4. `.codex/`
5. `templates/.cursor/`
6. `templates/.claude/`
7. `templates/.agent/`
8. `templates/.codex/`

### Code Style

- **Python**: PEP 8, type hints, UV for virtual environments
- **Markdown**: Use YAML frontmatter for task/skill files
- **Commit messages**: Use conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)

### Pull Requests

1. Ensure all 8 parity targets are updated
2. Test Docker build: `cd docker && docker compose up -d --build`
3. Verify no secrets or personal data in changes
4. Write a clear PR description

## Reporting Issues

Use [GitHub Issues](https://github.com/wrm3/galdr/issues) with the provided templates.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Last updated: 2026-03-28
