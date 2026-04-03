Perform code review: $ARGUMENTS

## What This Command Does

Performs a comprehensive code review focusing on quality, security, and best practices.

## Review Focus Areas

### 1. Code Quality
- Readability and maintainability
- Adherence to project conventions
- Proper error handling
- Code organization and structure
- DRY principle compliance
- Naming conventions

### 2. Functionality
- Logic correctness
- Edge case handling
- Input validation
- Expected behavior verification
- Null/undefined handling

### 3. Performance
- Algorithm efficiency (O notation)
- Resource usage (memory, CPU)
- Database query optimization
- Caching opportunities
- Unnecessary re-renders (React)

### 4. Security
- Input sanitization
- Authentication/authorization
- Sensitive data handling
- SQL injection prevention
- XSS prevention
- CSRF protection

### 5. Testing
- Test coverage adequacy
- Test quality and meaningfulness
- Missing test scenarios
- Edge case tests

### 6. Documentation
- Code comments for complex logic
- API documentation
- README updates if needed
- Type definitions (TypeScript)

## Review Output Format

### 🔴 Critical Issues (Must Fix)
Issues that could cause bugs, security vulnerabilities, or major problems.
```
Location: file.py:42
Issue: SQL injection vulnerability
Fix: Use parameterized queries
```

### 🟡 Important Issues (Should Fix)
Issues that impact maintainability or best practices.
```
Location: file.py:87
Issue: Missing error handling
Fix: Add try/catch block
```

### 🟢 Suggestions (Nice to Have)
Improvements that would enhance code quality.
```
Location: file.py:123
Suggestion: Extract to helper function
Reason: Improves readability
```

### ✅ Positive Notes
What was done well (to encourage good practices).

## What I Need From You
- File or directory to review
- Specific concerns to focus on (optional)
- Context about the changes (optional)

Let's review this code!
