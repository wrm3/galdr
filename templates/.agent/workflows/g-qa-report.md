---
description: "Generate quality assurance metrics report"
---

Generate quality metrics report: $ARGUMENTS

## What This Command Does

Analyzes your project's quality metrics from the galdr QA system.

## Quality Report Workflow

### 1. Analyze BUGS.md
I'll examine:
- Total bugs (active and closed)
- Bugs by severity (Critical, High, Medium, Low)
- Bugs by source (User Reported, Development, Testing, Production)
- Bugs by status (Open, Investigating, Fixing, Testing, Closed)
- Bug age and resolution time

### 2. Calculate Metrics
I'll compute:
- **Bug Discovery Rate**: Bugs found per time period
- **Bug Resolution Time**: Average time from discovery to resolution
- **Severity Distribution**: Percentage breakdown by severity
- **Feature Impact Analysis**: Which features have most bugs
- **Regression Rate**: Bugs introduced by fixes
- **Quality Gate Performance**: Pass rates for reviews, testing

### 3. Identify Trends
I'll analyze:
- Bug discovery trend (increasing/decreasing)
- Resolution time trend (improving/degrading)
- Severity distribution changes
- Feature quality patterns
- Production bug rate

### 4. Generate Report

## Quality Report Format

### 📊 Executive Summary
- Overall quality score: X/10
- Key achievements this period
- Areas needing attention

### 🐛 Bug Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| Open Bugs | X | ↑/↓ |
| Critical Bugs | X | ↑/↓ |
| Avg Resolution Time | X days | ↑/↓ |
| Discovery Rate | X/week | ↑/↓ |

### 📈 Severity Distribution
- Critical: X%
- High: X%
- Medium: X%
- Low: X%

### ✅ Quality Gates
- Code Review Pass Rate: X%
- Test Coverage: X%
- Documentation: Complete/Partial/Missing

### 🎯 Focus Areas
1. [Area needing attention]
2. [Area needing attention]

### 💡 Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

## Report Periods
- **Daily**: Quick status update
- **Weekly**: Detailed metrics and trends
- **Monthly**: Comprehensive analysis

## What I Need From You
- Report period (daily, weekly, monthly, custom)
- Specific areas of concern (optional)
- Comparison period (optional)

Let's assess your project's quality!
