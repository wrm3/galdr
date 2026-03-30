# Example: Complex Task with Sub-Task Expansion

**This example demonstrates how a complex task is scored, then broken down into sub-tasks using the galdr workflow system.**

---

## Parent Task File: `task142_implement_auth_system.md`

```yaml
---
id: 142
title: 'Implement User Authentication System'
type: task
status: pending
priority: high
phase: 1
subsystems: [auth, database, api, frontend]
project_context: 'Enables secure user access to the application, required for all user-specific features. Supports the project goal of multi-user collaboration.'
dependencies: [100, 101]
complexity_score: 13
---
```

# Task 142: Implement User Authentication System

## Objective
Implement a complete user authentication system including registration, login, password reset, and session management. The system must be secure, scalable, and provide a foundation for role-based access control.

## Complexity Assessment
**Score: 13/10 — MANDATORY EXPANSION**

| Factor | Points | Reason |
|--------|--------|--------|
| Estimated Effort | 4 | 5-7 days exceeds the 2-3 day threshold |
| Cross-Subsystem Impact | 3 | Affects auth, database, api, and frontend |
| Multiple Components | 3 | Registration, login, password reset, sessions |
| High Uncertainty | 2 | Security best practices require research |
| Multiple Outcomes | 2 | 4 distinct, verifiable deliverables |
| **Total** | **14** | **Mandatory expansion** |

## Sub-Tasks

| Sub-Task File | Title | Status |
|---------------|-------|--------|
| `task142-1_setup_auth_database.md` | Setup authentication database schema | [ ] |
| `task142-2_password_hashing.md` | Implement secure password hashing | [ ] |
| `task142-3_auth_api_endpoints.md` | Create auth REST API endpoints | [ ] |
| `task142-4_frontend_auth_ui.md` | Build login and registration UI | [ ] |
| `task142-5_session_management.md` | Implement secure session handling | [ ] |
| `task142-6_password_reset_flow.md` | Email-based password reset | [ ] |
| `task142-7_protect_api_routes.md` | Apply auth middleware to API routes | [ ] |
| `task142-8_security_testing.md` | Security audit and penetration testing | [ ] |

> **Sub-task ID convention**: Use `142-1` (hyphen), not `142.1` (dot).
> Sub-task files are named `task{parent}-{sub}_{description}.md`

## Acceptance Criteria
- [ ] Users can register with email and password
- [ ] Users can login with valid credentials
- [ ] Users can reset forgotten passwords via email
- [ ] Sessions are securely managed (JWT with expiry)
- [ ] Password complexity requirements enforced
- [ ] API routes protected by authentication middleware
- [ ] Login/register frontend UI complete
- [ ] OWASP authentication guidelines followed

## Implementation Notes
- Use bcrypt for password hashing (minimum 12 rounds)
- Implement JWT tokens for stateless session management
- Follow OWASP Top 10 security guidelines
- Add rate limiting to prevent brute force (5 attempts/minute per IP)
- Use HTTPS for all authentication endpoints
- Store refresh tokens in HttpOnly cookies

---

## Sub-Task Example: `task142-1_setup_auth_database.md`

```yaml
---
id: "142-1"
title: 'Setup Authentication Database Schema'
type: task
status: pending
priority: high
phase: 1
parent_task: 142
subsystems: [database, auth]
project_context: 'Creates the database foundation for user authentication, storing user accounts, hashed passwords, and session data.'
dependencies: [100]
---
```

# Task 142-1: Setup Authentication Database Schema

## Objective
Design and implement database tables for user authentication: users, sessions, and password reset tokens.

## Acceptance Criteria
- [ ] `users` table created (id, email, password_hash, created_at, updated_at, deleted_at)
- [ ] `sessions` table created (id, user_id, token, expires_at, created_at)
- [ ] `password_reset_tokens` table created (id, user_id, token, expires_at, used, created_at)
- [ ] Appropriate indexes created for query performance
- [ ] Foreign key constraints established
- [ ] Database migrations written and tested (up and down)
- [ ] Schema documented in SUBSYSTEMS.md

## Database Schema

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL  -- soft delete
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_reset_tokens_token ON password_reset_tokens(token);
```

---

## Sub-Task Example: `task142-3_auth_api_endpoints.md`

```yaml
---
id: "142-3"
title: 'Create Authentication API Endpoints'
type: task
status: pending
priority: high
phase: 1
parent_task: 142
subsystems: [api, auth]
project_context: 'REST API endpoints for user registration, login, logout, and password reset. Enables frontend to interact with the authentication system.'
dependencies: ["142-1", "142-2", 101]
---
```

# Task 142-3: Create Authentication API Endpoints

## Objective
Implement REST API endpoints for user authentication.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | New user registration |
| POST | `/api/auth/login` | User login, returns JWT |
| POST | `/api/auth/logout` | Invalidate session |
| POST | `/api/auth/refresh` | Refresh JWT token |
| POST | `/api/auth/reset-password` | Request password reset email |
| POST | `/api/auth/reset-password/confirm` | Confirm reset with token |

## Acceptance Criteria
- [ ] All 6 endpoints implemented
- [ ] Input validation on all endpoints (email format, password strength)
- [ ] Proper HTTP status codes (200, 201, 400, 401, 422, 429)
- [ ] Rate limiting: 5 requests/minute per IP on login
- [ ] API documentation updated (OpenAPI spec)
- [ ] Unit tests for all endpoints

### POST /api/auth/login — Request/Response

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "expires_at": "2026-01-28T12:00:00Z"
}
```

**Response (401):**
```json
{
  "error": "invalid_credentials",
  "message": "Email or password is incorrect"
}
```

---

**This example demonstrates:**
1. **Complexity Scoring**: Task scored 14 points, triggering mandatory expansion
2. **Sub-Task Format**: `142-1` hyphen notation (never `142.1`)
3. **Sub-Task Files**: Named `task{parent}-{sub}_{description}.md`
4. **Dependency Chain**: Sub-tasks can depend on other sub-tasks (`142-3` depends on `142-1` and `142-2`)
5. **Parent Task**: Summarizes all sub-tasks and holds the overall acceptance criteria
