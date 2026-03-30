#!/bin/bash

# Script to generate all remaining Product Development Skill files

SKILL_DIR="/mnt/c/git/ai_project_template/.cursor/skills/startup-product-development"
cd "$SKILL_DIR"

echo "Generating remaining reference guides..."

# Generate software_development_guide.md (condensed to ~400 lines for efficiency)
cat > reference/software_development_guide.md << 'EOF'
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
EOF

echo "Generated software_development_guide.md"

# Generate hardware_development_guide.md
cat > reference/hardware_development_guide.md << 'EOF'
# Hardware Development Guide

> **From concept to manufacturing for physical products**

## Development Phases

### Phase 1: Concept (Weeks 1-2)

**Deliverables**:
- Hand sketches of product
- Block diagram of system architecture
- Bill of Materials (BOM) estimate
- Feature requirements
- Target cost per unit

**Activities**:
- Brainstorm form factor
- Research components (sensors, MCU, connectivity)
- Estimate power requirements
- Identify regulatory requirements

### Phase 2: Breadboard Prototype (Weeks 3-8)

**Goal**: Prove core functionality works

**Tools**:
- Breadboard
- Jumper wires
- Development boards (Arduino, ESP32, Raspberry Pi)
- Power supply
- Multimeter/oscilloscope

**Deliverables**:
- Working breadboard prototype
- Firmware demonstrating core features
- Power consumption measurements
- Component selection finalized

**Common Issues**:
- Wiring mistakes (use wire colors consistently)
- Power supply noise (add decoupling capacitors)
- Ground loops (single ground point)

### Phase 3: PCB Design (Weeks 9-16)

**Tools**: KiCad (free), Eagle, Altium Designer

**Steps**:
1. **Schematic Design**: Component connections
2. **PCB Layout**: Physical component placement
3. **Design Rule Check (DRC)**: Verify no errors
4. **Generate Gerber Files**: Manufacturing files
5. **Order PCBs**: JLCPCB, PCBWay, OSH Park

**PCB Design Checklist**:
- [ ] Power traces wide enough (1mm for 1A)
- [ ] Decoupling capacitors near ICs
- [ ] Ground plane on bottom layer
- [ ] Clearance rules met (6mil minimum for cheap boards)
- [ ] Silkscreen labels clear and useful
- [ ] Test points for debugging
- [ ] Mounting holes positioned correctly

**Turnaround**: 1-2 weeks from order to delivery

### Phase 4: PCB Bring-Up (Weeks 17-20)

**Process**:
1. Visual inspection for shorts/defects
2. Power test (measure voltages before connecting battery)
3. Program firmware
4. Test each subsystem individually
5. Debug issues (expect rev 2 or 3)

**Common Rev 1 Issues**:
- Swapped pins
- Missing pull-up/pull-down resistors
- Wrong footprints (check datasheets!)
- Antenna placement issues (WiFi/BLE)

### Phase 5: Enclosure Design (Weeks 18-24)

**Tools**: Fusion 360 (free for startups), SolidWorks, OnShape

**Considerations**:
- Material: ABS, PLA (3D printed), injection molded
- Assembly: Snap fit, screws, glue
- Cutouts: Buttons, ports, LEDs, sensors
- Waterproofing (IP rating if outdoor use)

**Prototyping**:
- 3D print enclosures (FDM: $200-500, SLA: $1K-3K)
- Iterate on fit and finish
- Test drop resistance

**Injection Molding** (for production):
- Tooling cost: $3K-20K per part
- Unit cost: $0.50-5 per part
- MOQ: 500-1000 units

### Phase 6: Pre-Production (Weeks 25-32)

**Goal**: Validate design for mass manufacturing

**Activities**:
- Design for Manufacturing (DFM) review with CM
- Order pilot run (50-100 units)
- Functional testing of all units
- Firmware bug fixes
- Regulatory testing (FCC, CE)

**Contract Manufacturer (CM) Selection**:
- Get quotes from 3-5 CMs
- Check references
- Visit facility if possible
- Negotiate pricing and terms

### Phase 7: Certifications (Weeks 28-40)

**FCC (US)**:
- Required for: RF devices (WiFi, Bluetooth, cellular)
- Cost: $3K-10K
- Time: 4-8 weeks
- Process: Submit to test lab, fix issues, get cert

**CE (Europe)**:
- Required for: All electronics sold in EU
- Cost: $2K-8K
- Self-certification possible for some categories

**UL (Safety)**:
- Required for: Products plugged into wall power
- Cost: $5K-15K
- Time: 8-12 weeks

**IP Rating** (Water/Dust Resistance):
- IP65: Dust-tight, water spray resistant
- IP67: Dust-tight, immersion up to 1m
- IP68: Dust-tight, prolonged immersion
- Cost: $2K-5K for testing

### Phase 8: Manufacturing (Weeks 36+)

**First Production Run**:
- Start small: 500-1000 units
- Quality control: Inspect sample from each batch
- Expect 1-3% defect rate initially

**Scaling Production**:
- 1K-10K units: Small batch manufacturing
- 10K-100K units: Dedicated production line
- 100K+ units: Multiple CMs, negotiate pricing

**Lead Times**:
- PCB assembly: 2-4 weeks
- Enclosure molding: 4-8 weeks
- Final assembly: 1-2 weeks
- Shipping: 2-6 weeks (air/sea)

## BOM Management

### Component Selection

**Criteria**:
- Availability (not end-of-life)
- Multiple suppliers (avoid single-source)
- Cost at volume (1K, 10K, 100K pricing)
- Package size (SMD components for production)

**Component Categories**:
- **Microcontroller**: ESP32 ($2-5), STM32 ($1-3)
- **Sensors**: BME280 ($3), MPU6050 ($2)
- **Connectivity**: WiFi module ($5-10), Bluetooth ($3-8)
- **Power Management**: LDO regulators ($0.50), LiPo charger ($1-2)
- **Passives**: Resistors, capacitors ($0.01-0.10 each)

### Cost Breakdown

**Example: Smart Home Sensor**

| Component | Unit Cost (1K qty) | % of BOM |
|-----------|-------------------|----------|
| ESP32-C3 | $2.50 | 25% |
| Sensors (temp, humidity, motion) | $3.00 | 30% |
| PCB (4-layer) | $1.50 | 15% |
| Enclosure (injection molded) | $1.00 | 10% |
| Battery (LiPo 1000mAh) | $1.50 | 15% |
| Passives (R, C, L) | $0.50 | 5% |
| **Total BOM** | **$10.00** | **100%** |

**Retail Pricing**: BOM × 4-5 = $40-50 retail

## Firmware Development

### Embedded Programming

**Languages**: C, C++, MicroPython (for prototyping)

**Development Boards**:
- Arduino: easiest for beginners
- ESP32: WiFi/BLE, powerful
- STM32: production-grade, ARM Cortex-M

**Development Flow**:
1. Write code in IDE (Arduino IDE, PlatformIO, STM32Cube)
2. Compile firmware
3. Flash to device via USB/JTAG
4. Test and debug (serial monitor, LEDs, oscilloscope)
5. Iterate

### OTA Updates

**Over-The-Air firmware updates**:
- Critical for fixing bugs post-launch
- ESP32 has built-in OTA support
- Implement secure updates (signed firmware)

### Power Optimization

**Techniques**:
- Sleep modes (deep sleep < 10µA on ESP32)
- Wake on interrupt (motion sensor, timer)
- Reduce WiFi transmit power
- Use BLE instead of WiFi when possible

**Battery Life Calculation**:
```
Battery capacity: 1000mAh
Average current: 10mA
Battery life = 1000mAh / 10mA = 100 hours ≈ 4 days

With sleep mode (1mA average):
Battery life = 1000mAh / 1mA = 1000 hours ≈ 42 days
```

## Supply Chain

### Component Sourcing

**Distributors**:
- Digi-Key (US, huge selection, fast shipping)
- Mouser (US, similar to Digi-Key)
- LCSC (China, cheap, long lead times)
- Alibaba (bulk orders, negotiate pricing)

**Lead Time Management**:
- Order long-lead components early (6-12 weeks)
- Keep safety stock for critical parts
- Have backup suppliers

**COVID/Chip Shortage Lessons**:
- Diversify component sources
- Design with common components
- Avoid single-source parts

## Quality Control

### Incoming QC

**Inspect components on arrival**:
- Visual inspection for damage
- Verify part numbers match order
- Sample test critical components

### Production QC

**100% Functional Testing**:
- Power-on test
- WiFi connectivity test
- Sensor readings verification
- Button/LED functionality
- Battery charging test

**Sample Testing** (from each batch):
- Environmental testing (temperature, humidity)
- Drop test
- Long-term reliability test

### Field Failures

**RMA Process**:
- Track defect rates
- Identify common failure modes
- Implement fixes in next production run
- Offer warranty replacements

**Target Metrics**:
- < 2% defect rate in production
- < 5% RMA rate in first year

## Regulatory Strategy

### Certification Timeline

**Plan early** (add 6 months to timeline for certs):
- FCC/CE required before selling in US/EU
- UL required for wall-powered devices
- Budget $10K-30K for all certifications

### Test Lab Selection

**Accredited Labs**:
- Intertek
- UL
- TÜV
- Bureau Veritas

**Process**:
1. Submit samples and documentation
2. Lab tests for compliance
3. Address any failures
4. Retest
5. Receive certification

## Manufacturing Partners

### Contract Manufacturers (CM)

**Domestic (US)**:
- Pros: Faster communication, smaller MOQs, easier QC
- Cons: 3-5x cost vs China
- Use for: Pilot runs, low volume (<5K units)

**Overseas (China)**:
- Pros: Low cost, scalable, full-service
- Cons: Communication challenges, higher MOQs, shipping time
- Use for: High volume (>5K units)

**How to Find CMs**:
- Alibaba (search "PCB assembly")
- ThomasNet (US manufacturers)
- Referrals from other hardware startups

### Negotiation Tips

- Get quotes from 3-5 vendors
- Negotiate on MOQ, payment terms, tooling costs
- Request samples before committing
- Start small, scale with successful vendor

---

**Last Updated**: 2025-11-02
**Version**: 1.0.0
EOF

echo "Generated hardware_development_guide.md"

echo "All reference guides generation script completed successfully!"
echo "Files generated:"
echo "  - reference/software_development_guide.md"
echo "  - reference/hardware_development_guide.md"
EOF

chmod +x /mnt/c/git/ai_project_template/.cursor/skills/startup-product-development/generate_remaining_files.sh
