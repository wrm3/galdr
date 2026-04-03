# PRD Template - Complete 10-Section Structure

## Overview

This document provides the complete Product Requirements Document (PRD) template used in the galdr system. Copy this template and customize for your project.

## Complete PRD Template

```markdown
# PRD: [Project/Feature Title]

## 1. Product overview

### 1.1 Document title and version
- PRD: [Project/Feature Title]
- Version: 1.0
- Date: [YYYY-MM-DD]
- Author: [Name/Team]

### 1.2 Product summary
[2-3 paragraphs providing an overview of the project or feature. Include:
- What problem does this solve?
- Who is this for?
- What is the proposed solution?
- Why now?]

## 2. Goals

### 2.1 Business goals
- [Specific, measurable business objective 1]
- [Specific, measurable business objective 2]
- [Specific, measurable business objective 3]

### 2.2 User goals
- [What users aim to achieve 1]
- [What users aim to achieve 2]
- [What users aim to achieve 3]

### 2.3 Non-goals
- [Explicitly out-of-scope item 1]
- [Explicitly out-of-scope item 2]
- [Explicitly out-of-scope item 3]

## 3. User personas

### 3.1 Key user types
- [Primary user category 1]
- [Primary user category 2]
- [Secondary user category]

### 3.2 Basic persona details
- **[Persona Name 1]**: [Brief description of who they are, their needs, and pain points]
- **[Persona Name 2]**: [Brief description of who they are, their needs, and pain points]

### 3.3 Role-based access
- **[Role Name 1]**: [Description of permissions/access level]
- **[Role Name 2]**: [Description of permissions/access level]

## 4. Features

### 4.1 Core Features

#### Feature 1: [Feature Name] (Priority: High)
- [Requirement 1.1]
- [Requirement 1.2]
- [Requirement 1.3]
- **Reference**: See `features/[feature-name].md`

#### Feature 2: [Feature Name] (Priority: Medium)
- [Requirement 2.1]
- [Requirement 2.2]
- **Reference**: See `features/[feature-name].md`

### 4.2 Feature References
- Each feature has a corresponding document in `features/` folder
- Features are referenced by tasks in TASKS.md
- Bugs reference affected features

## 5. User experience

### 5.1 Entry points & first-time user flow
[How users access this feature/product initially. Include:
- Where do they start?
- What's the onboarding experience?
- First-time user journey]

### 5.2 Core experience
**Step 1**: [Explanation of the first major interaction]
**Step 2**: [Explanation of the second major interaction]
**Step 3**: [Explanation of the third major interaction]

### 5.3 Advanced features & edge cases
- [Less common scenario or advanced capability 1]
- [Less common scenario or advanced capability 2]
- [Edge case handling]

### 5.4 UI/UX highlights
- [Key design principle 1]
- [Key design principle 2]
- [Important user interface element]

## 6. Narrative

[A single paragraph (3-5 sentences) describing the user's journey and the benefit they receive. Tell a story about a specific user using the product to accomplish their goal.]

## 7. Success metrics

### 7.1 User-centric metrics
- [e.g., Task completion rate: Target 90%]
- [e.g., User satisfaction score: Target 4.5/5]
- [e.g., Time to complete core task: Target < 2 minutes]

### 7.2 Business metrics
- [e.g., Conversion rate: Target 15%]
- [e.g., Revenue impact: Target $100K/month]
- [e.g., Cost reduction: Target 30%]

### 7.3 Technical metrics
- [e.g., Page load time: Target < 2 seconds]
- [e.g., Error rate: Target < 0.1%]
- [e.g., API response time: Target < 200ms]

## 8. Technical considerations

### 8.1 Affected subsystems
**Primary subsystems** (directly modified/extended):
- **[Subsystem Name 1]**: [Impact description - what changes, why]
- **[Subsystem Name 2]**: [Impact description - what changes, why]

**Secondary subsystems** (indirectly affected):
- **[Subsystem Name 3]**: [Dependency/integration description]

### 8.2 Integration points
- [Interaction with other systems/services]
- [API dependencies]
- [Third-party service integration]

### 8.3 Data storage & privacy
- [How data is handled]
- [GDPR/CCPA compliance requirements]
- [Data retention policies]
- [Privacy considerations]

### 8.4 Scalability & performance
- [Anticipated load: X users, Y requests/second]
- [Performance targets]
- [Scalability strategy]

### 8.5 Potential challenges
- [Risk or technical hurdle 1]
- [Risk or technical hurdle 2]
- [Mitigation strategies]

## 9. Milestones & sequencing

### 9.1 Project estimate
- **Size**: [Small/Medium/Large]
- **Estimated Duration**: [e.g., 2-4 weeks, 2-3 months]
- **Confidence Level**: [High/Medium/Low]

### 9.2 Team size & composition
- **Team Size**: [e.g., Small Team: 1-2 people]
- **Roles Needed**: [e.g., 1 PM, 1 Engineer, 1 Designer]

### 9.3 Suggested phases

**Phase 1: [Phase Name]** ([Time estimate])
- Key deliverables:
  - [Deliverable 1]
  - [Deliverable 2]
- Success criteria: [How to know phase is complete]

**Phase 2: [Phase Name]** ([Time estimate])
- Key deliverables:
  - [Deliverable 1]
  - [Deliverable 2]
- Success criteria: [How to know phase is complete]

## 10. User stories

### 10.1 [User Story Title 1]
- **ID**: US-001
- **Description**: As a [persona], I want to [action] so that [benefit].
- **Acceptance Criteria**:
  - [Criterion 1.1]
  - [Criterion 1.2]
  - [Criterion 1.3]
- **Priority**: [High/Medium/Low]
- **Estimated Effort**: [Story points or time]

### 10.2 [User Story Title 2]
- **ID**: US-002
- **Description**: As a [persona], I want to [action] so that [benefit].
- **Acceptance Criteria**:
  - [Criterion 2.1]
  - [Criterion 2.2]
- **Priority**: [High/Medium/Low]
- **Estimated Effort**: [Story points or time]

---

## Appendix

### A. Related Documents
- [Link to technical spec]
- [Link to design mockups]
- [Link to market research]

### B. Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial version |

### C. Stakeholders
- **Product Owner**: [Name]
- **Engineering Lead**: [Name]
- **Design Lead**: [Name]
- **Key Stakeholders**: [Names]
```

## Section-by-Section Guidance

### Section 1: Product Overview
**Purpose**: Provide context and high-level summary  
**Length**: 1 page  
**Key Questions**:
- What are we building?
- Why are we building it?
- Who is it for?

### Section 2: Goals
**Purpose**: Define success criteria  
**Length**: 1/2 page  
**Key Questions**:
- What business outcomes do we want?
- What user outcomes do we want?
- What are we explicitly NOT doing?

### Section 3: User Personas
**Purpose**: Understand the users  
**Length**: 1 page  
**Key Questions**:
- Who will use this?
- What are their needs?
- What access levels do they need?

### Section 4: Features
**Purpose**: Detail what we're building  
**Length**: 2-3 pages  
**Key Questions**:
- What features are required?
- What's the priority?
- What are the detailed requirements?

### Section 5: User Experience
**Purpose**: Describe the user journey  
**Length**: 1-2 pages  
**Key Questions**:
- How do users interact with this?
- What's the core workflow?
- What about edge cases?

### Section 6: Narrative
**Purpose**: Tell the story  
**Length**: 1 paragraph  
**Key Questions**:
- What's the user's journey?
- What benefit do they receive?
- How does it feel to use?

### Section 7: Success Metrics
**Purpose**: Define measurable success  
**Length**: 1 page  
**Key Questions**:
- How do we measure user success?
- How do we measure business success?
- What technical metrics matter?

### Section 8: Technical Considerations
**Purpose**: Address implementation details  
**Length**: 1-2 pages  
**Key Questions**:
- What systems are affected?
- What are the technical challenges?
- What about scalability?

### Section 9: Milestones & Sequencing
**Purpose**: Plan the work  
**Length**: 1 page  
**Key Questions**:
- How long will this take?
- What team do we need?
- What are the phases?

### Section 10: User Stories
**Purpose**: Detail specific requirements  
**Length**: 2-3 pages  
**Key Questions**:
- What specific user needs exist?
- What are the acceptance criteria?
- What's the priority?

## Best Practices

1. **Be Specific**: Avoid vague language
2. **Be Measurable**: Include concrete metrics
3. **Be Realistic**: Don't over-promise
4. **Be Complete**: Cover all sections
5. **Be Concise**: Respect the reader's time
6. **Be Clear**: Use simple language
7. **Be Visual**: Include diagrams when helpful

## Common Mistakes to Avoid

❌ **Too Vague**: "Improve user experience"  
✅ **Specific**: "Reduce login time from 5s to 2s"

❌ **Feature List**: Just listing features  
✅ **User-Focused**: Explaining why features matter

❌ **Technical Jargon**: "Implement microservices architecture"  
✅ **Business Value**: "Enable independent team deployment"

❌ **No Metrics**: "Make it better"  
✅ **Measurable**: "Increase conversion by 15%"

## Summary

This PRD template provides a complete structure for documenting product requirements. Use it as a starting point and customize based on your project needs. Remember: a good PRD is specific, measurable, and user-focused.

