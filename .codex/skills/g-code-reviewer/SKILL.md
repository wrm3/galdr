---
name: g-code-reviewer
description: Comprehensive code review following galdr standards with focus on security, performance, maintainability, and best practices
---

# galdr Code Reviewer

Perform thorough code reviews following company-specific templates, security guidelines, and best practices.

## Overview

This skill provides comprehensive code review capabilities with structured checklists, security scanning, performance analysis, and maintainability assessments. It ensures consistent code quality across your projects by following standardized review procedures.

## When to Use

This skill activates automatically when you:
- Ask for a code review
- Request security scanning
- Need quality assessment
- Review pull requests
- Check code before committing

## Capabilities

### 1. Security Review
- SQL injection vulnerability detection
- XSS attack vector identification
- Authentication/authorization checks
- Sensitive data exposure prevention
- Input validation review
- Secret/credential detection

### 2. Code Quality Assessment
- Code style compliance
- Naming conventions
- Documentation completeness
- Error handling patterns
- Code complexity analysis
- DRY principle adherence

### 3. Performance Analysis
- Algorithm efficiency
- Database query optimization
- Memory usage patterns
- Network request efficiency
- Caching opportunities
- Resource cleanup

### 4. Maintainability Review
- Code organization
- Function/class size (target: <100 lines, warn: >200 lines)
- Cyclomatic complexity
- Test coverage
- Documentation quality
- Technical debt identification

### 5. Best Practices
- Language-specific idioms
- Framework conventions
- Design patterns
- SOLID principles
- Clean code principles
- Team coding standards

## Review Types

### Quick Review
For small changes (<100 lines):
- Security scan
- Style check
- Basic quality assessment
- ~2-5 minutes

### Standard Review
For typical changes (100-500 lines):
- Full security scan
- Code quality analysis
- Performance check
- Documentation review
- ~10-20 minutes

### Comprehensive Review
For large changes (>500 lines) or critical code:
- In-depth security analysis
- Detailed performance profiling
- Architecture review
- Test coverage analysis
- Technical debt assessment
- ~30-60 minutes

## Output Format

Reviews generate:
1. **Summary**: Overall assessment (Approve/Request Changes/Comment)
2. **Security Issues**: Critical/High/Medium/Low with recommendations
3. **Quality Issues**: Categorized by severity
4. **Performance Concerns**: Identified bottlenecks
5. **Best Practices**: Suggestions for improvement
6. **Action Items**: Specific tasks to address findings

## Integration

Works with:
- GitHub Pull Requests
- GitLab Merge Requests
- Local file reviews
- Diff-based reviews
- Multi-file reviews

## Examples

**Quick Review:**
```
"Review this authentication function for security issues"
→ Focused security scan with recommendations
```

**Full PR Review:**
```
"Review PR #123 for code quality and security"
→ Comprehensive review with checklist and ratings
```

**Pre-Commit Check:**
```
"Check this code before I commit"
→ Quick scan for obvious issues
```

## Company Standards

This skill enforces your specific:
- Coding standards
- Security requirements
- Testing requirements
- Documentation standards
- Performance SLAs

For detailed review procedures, see [rules.md](rules.md).

For examples and templates, see [examples/](examples/) folder.

## Related Skills

- **galdr-task-management**: Create tasks for review findings
- **galdr-qa**: Track bugs found during review
- **galdr-planning**: Plan refactoring based on review

---

**Version**: 1.0.0
**Last Updated:** 2025-10-19
**Part of:** galdr system
