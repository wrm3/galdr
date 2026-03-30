# Quality Assurance Frameworks
> Testing strategies and QA processes by industry

## Software/SaaS QA

### Test Pyramid
```
       /E2E\      5-10 tests (critical flows)
      /------\
     /Integr.\   50-100 tests (API endpoints)
    /----------\
   /   Unit    \ 500+ tests (functions, components)
```

### Testing Types
**Unit Tests**: Jest, pytest, JUnit (70-80% coverage)
**Integration Tests**: API endpoints, database interactions
**E2E Tests**: Cypress, Playwright (5-10 critical user flows)
**Performance Tests**: Load testing (k6, JMeter)
**Security Tests**: OWASP ZAP, Snyk

### QA Metrics
- Test coverage: 70-80% for business logic
- Defect density: <10 bugs per 1000 LOC
- MTTR: Mean time to resolution <24 hours
- Escaped defects: <5% to production

### Beta Testing
- Private beta: 10-50 users, 2-4 weeks
- Public beta: 100-500 users, 4-8 weeks
- Collect feedback, iterate, fix critical bugs

## Hardware QA

### Functional Testing (100% of units)
- Power-on test
- Connectivity test (WiFi, Bluetooth)
- Sensor readings validation
- Button/LED functionality

### Environmental Testing (Sample from each batch)
- Temperature: -20°C to +60°C
- Humidity: 10% to 90% RH
- Drop test: 1m onto concrete
- Vibration test (if mobile/automotive)

### Reliability Testing
- MTBF (Mean Time Between Failures): Target 50K+ hours
- Accelerated life testing
- Long-term stress testing

### Compliance Testing
- FCC (RF emissions)
- CE (European safety)
- UL (electrical safety)
- IP rating (water/dust resistance)

### Quality Metrics
- Production defect rate: <2%
- Field failure rate: <5% in first year
- RMA rate: <3%

## Biotech/Pharma QA

### Analytical Validation
- Sensitivity: True positive rate (aim >90%)
- Specificity: True negative rate (aim >95%)
- Accuracy: Agreement with gold standard
- Precision: Reproducibility (CV <10%)
- LOD/LOQ: Limit of detection/quantification

### Clinical Validation
- Clinical sensitivity/specificity vs gold standard
- N=200-500 samples minimum
- Multiple sites/operators
- Diverse patient population

### Manufacturing QA
- GMP compliance (Good Manufacturing Practice)
- Process validation (3 consecutive successful batches)
- Statistical process control (SPC)
- Batch record review

### Quality Systems
- ISO 13485: Medical device quality management
- FDA QSR: Quality System Regulation
- CAPA: Corrective and Preventive Action
- Design controls (DHF, DMR, DHR)

### Quality Metrics
- Batch failure rate: <1%
- Out-of-specification (OOS): <2%
- Customer complaints: Track and trend
- Regulatory observations: 0 critical

## QA Process

### Test Planning
1. Define test strategy
2. Identify test cases
3. Estimate effort
4. Assign resources

### Test Execution
1. Execute test cases
2. Log defects
3. Verify fixes
4. Regression testing

### Release Criteria
- All critical bugs fixed
- Test coverage >70%
- Performance targets met
- Security scan clean
- Acceptance from product owner

### Continuous Improvement
- Retrospectives after each release
- Track defect trends
- Identify process improvements
- Update test automation

---
**Last Updated**: 2025-11-02
