# Software Development Guide for Startups

> **Agile/Scrum practices optimized for fast-moving startups**

## Agile Methodology for Startups

### Core Principles
- Deliver working software frequently (weeks, not months)
- Welcome changing requirements
- Close collaboration between business and developers
- Build projects around motivated individuals
- Working software is the primary measure of progress

### Scrum Framework

**Sprint**: 2-week iteration delivering working software

**Roles**:
- **Product Owner**: Prioritizes backlog (founder or product lead)
- **Scrum Master**: Facilitates process (often a developer wearing two hats)
- **Development Team**: Builds the product (2-5 people ideal for startups)

**Ceremonies**:
- **Sprint Planning** (2 hours): Select user stories for sprint
- **Daily Standup** (15 min): What did you do? What's next? Any blockers?
- **Sprint Review** (1 hour): Demo completed work
- **Sprint Retrospective** (1 hour): What went well? What to improve?

## Sprint Planning

### User Stories Format

**Template**:
```
As a [user type]
I want to [action]
So that [benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

**Example**:
```
As a project manager
I want to assign tasks to team members
So that everyone knows what to work on

Acceptance Criteria:
- [ ] Can select team member from dropdown
- [ ] Task shows assignee name
- [ ] Assignee receives email notification
- [ ] Can reassign to different team member
```

### Story Points Estimation

**Fibonacci Scale**: 1, 2, 3, 5, 8, 13, 21

- **1 point**: 1-2 hours (simple bug fix)
- **2 points**: Half day (small feature)
- **3 points**: 1 day (medium feature)
- **5 points**: 2-3 days (complex feature)
- **8 points**: Full week (very complex, consider breaking down)
- **13+**: Too large, must break down

**Velocity**: Sum of story points completed per sprint (track over time)

## Development Workflow

### Git Workflow

**Branch Strategy** (GitHub Flow):
```
main (production-ready)
  ├── feature/user-authentication
  ├── feature/task-assignment
  └── bugfix/login-error
```

**Process**:
1. Create feature branch from main: `git checkout -b feature/feature-name`
2. Commit regularly with clear messages
3. Push to GitHub: `git push -u origin feature/feature-name`
4. Create Pull Request
5. Code review + tests pass
6. Merge to main
7. Deploy to production

**Commit Message Format**:
```
feat: add user authentication
fix: resolve login redirect issue
docs: update API documentation
test: add unit tests for task model
refactor: simplify search algorithm
```

### Code Review

**Checklist**:
- [ ] Code works as expected (tested manually or automated)
- [ ] Follows project style guide
- [ ] No console.log or debugging code left in
- [ ] Tests added for new features
- [ ] Documentation updated if needed
- [ ] No security vulnerabilities introduced
- [ ] Performance impact considered

**Review Time**: Aim for < 24 hours turnaround

## CI/CD Pipeline

### Continuous Integration

**Tools**: GitHub Actions, GitLab CI, CircleCI

**Pipeline Steps**:
1. **Lint**: Check code style (ESLint, Prettier)
2. **Build**: Compile/bundle code
3. **Test**: Run unit + integration tests
4. **Security Scan**: Check for vulnerabilities (npm audit, Snyk)

**Example GitHub Actions** (.github/workflows/ci.yml):
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### Continuous Deployment

**Staging Environment**:
- Deploys automatically on merge to main
- Testing ground before production
- Mirrors production configuration

**Production Deployment**:
- Manual approval or automated after staging tests pass
- Blue-green or canary deployment for zero downtime
- Rollback plan in case of issues

**Tools**:
- **Frontend**: Vercel, Netlify (auto-deploy from Git)
- **Backend**: Railway, Heroku, AWS (with GitHub Actions)

## Testing Strategies

### Test Pyramid

```
       /\
      /E2E\      <- Few (5-10 critical user flows)
     /------\
    /Integr.\ <- Some (API endpoints, DB interactions)
   /----------\
  /   Unit    \  <- Many (functions, components)
 /--------------\
```

### Unit Tests

**Purpose**: Test individual functions/components in isolation

**Tools**: Jest (JavaScript), pytest (Python), JUnit (Java)

**Example** (JavaScript):
```javascript
// sum.test.js
const sum = (a, b) => a + b;

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

**Coverage Goal**: 70-80% for critical business logic

### Integration Tests

**Purpose**: Test API endpoints, database interactions

**Example** (Node.js + Express):
```javascript
const request = require('supertest');
const app = require('../app');

test('GET /api/users returns user list', async () => {
  const response = await request(app).get('/api/users');
  expect(response.status).toBe(200);
  expect(response.body).toHaveProperty('users');
});
```

### End-to-End Tests

**Purpose**: Test complete user workflows

**Tools**: Cypress, Playwright, Selenium

**Example** (Cypress):
```javascript
describe('User Login', () => {
  it('logs in successfully with valid credentials', () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="login-btn"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

**Coverage**: 5-10 critical user paths

## Development Tools

### Required Tools

**Version Control**: Git + GitHub/GitLab
**Code Editor**: VS Code, Cursor, WebStorm
**API Testing**: Postman, Insomnia, curl
**Database Client**: TablePlus, Postico, DBeaver
**Terminal**: iTerm2 (Mac), Windows Terminal, Hyper

### Recommended Extensions

**VS Code Extensions**:
- ESLint (code linting)
- Prettier (code formatting)
- GitLens (Git visualization)
- Thunder Client (API testing in editor)
- Error Lens (inline error highlighting)
- Auto Rename Tag (HTML/JSX)

### Project Setup

**package.json Scripts**:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Performance Best Practices

### Frontend

- Use code splitting (lazy load routes/components)
- Optimize images (WebP format, responsive sizes)
- Minimize bundle size (tree shaking, analyze bundle)
- Use CDN for static assets
- Implement caching (service workers, browser cache)

**Target Metrics**:
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.8s

### Backend

- Add database indexes on frequently queried fields
- Use connection pooling
- Implement caching (Redis, in-memory)
- Optimize N+1 queries (use eager loading)
- Add pagination for list endpoints

**Target Metrics**:
- API response time: < 200ms (p95)
- Database query time: < 50ms (p95)

## Security Best Practices

### Essential Security Measures

**Authentication**:
- Use proven libraries (Passport.js, Auth0, Firebase)
- Never store passwords in plain text (bcrypt/argon2)
- Implement rate limiting on login endpoints
- Use HTTPS everywhere

**Authorization**:
- Validate user permissions on every request
- Use Role-Based Access Control (RBAC)
- Never trust client-side data

**Data Protection**:
- Encrypt sensitive data at rest and in transit
- Use environment variables for secrets (never commit)
- Implement CORS properly
- Sanitize user inputs (prevent SQL injection, XSS)

**OWASP Top 10 Checklist**:
- [ ] Injection prevention (parameterized queries)
- [ ] Broken authentication protection
- [ ] Sensitive data exposure prevention
- [ ] XML External Entities (XXE) protection
- [ ] Broken access control prevention
- [ ] Security misconfiguration fixes
- [ ] Cross-Site Scripting (XSS) prevention
- [ ] Insecure deserialization prevention
- [ ] Using components with known vulnerabilities (keep updated)
- [ ] Insufficient logging & monitoring

## Monitoring & Logging

### Application Monitoring

**Tools**: Sentry (errors), DataDog (performance), New Relic

**What to Monitor**:
- Error rate and types
- API response times (p50, p95, p99)
- Database query performance
- Server CPU/memory usage
- User sessions and active users

### Logging

**Log Levels**:
- **ERROR**: Application errors, exceptions
- **WARN**: Potential issues, deprecated usage
- **INFO**: Important application events (user login, payment)
- **DEBUG**: Detailed diagnostic information

**Structured Logging** (JSON format):
```json
{
  "timestamp": "2025-11-02T10:30:00Z",
  "level": "ERROR",
  "message": "Payment processing failed",
  "userId": "12345",
  "amount": 49.99,
  "error": "Insufficient funds"
}
```

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing (unit, integration, E2E)
- [ ] Code reviewed and approved
- [ ] Environment variables configured
- [ ] Database migrations prepared
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured

### Deployment Steps

1. Deploy to staging environment
2. Run smoke tests on staging
3. Get approval from product owner
4. Deploy to production (during low-traffic period)
5. Monitor error rates and performance
6. Verify critical features working
7. Communicate deployment in team channel

### Post-Deployment

- [ ] Verify deployment successful
- [ ] Check error rates (should not spike)
- [ ] Monitor performance metrics
- [ ] Test critical user flows manually
- [ ] Be ready to rollback if issues arise

## Startup-Specific Optimizations

### Move Fast Without Breaking Things

**Balanced Approach**:
- Write tests for critical business logic
- Skip tests for UI that changes frequently
- Use TypeScript for type safety
- Automate repetitive tasks
- Technical debt is okay, but track it

### When to Optimize

**Don't Optimize**:
- Before you have users
- Without data showing bottlenecks
- For hypothetical scale problems

**Do Optimize**:
- When users report slowness
- When metrics show degradation
- When costs are growing unsustainably

### Technical Debt Management

**Rule of Thumb**: 20-30% of sprint capacity for tech debt

**Track Tech Debt**:
- Create "Tech Debt" label in GitHub Issues
- Regular backlog grooming
- Address before it compounds

---

**Last Updated**: 2025-11-02
**Version**: 1.0.0
