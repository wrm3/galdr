# Planning Questionnaire - 27 Questions

## Overview

This comprehensive 27-question framework helps gather complete requirements before creating a PRD. Use this to prevent over-engineering and ensure appropriate scope.

## How to Use

1. **Ask questions in order** - They build on each other
2. **Listen carefully** - Follow-up based on responses
3. **Document answers** - Use them in PRD creation
4. **Adjust scope** - Based on responses, right-size the solution

## Phase 1: Project Context (Q1-Q7)

### Q1: Primary Problem
**Question**: "What is the primary problem this system solves?"  
**Follow-up**: "Who experiences this problem? How is it handled today?"  
**Purpose**: Understand the core need  
**PRD Section**: Product Overview, Goals

### Q2: Success Definition
**Question**: "What does success look like for this project?"  
**Follow-up**: "How will you measure it? What would indicate failure?"  
**Purpose**: Define measurable outcomes  
**PRD Section**: Success Metrics

### Q3: New vs Replacement
**Question**: "Are you replacing an existing system or creating something new?"  
**Follow-up if Replacing**: "What are the pain points with the current system?"  
**Follow-up if New**: "Why is this needed now? What changed?"  
**Purpose**: Understand context and constraints  
**PRD Section**: Product Overview, Technical Considerations

### Q4: Primary Users
**Question**: "Who are the primary users?"  
**Options**: End users, Admins, Stakeholders, External parties  
**Purpose**: Identify user personas  
**PRD Section**: User Personas

### Q5: User Count
**Question**: "How many users will this have?"  
**Options**: Single, 2-10, 11-50, 51-200, 200+  
**Purpose**: Determine scale requirements  
**PRD Section**: Technical Considerations, Scalability

### Q6: Usage Frequency
**Question**: "How often will this be used?"  
**Options**: Occasional, Daily, Continuous, Peak periods  
**Purpose**: Understand usage patterns  
**PRD Section**: Technical Considerations, Performance

### Q7: Access Locations
**Question**: "Where will users access this from?"  
**Options**: Local machine, Office network, Remote, Internet, Mobile  
**Purpose**: Determine deployment strategy  
**PRD Section**: Technical Considerations

## Phase 2: Technical Requirements (Q8-Q16)

### Q8: Deployment Preference
**Question**: "Where should this be deployed?"  
**Options**: Local desktop, Local server, Cloud, Hybrid, No preference  
**Purpose**: Determine infrastructure needs  
**PRD Section**: Technical Considerations

### Q9: Maintenance Comfort
**Question**: "What's your comfort level with system maintenance?"  
**Options**: Minimal (set and forget), Basic (occasional updates), Intermediate (regular maintenance), Advanced (full control)  
**Purpose**: Determine complexity level  
**PRD Section**: Technical Considerations

### Q10: Integration Needs
**Question**: "What systems does this need to integrate with?"  
**Examples**: Active Directory, Databases, Business applications, Monitoring tools, Backup systems  
**Purpose**: Identify integration points  
**PRD Section**: Integration Points

### Q11: Data Types
**Question**: "What types of data will this handle?"  
**Options**: Public, Internal, PII, Financial, Healthcare, Regulated  
**Purpose**: Determine security requirements  
**PRD Section**: Data Storage & Privacy

### Q12: Security Requirements
**Question**: "What security requirements do you have?"  
**Options**: Basic, Industry compliance (SOC2, ISO), Government (FedRAMP), Custom requirements, None specific  
**Purpose**: Define security posture  
**PRD Section**: Data Storage & Privacy

### Q13: Access Control
**Question**: "How should access be controlled?"  
**Options**: All users see everything, Role-based, Department-based, Individual permissions, External user access  
**Purpose**: Determine authorization model  
**PRD Section**: User Personas, Role-based Access

### Q14: Performance Expectations
**Question**: "What are your performance expectations?"  
**Options**: Basic (seconds acceptable), Good (< 1 second), High (instant), Not critical  
**Purpose**: Set performance targets  
**PRD Section**: Success Metrics, Technical Metrics

### Q15: Data Volume
**Question**: "How much data will this handle?"  
**Options**: Thousands of records, Hundreds of thousands, Millions, Billions, Growing rapidly  
**Purpose**: Determine scalability needs  
**PRD Section**: Scalability & Performance

### Q16: Peak Usage
**Question**: "When will usage peak?"  
**Options**: Consistent, Business hours, Month/quarter end, Seasonal, Event-driven  
**Purpose**: Plan for capacity  
**PRD Section**: Scalability & Performance

## Phase 3: Feature Scope (Q17-Q22)

### Q17: Essential Features (MVP)
**Question**: "What features are absolutely essential?"  
**Follow-up**: "What are the deal-breakers? What can't you live without?"  
**Purpose**: Define MVP scope  
**PRD Section**: Features (Core Features)

### Q18: Nice-to-Have Features
**Question**: "What features would be nice to have but aren't essential?"  
**Follow-up**: "What would make this great vs just good?"  
**Purpose**: Identify future enhancements  
**PRD Section**: Features, Non-goals

### Q19: Features to Avoid
**Question**: "Are there features you explicitly want to avoid?"  
**Follow-up**: "Any complexity you don't want? Specific integrations to avoid?"  
**Purpose**: Prevent scope creep  
**PRD Section**: Non-goals

### Q20: Ease vs Power
**Question**: "What's more important: ease of use or powerful features?"  
**Options**: Ease (simple, intuitive), Power (feature-rich, flexible), Balanced, Depends on user type  
**Purpose**: Guide UX decisions  
**PRD Section**: User Experience

### Q21: Interface Examples
**Question**: "Are there any interfaces or applications you like?"  
**Follow-up**: "What do you like about them? Any patterns to follow?"  
**Purpose**: Understand UX preferences  
**PRD Section**: UI/UX Highlights

### Q22: User Training
**Question**: "How much training are users willing to invest?"  
**Options**: Self-explanatory (no training), Brief tutorial, Formal training, Complex is OK  
**Purpose**: Determine UX complexity  
**PRD Section**: User Experience

## Phase 4: Timeline & Resources (Q23-Q27)

### Q23: Timeline Drivers
**Question**: "What's driving the timeline?"  
**Options**: Business deadline, Budget constraints, Competition, Regulatory requirement, Personal goal  
**Purpose**: Understand urgency  
**PRD Section**: Milestones & Sequencing

### Q24: Delivery Preference
**Question**: "How would you prefer to receive this?"  
**Options**: Quick prototype (iterate), Phased delivery (incremental), Complete solution (all at once), Iterative (continuous)  
**Purpose**: Determine delivery approach  
**PRD Section**: Milestones & Sequencing

### Q25: Trade-offs
**Question**: "If you had to choose, what's most important?"  
**Options**: Core features over polish, Polish over features, Speed over performance, Performance over speed  
**Purpose**: Understand priorities  
**PRD Section**: Goals, Milestones

### Q26: Available Resources
**Question**: "What resources are available?"  
**Examples**: Development time, Technical expertise, Budget, Third-party services  
**Purpose**: Assess feasibility  
**PRD Section**: Team Size & Composition

### Q27: Hard Constraints
**Question**: "Are there any hard constraints?"  
**Examples**: Must use specific technology, Cannot use cloud, Budget limits, Compliance policies  
**Purpose**: Identify non-negotiables  
**PRD Section**: Technical Considerations, Potential Challenges

## Using the Responses

### Creating the PRD

Map questionnaire responses to PRD sections:

| Questions | PRD Section |
|-----------|-------------|
| Q1-Q3 | Product Overview, Goals |
| Q4-Q7 | User Personas |
| Q8-Q16 | Technical Considerations |
| Q17-Q22 | Features, User Experience |
| Q23-Q27 | Milestones & Sequencing |

### Scope Validation

Use responses to validate scope:

**Personal Use (1 user)**:
- Simple, file-based solutions
- Minimal security
- Basic features only

**Small Team (2-10)**:
- Basic sharing capabilities
- Simple user management
- Standard features

**Broader Deployment (10+)**:
- Full authentication
- Role management
- Comprehensive features
- Scalability planning

### Over-Engineering Prevention

Red flags from responses:
- ❌ Single user but asking for role-based access
- ❌ Occasional use but wanting real-time features
- ❌ Minimal maintenance but complex architecture
- ❌ Small data volume but asking for clustering

Right-sizing based on responses:
- ✅ Match complexity to actual needs
- ✅ Start simple, add complexity as needed
- ✅ Focus on essential features first
- ✅ Defer nice-to-haves

## Example Session

**Q1**: "What problem does this solve?"  
**A**: "We need to track customer support tickets"

**Q5**: "How many users?"  
**A**: "About 5 support agents"

**Q17**: "Essential features?"  
**A**: "Create tickets, assign to agents, track status"

**Conclusion**: Small team ticket system, basic features, simple deployment

## Best Practices

1. **Ask all questions** - Don't skip based on assumptions
2. **Listen actively** - Follow-up based on responses
3. **Document thoroughly** - Use responses in PRD
4. **Validate scope** - Ensure solution matches needs
5. **Prevent over-engineering** - Right-size the solution

## Summary

This 27-question framework ensures comprehensive requirements gathering while preventing over-engineering. Use it to create well-scoped, appropriate PRDs that match actual needs.

