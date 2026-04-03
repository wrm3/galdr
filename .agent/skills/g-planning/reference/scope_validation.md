# Scope Validation - 5 Essential Questions

## Overview

These 5 essential questions prevent over-engineering by validating scope before creating a PRD. Ask these BEFORE the full 27-question framework.

## The 5 Essential Questions

### 1. User Context & Deployment

**Question**: "Is this intended for personal use, a small team, or broader deployment?"

**Options:**
- **Personal (1 user)**: Simple, file-based, minimal security
- **Small team (2-10)**: Basic sharing, simple user management
- **Broader (10+)**: Full authentication, role management, scalability

**Impact on Design:**
| Aspect | Personal | Small Team | Broader |
|--------|----------|------------|---------|
| Authentication | None/Basic | Simple login | Full auth system |
| Database | File-based OK | SQLite/simple DB | PostgreSQL/MySQL |
| Deployment | Local | Shared server | Cloud/scalable |
| Security | Minimal | Standard | Enhanced |

**Example:**
- Personal: Todo list app for one person
- Small Team: Team task tracker (5 people)
- Broader: SaaS product (100+ users)

### 2. Security Requirements

**Question**: "What are your security expectations?"

**Options:**
- **Minimal**: Basic validation, no authentication
- **Standard**: User auth, session management, basic authorization
- **Enhanced**: Role-based access, encryption, audit trails
- **Enterprise**: SAML/SSO, compliance (SOC2, ISO), advanced security

**Impact on Design:**
| Level | Authentication | Authorization | Data Protection |
|-------|---------------|---------------|-----------------|
| Minimal | None | None | Basic validation |
| Standard | Login/password | Basic roles | HTTPS, hashing |
| Enhanced | MFA, sessions | RBAC | Encryption, audits |
| Enterprise | SSO, SAML | Fine-grained | Full compliance |

**Example:**
- Minimal: Internal tool, trusted users
- Standard: Customer-facing app
- Enhanced: Financial data handling
- Enterprise: Healthcare/banking system

### 3. Scalability Expectations

**Question**: "What are your performance and scalability expectations?"

**Options:**
- **Basic**: Works for expected load, simple architecture
- **Moderate**: Handles growth, some optimization
- **High**: Speed-optimized, caching, efficient queries
- **Enterprise**: Load balancing, clustering, horizontal scaling

**Impact on Design:**
| Level | Architecture | Database | Caching |
|-------|-------------|----------|---------|
| Basic | Monolith | Single instance | None |
| Moderate | Modular monolith | Replication | Basic |
| High | Microservices | Sharding | Redis/Memcached |
| Enterprise | Distributed | Multi-region | CDN, distributed |

**Example:**
- Basic: Internal tool (< 100 users)
- Moderate: Growing SaaS (100-1K users)
- High: Popular app (1K-100K users)
- Enterprise: Large platform (100K+ users)

### 4. Feature Complexity

**Question**: "How much complexity are you comfortable with?"

**Options:**
- **Minimal**: Core functionality only, keep it simple
- **Standard**: Core plus reasonable conveniences
- **Feature-Rich**: Comprehensive with advanced options
- **Enterprise**: Full-featured with extensive configuration

**Impact on Design:**
| Level | Features | UI Complexity | Configuration |
|-------|----------|---------------|---------------|
| Minimal | Essential only | Simple, focused | Minimal |
| Standard | Core + common | Intuitive | Moderate |
| Feature-Rich | Comprehensive | Power user friendly | Extensive |
| Enterprise | Everything | Complex but powerful | Highly configurable |

**Example:**
- Minimal: Simple CRUD app
- Standard: Feature-complete app
- Feature-Rich: Advanced tool with many options
- Enterprise: Platform with plugins/extensions

### 5. Integration Requirements

**Question**: "What integration needs do you have?"

**Options:**
- **Standalone**: No external integrations
- **Basic**: File import/export, basic API
- **Standard**: REST API, webhooks, common integrations
- **Enterprise**: Comprehensive API, message queues, enterprise systems

**Impact on Design:**
| Level | API | Integrations | Data Exchange |
|-------|-----|--------------|---------------|
| Standalone | None | None | Manual |
| Basic | Simple endpoints | CSV/JSON | Files |
| Standard | REST API | OAuth, webhooks | Real-time |
| Enterprise | GraphQL, gRPC | Enterprise systems | Message queues |

**Example:**
- Standalone: Self-contained app
- Basic: Export reports to Excel
- Standard: Integrate with Slack, email
- Enterprise: Connect to SAP, Salesforce, etc.

## Validation Matrix

Use this matrix to validate scope:

| Q1 Answer | Q2 Answer | Q3 Answer | Recommended Approach |
|-----------|-----------|-----------|---------------------|
| Personal | Minimal | Basic | Simple file-based app |
| Personal | Standard | Basic | Local app with basic auth |
| Small Team | Standard | Moderate | Simple web app, shared DB |
| Small Team | Enhanced | Moderate | Web app with RBAC |
| Broader | Enhanced | High | Scalable web platform |
| Broader | Enterprise | Enterprise | Full enterprise solution |

## Over-Engineering Prevention

### Red Flags

Watch for these mismatches:

❌ **Over-Engineering Indicators:**
- Personal use + Enterprise security
- Small team + Enterprise scalability
- Minimal features + Complex architecture
- Standalone + Comprehensive API

✅ **Right-Sized Solutions:**
- Personal use + Minimal security
- Small team + Standard features
- Broader deployment + Enhanced security
- Enterprise + Full features

### Common Over-Engineering Patterns

**Pattern 1: Authentication Overkill**
- **Need**: Personal todo app
- **Over-engineered**: SSO, RBAC, MFA
- **Right-sized**: No auth or simple password

**Pattern 2: Database Overkill**
- **Need**: 100 records, 5 users
- **Over-engineered**: PostgreSQL cluster, replication
- **Right-sized**: SQLite or JSON file

**Pattern 3: API Overkill**
- **Need**: Internal tool, no integrations
- **Over-engineered**: GraphQL, comprehensive REST API
- **Right-sized**: No API or simple endpoints

**Pattern 4: Architecture Overkill**
- **Need**: Simple CRUD app
- **Over-engineered**: Microservices, message queues
- **Right-sized**: Monolith with clear modules

## Decision Trees

### Authentication Decision Tree

```
Is this for multiple users?
├─ No → No authentication needed
└─ Yes → How many users?
    ├─ 2-10 → Simple login (email/password)
    ├─ 10-100 → Standard auth + basic roles
    └─ 100+ → Full auth system + RBAC
```

### Database Decision Tree

```
How much data?
├─ < 1K records → File-based (JSON, SQLite)
├─ 1K-100K → Single database (PostgreSQL/MySQL)
├─ 100K-1M → Database with optimization
└─ 1M+ → Sharding/clustering
```

### Architecture Decision Tree

```
How complex are requirements?
├─ Simple CRUD → Monolith
├─ Multiple domains → Modular monolith
├─ Independent scaling → Microservices
└─ Distributed team → Microservices
```

## Practical Examples

### Example 1: Personal Project

**Answers:**
- Q1: Personal (1 user)
- Q2: Minimal security
- Q3: Basic scalability
- Q4: Minimal features
- Q5: Standalone

**Right-Sized Solution:**
- File-based storage (JSON)
- No authentication
- Simple UI
- No API
- Desktop or simple web app

**Avoid:**
- ❌ Database server
- ❌ User authentication
- ❌ REST API
- ❌ Microservices

### Example 2: Small Team Tool

**Answers:**
- Q1: Small team (5 users)
- Q2: Standard security
- Q3: Moderate scalability
- Q4: Standard features
- Q5: Basic integration

**Right-Sized Solution:**
- SQLite or simple PostgreSQL
- Basic authentication (email/password)
- Simple role system (admin/user)
- Basic REST API for integrations
- Web application

**Avoid:**
- ❌ Complex RBAC
- ❌ Microservices
- ❌ Database clustering
- ❌ Enterprise integrations

### Example 3: SaaS Product

**Answers:**
- Q1: Broader (100+ users)
- Q2: Enhanced security
- Q3: High scalability
- Q4: Feature-rich
- Q5: Standard integration

**Right-Sized Solution:**
- PostgreSQL with replication
- Full authentication + MFA
- Role-based access control
- Comprehensive REST API
- Scalable architecture
- Caching layer

**Include:**
- ✅ Load balancing
- ✅ Database optimization
- ✅ API rate limiting
- ✅ Monitoring/alerting

## Using in PRD Creation

### Step 1: Ask 5 Questions
Get clear answers to all 5 questions

### Step 2: Validate Scope
Use validation matrix to check for over-engineering

### Step 3: Document in PRD
Include scope validation in PRD:

```markdown
## Scope Validation

**User Context**: Small team (5 users)
**Security**: Standard (basic auth, HTTPS)
**Scalability**: Moderate (handles growth to 20 users)
**Features**: Standard (core features + conveniences)
**Integration**: Basic (CSV export, simple API)

**Complexity Level**: Appropriate for small team tool
**Architecture**: Simple web app with PostgreSQL
```

### Step 4: Prevent Scope Creep
Reference scope validation when features are requested:
- "That's enterprise-level, we validated for standard"
- "That requires broader deployment scope"
- "That's beyond our validated complexity level"

## Best Practices

1. **Ask First**: Always validate scope before detailed planning
2. **Be Honest**: Don't inflate requirements
3. **Start Simple**: Can always add complexity later
4. **Match Needs**: Solution should fit actual use case
5. **Document**: Record validation decisions
6. **Reference**: Use validation to prevent scope creep

## Summary

These 5 essential questions prevent over-engineering by:
- ✅ Validating actual needs
- ✅ Right-sizing solutions
- ✅ Preventing unnecessary complexity
- ✅ Matching architecture to requirements
- ✅ Setting clear scope boundaries

Always validate scope before creating detailed PRDs.

