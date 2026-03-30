# Bug Tracking — E-Commerce Platform

> This is an example BUGS.md demonstrating galdr bug tracking conventions.
> All bugs also have a corresponding task entry in TASKS.md.
> Bug IDs use the format BUG-NNN (sequential).

---

## Active Bugs

### BUG-002: Shopping Cart Total Calculation Error
- **Severity**: High
- **Source**: User Reported
- **Phase Impact**: Phase 2 (Core Features)
- **Status**: Investigating
- **Task Reference**: Task 117
- **Reported**: 2026-01-24
- **Assigned**: backend team

**Description**: Cart total does not update when item quantity is changed. Requires page refresh to show correct total.

**Reproduction Steps**:
1. Add any product to cart
2. Change quantity using the +/- buttons
3. Observe: subtotal and total do not update

**Expected**: Total updates in real-time when quantity changes
**Actual**: Total remains unchanged until page is refreshed

---

### BUG-003: Product Images Not Loading on Mobile
- **Severity**: Medium
- **Source**: Testing
- **Phase Impact**: Phase 2 (Core Features)
- **Status**: Open
- **Task Reference**: Task 118
- **Reported**: 2026-01-25
- **Assigned**: frontend team

**Description**: Product listing page fails to load images on mobile devices with screen width < 480px. Desktop and tablet display correctly.

**Reproduction Steps**:
1. Open the application on a mobile device (or DevTools mobile emulation)
2. Navigate to the product listing page
3. Observe: images show broken placeholder icon

**Expected**: Images load and display correctly on all screen sizes
**Actual**: Images fail to load on mobile (< 480px width)

**Notes**: Console shows 404 errors for mobile-sized image variants. CDN may not be generating responsive image variants.

---

## Resolved Bugs

### BUG-001: Login Button Not Responding
- **Severity**: Critical
- **Source**: Production
- **Phase Impact**: Phase 1 (Foundation)
- **Status**: Closed
- **Task Reference**: Task 115
- **Reported**: 2026-01-15
- **Resolved**: 2026-01-15
- **Fixed By**: Restored event listener in `auth.js` module initialization

---

## Bug Statistics

| Severity | Open | Resolved | Total |
|----------|------|----------|-------|
| Critical | 0 | 1 | 1 |
| High | 1 | 0 | 1 |
| Medium | 1 | 0 | 1 |
| Low | 0 | 0 | 0 |
| **Total** | **2** | **1** | **3** |

---

## Bug Severity Reference

| Severity | Definition | Target Resolution |
|----------|------------|-------------------|
| Critical | System crash, data loss, security breach, complete feature failure | Same day |
| High | Major feature failure, significant data corruption, >50% user impact | Within 2 days |
| Medium | Minor feature issues, workaround available, moderate user impact | Within 1 week |
| Low | Cosmetic issues, edge cases, minor UX problems | Next sprint |

## Bug Source Reference

| Source | Definition |
|--------|------------|
| User Reported | Submitted by end users or stakeholders |
| Development | Discovered during feature development |
| Testing | Found during QA or automated testing |
| Production | Identified in live environment via monitoring/alerts |
