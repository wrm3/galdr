# Contributing to galdr

Thank you for your interest in improving galdr.

## Reporting Bugs

Use the [bug report template](https://github.com/wrm3/galdr/issues/new?template=bug_report.yml) on GitHub Issues. The form asks for:

- Which IDE you are using (Cursor, Claude Code, Gemini, Codex, OpenCode)
- The galdr version from your `AGENTS.md` or `.galdr/.identity`
- Steps to reproduce, expected behavior, and actual behavior
- Relevant hook or session logs if available

For security vulnerabilities, please do not open a public issue. Email the maintainer directly.

## Requesting Features

Use the [feature request template](https://github.com/wrm3/galdr/issues/new?template=feature_request.yml). Describe:

- The problem you are trying to solve
- How you currently work around it
- What the ideal experience would look like

Features that work across all five IDEs (not Cursor-only) are prioritized.

## Suggesting Improvements

Open a plain issue or start a discussion if you have ideas that do not fit neatly into a bug or feature request. Examples:

- A new skill that would benefit most projects
- A documentation gap
- An inconsistency across IDEs
- A new platform galdr should support

## How galdr Is Developed

galdr is built with galdr. The source development repository (`galdr_full`) uses galdr's own task management, skill system, and quality gates to develop itself. Tasks are tracked in `.galdr/TASKS.md`, acceptance criteria are written into individual task spec files, and the two-phase `@g-go-code` / `@g-go-verify` gate is used for every feature.

The `galdr` repository you are reading now is the installable consumer template. It is exported from `template_full/` in the `galdr_full` source repository on each release.

This means:

- If you want to use galdr in your own project, you are in the right place. Clone this repo and copy the contents into your project.
- If you want to contribute changes to the framework itself, open an issue describing what you want to change. Accepted contributions are integrated into the `galdr_full` source and shipped in the next release.

## Questions

Open a [GitHub Discussion](https://github.com/wrm3/galdr/discussions) for usage questions, integration help, or general conversation about AI-driven development workflows.
