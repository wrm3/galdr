---
name: research-methodology
description: Deep research—multi-source gathering, synthesis, citations, competitive and technical dives—not quick lookups.
---

Base directory for this skill: /mnt/c/git/galdr/.cursor/skills/research-methodology

# Deep Research Skill

Conduct comprehensive, multi-step research with iterative workflows to gather, analyze, and synthesize information from multiple sources. Use this skill when users need thorough research, competitive analysis, literature reviews, or deep technical investigation.

## When to Use This Skill

Use the Deep Research skill when the user requests:
- Comprehensive literature reviews
- Technical deep dives into complex topics
- Competitive analysis of tools/frameworks/approaches
- Best practices research
- Problem-solving research requiring multiple sources
- Trend analysis and emerging technology research
- Synthesis of information from multiple sources
- Research reports with citations and references

**Trigger phrases**: "research", "investigate", "compare", "analyze", "best practices", "literature review", "competitive analysis", "deep dive"

## When NOT to Use This Skill

DO NOT use this skill for:
- Simple factual lookups (use WebSearch directly)
- Quick documentation checks (use WebFetch directly)
- Code-specific searches (use Grep/Glob tools)
- User has specific solution in mind (just implement it)
- Time-critical tasks requiring immediate action

## Research Capabilities

This skill provides:
1. **Multi-source information gathering** - Search and fetch from multiple sources
2. **Iterative research workflows** - Refine research based on findings
3. **Source verification** - Evaluate credibility and currency
4. **Information synthesis** - Organize and summarize findings
5. **Citation management** - Properly cite all sources
6. **Research artifacts** - Generate professional research reports
7. **Knowledge organization** - Structure findings by themes

## Core Research Process

### 1. Define Research Objective
**Before starting research:**
- Clarify the research question
- Understand the context and use case
- Determine required depth (quick vs. comprehensive)
- Identify key decision criteria
- Set scope boundaries

**Example objectives**:
- "What are the best practices for React state management?"
- "Compare task management systems for development teams"
- "Research authentication methods for web applications"
- "Investigate solutions to CORS issues in Next.js"

### 2. Plan Research Strategy
**Develop a research approach:**
- Identify key search terms
- Prioritize source types (official docs, articles, forums)
- Determine research breadth vs. depth
- Plan iterative refinement
- Estimate time investment

**Research phases**:
1. **Broad exploration** - Get overview, identify key concepts
2. **Focused investigation** - Deep dive into promising areas
3. **Verification** - Cross-check critical information
4. **Synthesis** - Organize and summarize findings

### 3. Gather Information
**Execute research strategy:**

**Phase 1: Initial Broad Search**
- Use WebSearch with broad terms
- Scan results for authoritative sources
- Identify key concepts and terminology
- Note knowledge gaps

```markdown
**Search query**: "[topic] best practices"
**Goal**: Get overview and identify key themes
**Sources to prioritize**: Official docs, established blogs, recent articles
```

**Phase 2: Deep Dive into Key Sources**
- Use WebFetch to read full content
- Follow promising links
- Read official documentation thoroughly
- Gather specific implementation details

```markdown
**For each promising source:**
1. Fetch full content with WebFetch
2. Extract key points
3. Note quotes for citation
4. Identify related topics to explore
```

**Phase 3: Verify and Cross-Reference**
- Check multiple sources for consensus
- Verify technical claims
- Note conflicting information
- Check publication dates for currency

### 4. Evaluate Sources
**Assess source quality using criteria:**

**Tier 1: Authoritative (Highest Priority)**
- Official documentation
- Project repositories (README, docs)
- Academic papers
- Industry standards bodies

**Tier 2: Expert Content (High Priority)**
- Established technical blogs
- Conference talks/videos
- Books from recognized authors
- Technical publications

**Tier 3: Community Content (Medium Priority)**
- Stack Overflow discussions
- Reddit technical subreddits
- GitHub issues/discussions
- Community forums

**Tier 4: General Content (Use with Caution)**
- Personal blogs (unknown authors)
- Medium articles (variable quality)
- Forum posts (unverified)
- AI-generated content

**Red flags**:
- No author information
- Outdated publication date
- No sources/citations
- Promotional content
- Factual errors

### 5. Analyze and Synthesize
**Organize findings into coherent insights:**

**Thematic Organization**
- Group related findings by theme
- Identify patterns and trends
- Note consensus vs. disagreement
- Highlight key insights

**Analysis Framework**
For each major finding:
- **What**: Describe the approach/concept
- **Why**: Explain the rationale
- **Pros**: List advantages
- **Cons**: List disadvantages
- **When**: Identify use cases
- **How**: Provide implementation guidance

**Synthesis Questions**
- What are the common themes?
- Where is there consensus?
- What are the trade-offs?
- What are the emerging trends?
- What gaps remain?

### 6. Document Research
**Create professional research artifacts:**

**Research Report Structure**
1. **Executive Summary** - Key findings in 2-3 paragraphs
2. **Research Objective** - What question we answered
3. **Methodology** - How research was conducted
4. **Findings** - Organized by theme with citations
5. **Analysis** - Synthesis and insights
6. **Recommendations** - Actionable guidance
7. **Gaps and Limitations** - What's unknown
8. **References** - Complete source list

**Citation Format**
```markdown
[Finding description] [1]

## References
1. [Title] - [Author/Source] ([Date]) - [URL] - Accessed [Date]
```

**Save Research Artifacts**
- Save to `docs/research/[topic-name].md`
- Create knowledge base entry if valuable
- Link from relevant task files
- Store for future reference

### 7. Iterative Refinement
**Research is iterative - refine based on findings:**

**After initial research:**
- Review findings for gaps
- Identify areas needing deeper investigation
- Follow up on promising leads
- Verify critical claims

**Refinement triggers**:
- Important details missing
- Conflicting information found
- New concepts discovered
- Additional context needed

**When to stop researching**:
- Research question answered
- Sufficient information for decision
- Diminishing returns on additional research
- Time constraints require moving forward

## Research Workflows

### Workflow 1: Literature Review
**Purpose**: Systematic review of available information on a topic

**Process**:
1. **Define scope** - What specific question or topic?
2. **Broad search** - Get overview of landscape
3. **Identify key sources** - Find most authoritative content
4. **Deep reading** - Thoroughly review key sources
5. **Extract findings** - Note key points with citations
6. **Organize by themes** - Group related information
7. **Synthesize** - What do findings mean collectively?
8. **Document gaps** - What's missing or unclear?
9. **Generate report** - Create structured summary

**Output**: Literature review document with thematic organization

**Example**: "Research best practices for API design"

### Workflow 2: Technical Deep Dive
**Purpose**: Comprehensive understanding of technical topic

**Process**:
1. **Define technical question** - What do we need to understand?
2. **Find official docs** - Start with authoritative sources
3. **Understand fundamentals** - Core concepts and terminology
4. **Explore approaches** - Different ways to solve/implement
5. **Compare options** - Pros, cons, trade-offs
6. **Review examples** - Real-world implementations
7. **Identify pitfalls** - Common mistakes and issues
8. **Document best practices** - Recommended approaches
9. **Provide guidance** - Specific recommendations for use case

**Output**: Technical research document with implementation guidance

**Example**: "Deep dive into React state management options"

### Workflow 3: Competitive Analysis
**Purpose**: Compare multiple solutions/tools/approaches

**Process**:
1. **Identify options** - What are we comparing?
2. **Research each option** - Gather information on each
3. **Define comparison criteria** - What matters for decision?
4. **Create comparison matrix** - Structured comparison
5. **Analyze strengths/weaknesses** - Detailed assessment
6. **Evaluate use cases** - When to use each option
7. **Consider trade-offs** - What are the compromises?
8. **Factor in constraints** - Cost, licensing, complexity, etc.
9. **Provide recommendation** - Best choice for use case

**Output**: Competitive analysis with comparison matrix and recommendation

**Example**: "Compare task management systems for dev teams"

### Workflow 4: Problem-Solving Research
**Purpose**: Find solution to specific technical problem

**Process**:
1. **Understand problem** - Clarify the specific issue
2. **Search for solutions** - Look for existing answers
3. **Review multiple approaches** - Don't stop at first result
4. **Evaluate solutions** - Which ones are viable?
5. **Consider trade-offs** - Pros/cons of each approach
6. **Verify solution** - Check if it actually works
7. **Adapt to context** - How does it apply to our case?
8. **Document solution** - Clear implementation steps
9. **Note alternatives** - Other options if primary fails

**Output**: Solution document with implementation steps and alternatives

**Example**: "Research solutions to CORS issues in Next.js API routes"

### Workflow 5: Best Practices Research
**Purpose**: Identify industry standards and recommended approaches

**Process**:
1. **Define scope** - What practices are we researching?
2. **Find authoritative sources** - Official guidelines, experts
3. **Identify common patterns** - What do experts recommend?
4. **Understand rationale** - Why these practices?
5. **Note variations** - Different contexts, different practices
6. **Check currency** - Are these still current?
7. **Synthesize guidelines** - Core principles
8. **Provide examples** - Concrete illustrations
9. **Document exceptions** - When to deviate

**Output**: Best practices guide with rationale and examples

**Example**: "Research best practices for error handling in Node.js"

### Workflow 6: Trend Analysis
**Purpose**: Identify emerging patterns and technologies

**Process**:
1. **Define focus area** - What trends are we tracking?
2. **Search recent content** - Last 6-12 months
3. **Identify signals** - What's gaining attention?
4. **Track adoption** - Who's using/discussing?
5. **Assess maturity** - Early stage or production-ready?
6. **Evaluate impact** - How significant?
7. **Note trade-offs** - Advantages vs. risks
8. **Predict trajectory** - Where is this heading?
9. **Provide guidance** - Should we adopt? When?

**Output**: Trend analysis with adoption recommendation

**Example**: "Research emerging trends in web application architecture"

## Research Quality Criteria

### Thoroughness
- [ ] Multiple sources consulted (minimum 3-5 for comprehensive research)
- [ ] Official documentation reviewed
- [ ] Multiple perspectives considered
- [ ] Key concepts understood
- [ ] Alternative approaches explored
- [ ] Edge cases considered

### Accuracy
- [ ] Information cross-verified from multiple sources
- [ ] Sources are credible and authoritative
- [ ] Publication dates checked (prefer recent)
- [ ] Technical claims verified
- [ ] Conflicting information addressed
- [ ] Confidence levels noted

### Organization
- [ ] Findings organized by clear themes
- [ ] Logical structure and flow
- [ ] Easy to navigate and understand
- [ ] Key points highlighted
- [ ] Summary provided
- [ ] References properly formatted

### Actionability
- [ ] Clear recommendations provided
- [ ] Trade-offs explained
- [ ] Use cases identified
- [ ] Implementation guidance included
- [ ] Next steps outlined
- [ ] Gaps and limitations noted

### Documentation
- [ ] All sources properly cited
- [ ] Research artifact created
- [ ] Saved to appropriate location
- [ ] Accessible for future reference
- [ ] Professional presentation
- [ ] Complete and self-contained

## Tools and Integration

### Web Search and Fetching
```markdown
**Initial broad search:**
Use WebSearch tool with broad query
Goal: Get overview, identify key sources

**Deep content reading:**
Use WebFetch tool with promising URLs
Goal: Extract detailed information

**Follow-up searches:**
Use WebSearch with refined queries
Goal: Fill gaps, verify claims
```

### File System
```markdown
**Save research artifacts:**
Location: docs/research/[topic-name].md
Purpose: Preserve findings for future reference

**Create knowledge base (optional):**
Location: .galdr/knowledge/
Purpose: Build organizational knowledge base

**Link from tasks:**
Reference research in relevant task files
Purpose: Provide context for implementation
```

### Task Management Integration
```markdown
**Create research tasks:**
When research is substantial, track as task
Status: pending → in-progress → completed

**Document findings in task notes:**
Add key insights to task implementation notes
Purpose: Inform implementation decisions

**Link research to features:**
Connect research to feature planning
Purpose: Evidence-based feature development
```

## Research Best Practices

### Start with the Right Question
- Make research objective specific and clear
- Understand the decision or action research will inform
- Set appropriate scope (don't over-research)
- Know success criteria upfront

### Prioritize Authoritative Sources
- Always start with official documentation
- Trust established experts over unknown bloggers
- Prefer recent content over outdated information
- Cross-verify important claims

### Balance Breadth and Depth
- Start broad to get landscape
- Go deep on most relevant areas
- Don't get lost in tangents
- Know when you have enough

### Document as You Go
- Take notes during research
- Capture source URLs immediately
- Note key quotes for citation
- Organize findings continuously

### Be Skeptical and Verify
- Don't trust single sources for important decisions
- Check publication dates
- Verify technical claims when possible
- Note confidence levels

### Synthesize, Don't Just Collect
- Organize findings by themes
- Identify patterns and insights
- Explain what findings mean
- Provide actionable recommendations

### Know When to Stop
- Research has diminishing returns
- Perfect information is impossible
- Balance research with action
- Make decisions with "good enough" information

## Output Templates

### Literature Review Template
Available at: `templates/literature_review.md`

Use for: Comprehensive review of available information

### Technical Deep Dive Template
Available at: `templates/technical_deep_dive.md`

Use for: Detailed technical investigation

### Competitive Analysis Template
Available at: `templates/competitive_analysis.md`

Use for: Comparing multiple options

### Research Report Template
Available at: `templates/research_report.md`

Use for: General research documentation

## Example Research Outputs

### Example 1: Literature Review
See: `examples/example_literature_review.md`

Topic: React State Management Best Practices

Demonstrates: Thematic organization, multiple sources, synthesis

### Example 2: Technical Deep Dive
See: `examples/example_technical_deep_dive.md`

Topic: Authentication Methods for Web Applications

Demonstrates: Technical analysis, comparison, recommendations

## Common Pitfalls to Avoid

### Over-Researching
**Problem**: Spending excessive time on research, paralysis by analysis

**Solution**: Set time limits, define "good enough", focus on decision-making

### Single-Source Bias
**Problem**: Relying on one source, missing alternative perspectives

**Solution**: Always consult multiple sources, cross-verify claims

### Outdated Information
**Problem**: Using obsolete information, deprecated approaches

**Solution**: Check publication dates, prioritize recent content

### Poor Source Evaluation
**Problem**: Treating all sources as equally credible

**Solution**: Use source quality tiers, prioritize authoritative sources

### Lack of Synthesis
**Problem**: Just listing findings without analysis

**Solution**: Organize by themes, identify patterns, provide insights

### Missing Citations
**Problem**: Not documenting sources, can't verify claims

**Solution**: Cite all sources, include URLs and dates

### Scope Creep
**Problem**: Research expands beyond original question

**Solution**: Regularly check against research objective, stay focused

### No Actionable Output
**Problem**: Research doesn't inform decision or action

**Solution**: Always end with clear recommendations and next steps

## Research Workflow Examples

### Example: User asks "What's the best way to handle authentication in my Next.js app?"

**Step 1: Define objective**
Research authentication solutions for Next.js applications, compare options, recommend best approach for user's use case.

**Step 2: Broad search**
```
WebSearch: "Next.js authentication best practices 2025"
Goal: Overview of current approaches
```

**Step 3: Identify key options**
From initial search, identify main approaches:
- NextAuth.js
- Auth0
- Clerk
- Supabase Auth
- Custom JWT implementation

**Step 4: Deep dive on each**
Use WebFetch to read:
- Official documentation for each
- Comparison articles
- Implementation examples

**Step 5: Create comparison matrix**
| Solution | Pros | Cons | Use Cases | Cost |
|----------|------|------|-----------|------|
| NextAuth.js | Free, flexible, self-hosted | Setup complexity | Full control needed | Free |
| Auth0 | Feature-rich, easy setup | Expensive at scale | Enterprise apps | Paid tiers |
| ... | ... | ... | ... | ... |

**Step 6: Provide recommendation**
Based on user's context (if known):
- Startup/small app → NextAuth.js or Clerk
- Enterprise → Auth0 or Okta
- Simple use case → Supabase Auth

**Step 7: Document findings**
Save to `docs/research/nextjs-authentication-comparison.md`

**Step 8: Provide actionable response**
"Based on comprehensive research, here are the main authentication options for Next.js, with recommendations based on your use case..."

## Success Metrics

Research is successful when:
- Research question is clearly answered
- Multiple credible sources consulted
- Information is current and accurate
- Findings are well-organized
- Synthesis provides insights beyond raw info
- Recommendations are actionable
- All sources properly cited
- Output is professional and useful
- Appropriate depth for decision importance
- Completed in reasonable time

## Integration with Other Skills

### with galdr-task-management
- Create research tasks for substantial research efforts
- Track research progress
- Document findings in task notes
- Link research to implementation tasks

### with galdr-planning
- Use research to inform feature planning
- Include research findings in PRDs
- Base technical decisions on research
- Identify risks through research

### With web-tools skill
- Use web-tools for initial searches
- Delegate heavy web scraping to web-tools
- Coordinate browser automation for research
- Leverage web-tools screenshots for documentation

### With other development skills
- Research informs architecture decisions
- Provides context for implementation
- Identifies best practices to follow
- Discovers solutions to technical challenges

## Notes for Claude

When this skill is activated:
1. Confirm you understand the research objective
2. Clarify scope and required depth with user
3. Follow appropriate research workflow
4. Use WebSearch and WebFetch tools extensively
5. Organize findings as you go
6. Synthesize insights, don't just list findings
7. Always cite sources properly
8. Create research artifacts in docs/research/
9. Provide clear recommendations
10. Know when research is sufficient

**Balance**: Be thorough but efficient. Match research depth to decision importance. Don't over-research trivial questions.

**Quality**: Prioritize authoritative sources, cross-verify claims, note confidence levels, document gaps.

**Output**: Create professional research reports that inform decisions and actions.
