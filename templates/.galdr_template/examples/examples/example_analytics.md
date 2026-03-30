# Example: Task Velocity and Phase Health Analytics

**This example demonstrates analytics and reporting capabilities for tracking project health.**

---

## Task Velocity Tracking

### Weekly Velocity Report — Week of 2026-01-20 to 2026-01-27

| Metric | Value | Trend |
|--------|-------|-------|
| Tasks Completed | 12 | +2 from last week |
| Average Completion Time | 1.8 days | -0.3 days (improving) |
| Tasks Created | 8 | Same as last week |
| Tasks In Progress | 5 | -1 from last week |
| Blocked Tasks | 1 | Same as last week |
| Velocity (tasks/week) | 12 | +2 |
| Story Points Delivered | 28 SP | +4 SP |
| Burndown Rate | 85% | +5% |

### Story Points Completed This Week

| Points | Task Count | Tasks |
|--------|------------|-------|
| 1 SP | 4 tasks | Minor fixes, config changes |
| 2 SP | 3 tasks | Small features |
| 3 SP | 2 tasks | Medium complexity |
| 5 SP | 1 task | Complex feature |
| 8 SP | 0 tasks | — |
| **Total** | **10 tasks** | **28 SP** |

**Rolling Average Velocity**: 25 SP/week
**Trend**: Increasing (was 22 SP/week last month)

### Velocity by Week (Last 6 Weeks)

```
Week | SP | Tasks
-----|----|---------
W1   | 18 | #######
W2   | 20 | ########
W3   | 22 | #########
W4   | 25 | ##########
W5   | 26 | ##########
W6   | 28 | ###########
```

---

## Phase Health Dashboard

### Phase 0: Setup & Infrastructure — COMPLETE

| Metric | Value | Status |
|--------|-------|--------|
| Completion | 100% (15/15 tasks) | Done |
| Duration | 8 days | On time (planned 10 days) |
| Quality Score | 4.2/5.0 | Good |
| Technical Debt | Low | Healthy |
| Open Bugs | 0 | Healthy |

**Assessment**: Healthy — clean handoff to Phase 1

---

### Phase 1: Foundation — IN PROGRESS (85%)

| Metric | Value | Status |
|--------|-------|--------|
| Completion | 85% (17/20 tasks) | On track |
| Duration | 12 days of 14 planned | Slightly behind |
| Quality Score | 4.0/5.0 | Good |
| Technical Debt | Medium | Monitor |
| Open Bugs | 1 (Task 118 blocked) | Monitor |

**Assessment**: Monitor — one blocker needs escalation

**Active Issues:**
- Task 118 blocked on external API key approval (escalation needed)
- Technical debt accumulating in API validation layer
- Test coverage at 85%, target is 90%

**Actions Required:**
1. Escalate Task 118 blocker to project manager
2. Schedule refactoring sprint after Phase 1 SWOT

---

### Phase 2: Core Features — PENDING

| Metric | Value | Status |
|--------|-------|--------|
| Completion | 0% (0/25 tasks) | Not started |
| Planned Duration | 18 days | Pending Phase 1 |
| Risk Level | Low | Stable |
| Dependencies | Phase 1 (3 tasks remaining) | Pending |

**Assessment**: Pending — waiting for Phase 1 completion gate

---

## Task Distribution

### By Status

| Status | Count | Percentage |
|--------|-------|------------|
| Pending | 24 | 48% |
| Ready (file created) | 3 | 6% |
| In Progress | 5 | 10% |
| Completed | 17 | 34% |
| Blocked/Paused | 1 | 2% |
| **Total** | **50** | **100%** |

### By Priority

| Priority | Count | Percentage |
|----------|-------|------------|
| Critical | 2 | 4% |
| High | 10 | 20% |
| Medium | 28 | 56% |
| Low | 10 | 20% |

### By Phase

| Phase | Total | Completed | In Progress | Pending |
|-------|-------|-----------|-------------|---------|
| Phase 0 | 15 | 15 (100%) | 0 | 0 |
| Phase 1 | 20 | 17 (85%) | 2 | 1 |
| Phase 2 | 25 | 0 (0%) | 0 | 25 |

---

## Bottleneck Analysis

### Current Bottlenecks

**1. Task 118 — External API Integration (BLOCKED)**
- Blocker: Waiting for external API key approval
- Impact: Blocks 3 dependent tasks in Phase 1
- Age: 5 days blocked
- Action: Escalate to project manager today

**2. Code Review Queue (WIP LIMIT EXCEEDED)**
- Current: 4 tasks in review (WIP limit: 2)
- Impact: Slowing task completion velocity
- Action: Increase review capacity or reduce active work

**3. Test Coverage Gap**
- Current: 85% (target: 90%)
- Impact: May trigger quality gate failure at Phase 1 completion
- Action: Add 3 focused test tasks to Phase 1 backlog

---

## Predictive Analytics

### Phase 1 Completion Forecast

| Metric | Value |
|--------|-------|
| Current Progress | 85% (17/20 tasks) |
| Remaining Tasks | 3 tasks |
| Average Completion Rate | 2.4 tasks/day |
| Estimated Completion | 2026-01-29 |
| Confidence | 85% |

**Risk**: Task 118 blocker could delay completion by 3-5 days if unresolved.

### Phase 2 Forecast

| Metric | Value |
|--------|-------|
| Planned Start | 2026-01-30 |
| Estimated Completion | 2026-02-17 (18 days) |
| Total Story Points | ~75 SP |
| Confidence | 70% (depends on Phase 1 quality) |

### Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Phase 1 delayed by blocker | Medium | High | Escalate Task 118 |
| Technical debt slows Phase 2 | High | Medium | Schedule refactoring in Phase 1 cleanup |
| Test coverage fails quality gate | Medium | High | Add test tasks to current sprint |
| Scope creep in Phase 2 | Low | Medium | Enforce phase gate review |

---

## Quality Metrics

### Bug Rate
- Bugs Found This Week: 1
- Bugs Fixed This Week: 1
- Cumulative Open Bugs: 1
- Bug Rate: 0.2 bugs per task completed (target: < 0.3)
- Average Fix Time: 1.5 days (target: < 2 days)

### Code Quality
- Test Coverage: 85% (target: 90%)
- Code Review Time: Avg 3.5 hours (target: < 8 hours)
- Technical Debt Level: Medium (target: Low)
- Documentation: 80% complete (target: 90%)
- Open Security Issues: 0

---

## Recommendations

### Immediate Actions (This Week)
1. Escalate Task 118 blocker — waiting 5+ days, blocks Phase 1 completion
2. Reduce code review queue — 4 tasks pending, WIP limit is 2
3. Add 2 test tasks to Phase 1 — close the 5% coverage gap

### Short-Term (Before Phase 2)
1. Schedule technical debt sprint — API validation refactoring
2. Configure application monitoring — before Phase 2 adds complexity
3. Run OWASP security audit — required before production traffic

### Long-Term
1. Automate analytics collection — currently manual reporting
2. Setup CI/CD quality gates — auto-block merges below coverage threshold
3. Implement completion forecasting — integrate story points with velocity tracking
