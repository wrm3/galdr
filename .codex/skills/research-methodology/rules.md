# Deep Research Skill - Rules and Guidelines

## Core Research Principles

### 1. Always Verify Information
- NEVER rely on a single source for important decisions
- Cross-reference claims from multiple credible sources
- Check publication dates - prefer recent information
- Verify technical claims when possible
- Note confidence levels for assertions

### 2. Prioritize Source Quality
**Source Hierarchy (use in order)**:
1. Official documentation
2. Project repositories and READMEs
3. Academic papers and technical publications
4. Established technical blogs and experts
5. Community content (Stack Overflow, Reddit)
6. General blogs and forums (use with caution)

**Red Flags for Sources**:
- No author or publication date
- Outdated content (>2-3 years for technical topics)
- No citations or references
- Promotional/marketing content
- Factual errors or inconsistencies
- AI-generated content without verification

### 3. Be Thorough but Efficient
- Match research depth to decision importance
- Don't over-research trivial questions
- Know when you have "good enough" information
- Balance breadth (overview) with depth (details)
- Research has diminishing returns - know when to stop

### 4. Synthesize, Don't Just Collect
- Organize findings by clear themes
- Identify patterns and common recommendations
- Explain what findings mean collectively
- Highlight consensus vs. disagreement
- Provide insights beyond raw information
- Always end with actionable recommendations

### 5. Document Everything
- Cite ALL sources with URL and access date
- Save research artifacts to docs/research/
- Create professional, well-organized outputs
- Make research accessible for future reference
- Include executive summary for quick understanding

## Research Process Rules

### Before Starting Research
1. **Clarify the objective**: Confirm exactly what needs to be researched
2. **Understand context**: Know how research will be used
3. **Set scope**: Define boundaries to prevent scope creep
4. **Estimate depth**: Quick overview vs. comprehensive analysis
5. **Confirm with user**: Make sure you understand the need

### During Research
1. **Start broad**: Get overview before deep diving
2. **Follow authoritative sources first**: Official docs before blogs
3. **Take notes continuously**: Don't try to remember everything
4. **Capture citations immediately**: URL, title, author, date
5. **Organize as you go**: Group findings by themes
6. **Check for gaps**: Note what's missing or unclear
7. **Verify critical claims**: Cross-check important information
8. **Stay focused**: Keep research objective in mind

### After Research
1. **Synthesize findings**: Organize into coherent insights
2. **Provide recommendations**: Clear, actionable guidance
3. **Note limitations**: What's unknown or uncertain
4. **Create artifact**: Professional research document
5. **Save for reference**: Store in docs/research/
6. **Link to tasks**: Connect research to implementation work

## Citation Rules

### Always Cite Sources
Every significant fact, claim, or recommendation must have a citation.

**Citation Format**:
```markdown
[Finding or claim] [1]

## References
1. [Title] - [Author/Organization] ([Date]) - [URL] - Accessed [Access Date]
```

**Example**:
```markdown
NextAuth.js is the most popular authentication library for Next.js applications [1].

## References
1. "Getting Started with NextAuth.js" - NextAuth.js Documentation (2025-01-15) - https://next-auth.js.org/getting-started - Accessed 2025-10-20
```

### What to Cite
- Direct quotes (always)
- Specific facts and statistics
- Technical claims
- Recommendations and best practices
- Code examples (if substantial)
- Architectural patterns
- Performance data

### What Doesn't Need Citation
- General knowledge (e.g., "JavaScript is a programming language")
- Your own analysis and synthesis
- Logical conclusions from multiple sources
- Common patterns visible across many sources

## Source Evaluation Rules

### Evaluate Every Source
Before using information from a source, assess:

**Authority**:
- Who is the author? Are they qualified?
- Is this official documentation?
- Is the organization reputable?

**Currency**:
- When was it published?
- Is it still current?
- Have there been updates since?

**Accuracy**:
- Are facts verifiable?
- Are there citations?
- Do other sources agree?

**Purpose**:
- Educational vs. promotional?
- Objective vs. biased?
- Comprehensive vs. superficial?

### Handling Conflicting Information
When sources disagree:
1. Note the conflict explicitly
2. Evaluate source credibility
3. Look for additional sources
4. Consider context (different use cases)
5. Explain the nuance in your synthesis
6. Provide balanced perspective

## Research Depth Guidelines

### Quick Research (15-30 minutes)
**When**: Simple questions, low-stakes decisions, preliminary investigation

**Process**:
- 1-2 broad searches
- Read 3-5 top sources
- Quick synthesis
- Brief recommendations

**Output**: 1-2 paragraphs with key findings and sources

### Standard Research (1-2 hours)
**When**: Moderate complexity, typical technical decisions, feature planning

**Process**:
- Multiple search queries
- Read 5-10 sources in detail
- Follow key links
- Thematic organization
- Comprehensive synthesis

**Output**: Structured research document (2-5 pages)

### Deep Research (3+ hours)
**When**: Critical decisions, major features, strategic planning, complex topics

**Process**:
- Extensive multi-source research
- Official docs thoroughly reviewed
- Multiple approaches compared
- Verification and cross-checking
- Detailed analysis
- Professional report

**Output**: Comprehensive research report (5+ pages) with executive summary

## Workflow Selection Rules

### Use Literature Review When:
- User wants overview of topic
- Comprehensive knowledge needed
- Multiple perspectives valuable
- Building knowledge base

### Use Technical Deep Dive When:
- Need detailed understanding
- Implementation decisions needed
- Technical complexity high
- Multiple approaches exist

### Use Competitive Analysis When:
- Comparing specific tools/frameworks
- "Which one should we use?" questions
- Need structured comparison
- Decision criteria clear

### Use Problem-Solving Research When:
- Specific technical problem
- Need solution quickly
- Multiple potential solutions
- Implementation details needed

### Use Best Practices Research When:
- "How should we do X?" questions
- Quality/standards focus
- Team alignment needed
- Establishing guidelines

### Use Trend Analysis When:
- "What's new/emerging?" questions
- Strategic planning
- Future-proofing decisions
- Innovation exploration

## Quality Control Rules

### Minimum Quality Standards
Every research output must have:
- [ ] Clear research objective stated
- [ ] Multiple sources consulted (minimum 3)
- [ ] Authoritative sources prioritized
- [ ] All sources properly cited
- [ ] Findings organized by themes
- [ ] Synthesis and insights provided
- [ ] Actionable recommendations
- [ ] Gaps and limitations noted
- [ ] Professional formatting
- [ ] Saved to appropriate location

### Self-Review Checklist
Before completing research, verify:
- [ ] Research question fully answered
- [ ] No single-source dependency
- [ ] Currency checked (prefer recent)
- [ ] Technical claims verified
- [ ] Conflicts addressed
- [ ] Organization clear and logical
- [ ] Recommendations specific and actionable
- [ ] All claims cited properly
- [ ] Output is professional
- [ ] User needs met

## Research Artifact Rules

### File Organization
**Primary location**: `docs/research/`

**Naming convention**: `[topic-name]-[type].md`
- Examples: `react-state-management-comparison.md`, `authentication-best-practices.md`

**Optional knowledge base**: `.galdr/knowledge/`
- For organization-wide knowledge
- Indexed and searchable
- Linked from tasks

### Document Structure
Every research document must include:
1. **Title**: Clear, descriptive
2. **Metadata**: Date, author, research type
3. **Executive Summary**: Key findings (2-3 paragraphs)
4. **Research Objective**: What question answered
5. **Methodology**: How research conducted
6. **Findings**: Organized by themes with citations
7. **Analysis**: Synthesis and insights
8. **Recommendations**: Actionable guidance
9. **Gaps and Limitations**: What's unknown
10. **References**: Complete source list

### Template Usage
Use appropriate template from `templates/`:
- `literature_review.md` - For comprehensive reviews
- `technical_deep_dive.md` - For technical investigations
- `competitive_analysis.md` - For comparing options
- `research_report.md` - For general research

## Integration Rules

### With Task Management
- Create research task if substantial (>1 hour)
- Update task status during research
- Document findings in task notes
- Link research artifacts from tasks
- Mark task complete when research done

### With Planning
- Research informs PRDs and feature plans
- Link research from planning documents
- Use findings to identify risks
- Base technical decisions on research
- Include research in project context

### With Implementation
- Research before implementing
- Reference research in code comments (if relevant)
- Use researched best practices
- Apply learned patterns
- Update research if implementation reveals gaps

## Common Mistakes to Avoid

### 1. Over-Reliance on First Result
**Problem**: Using first search result without checking others

**Solution**: Always consult multiple sources, compare approaches

### 2. Ignoring Publication Dates
**Problem**: Using outdated information, deprecated approaches

**Solution**: Check dates, prioritize recent content, note version-specific info

### 3. Treating All Sources Equally
**Problem**: Giving same weight to official docs and random blogs

**Solution**: Use source quality tiers, prioritize authoritative sources

### 4. Scope Creep
**Problem**: Research expands beyond original question

**Solution**: Regularly check against objective, stay focused, know when to stop

### 5. Lack of Synthesis
**Problem**: Just listing findings without organizing or analyzing

**Solution**: Group by themes, identify patterns, provide insights and recommendations

### 6. Missing Citations
**Problem**: Not documenting sources, can't verify claims later

**Solution**: Cite everything, capture URLs immediately, use consistent format

### 7. Analysis Paralysis
**Problem**: Over-researching, unable to make decision

**Solution**: Set time limits, define "good enough", focus on decision-making

### 8. No Actionable Output
**Problem**: Research doesn't inform decision or action

**Solution**: Always end with clear, specific recommendations

## Special Cases

### When Official Docs Are Missing
1. Look for GitHub repositories (README, docs, issues)
2. Check for community-maintained documentation
3. Search for conference talks or technical articles by maintainers
4. Review Stack Overflow discussions
5. Note in report that official docs are limited

### When Information Is Conflicting
1. Document the conflict clearly
2. Evaluate credibility of each source
3. Consider context (versions, use cases)
4. Look for additional authoritative sources
5. Explain nuance in your analysis
6. Provide balanced perspective

### When Research Is Inconclusive
1. Document what you found
2. Explain why it's inconclusive
3. Note information gaps
4. Provide best available guidance
5. Suggest how to fill gaps (experimentation, expert consultation)
6. Don't pretend certainty where none exists

### When Time Is Limited
1. Prioritize official docs only
2. Focus on most authoritative sources
3. Narrow scope to essential information
4. Provide "quick take" with caveats
5. Note that deeper research may be valuable
6. Offer to research more deeply if needed

## Success Indicators

Research is successful when:
- User's question is clearly answered
- Multiple credible sources consulted
- Information is organized and synthesized
- Recommendations are actionable
- Appropriate depth for decision importance
- Professional documentation created
- Sources are properly cited
- Gaps and limitations acknowledged
- Completed in reasonable time
- User can make informed decision

## Final Reminders

1. **Quality over quantity**: Better to read 5 sources thoroughly than 20 superficially
2. **Synthesis is key**: Organize, analyze, and provide insights - don't just list findings
3. **Always cite sources**: Every claim needs attribution
4. **Know when to stop**: Research has diminishing returns
5. **Be actionable**: End with clear recommendations
6. **Document everything**: Create artifacts for future reference
7. **Stay focused**: Keep research objective in mind
8. **Be skeptical**: Verify important claims
9. **Be honest**: Note uncertainties and gaps
10. **Be professional**: Create high-quality outputs
