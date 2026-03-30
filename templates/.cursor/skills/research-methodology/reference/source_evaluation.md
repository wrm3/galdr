# Source Evaluation Guide

This guide provides detailed criteria for evaluating source quality and credibility in research.

## Source Quality Tiers

### Tier 1: Authoritative Sources (Highest Priority)

**Official Documentation**
- Language/framework official docs
- Platform documentation (AWS, Azure, etc.)
- API references
- Release notes and changelogs

**Characteristics**:
- Published by the technology creator
- Maintained and updated regularly
- Definitive reference for features
- Version-specific information

**When to Use**: Always start here for technical topics

**Limitations**: May lack context, real-world examples, or critical perspective

---

**Academic and Technical Standards**
- IEEE, ACM publications
- W3C specifications
- RFC documents
- Industry standards (ISO, NIST, etc.)

**Characteristics**:
- Peer-reviewed or standards-body approved
- Rigorous methodology
- Authoritative
- Often foundational

**When to Use**: For fundamental concepts, standards, best practices

**Limitations**: May be overly academic, slow to update, not always practical

---

**Project Repositories**
- GitHub/GitLab README files
- Official project documentation
- GitHub Discussions for authoritative responses
- Issue trackers for known problems

**Characteristics**:
- Maintained by project maintainers
- Up-to-date implementation details
- Real issues and solutions
- Community involvement visible

**When to Use**: Understanding open-source projects, finding known issues

**Limitations**: Quality varies, may be incomplete, version confusion

---

### Tier 2: Expert Content (High Priority)

**Established Technical Publications**
- CSS-Tricks, Smashing Magazine
- A List Apart
- Web.dev (Google)
- Mozilla Developer Network (MDN)

**Characteristics**:
- Written by recognized experts
- Editorial review
- High technical quality
- Current and maintained

**When to Use**: Best practices, tutorials, deep dives

**Limitations**: May have editorial bias, sponsor influence

---

**Technical Blogs from Companies**
- Engineering blogs (Netflix, Airbnb, Uber)
- Cloud provider blogs (AWS, Google Cloud)
- Framework creator blogs (Vercel, Vue team)

**Characteristics**:
- Real-world implementation stories
- At-scale experiences
- Well-researched
- Company-specific context

**When to Use**: Architecture decisions, scaling patterns, real-world examples

**Limitations**: Company-specific solutions, may not generalize

---

**Recognized Expert Blogs**
- Blog posts from known experts in field
- Conference speakers
- Book authors
- Project maintainers

**Characteristics**:
- Deep expertise
- Often cutting-edge
- Personal perspective
- Detailed analysis

**When to Use**: Advanced topics, emerging patterns, expert opinions

**Limitations**: Individual perspective, may be outdated, variable quality

---

**Books and Long-Form Publications**
- Technical books from established publishers
- eBooks from recognized authors
- Long-form tutorials and courses

**Characteristics**:
- Comprehensive coverage
- Structured learning
- Reviewed and edited
- Deep treatment

**When to Use**: Learning new technologies, comprehensive understanding

**Limitations**: Can become outdated quickly, publication lag

---

### Tier 3: Community Content (Medium Priority)

**Stack Overflow**
- Accepted answers
- High-vote answers
- Recent answers (last 2-3 years)

**Characteristics**:
- Practical solutions
- Community-validated
- Code examples
- Specific problems

**When to Use**: Troubleshooting, specific problems, code examples

**Limitations**: Variable quality, may be outdated, context-specific

---

**Technical Reddit (r/programming, r/webdev, etc.)**
- High-vote posts
- Discussions with expert participation
- Community recommendations

**Characteristics**:
- Community consensus
- Multiple perspectives
- Current discussions
- Honest opinions

**When to Use**: Community sentiment, tool comparisons, emerging trends

**Limitations**: Opinions may be uninformed, echo chambers, variable expertise

---

**GitHub Issues and Discussions**
- Maintainer responses
- Issue resolutions
- Feature discussions
- Bug reports

**Characteristics**:
- Real problems and solutions
- Maintainer input
- Version-specific
- Community workarounds

**When to Use**: Known issues, workarounds, feature status

**Limitations**: May be unclear, version-specific, unresolved

---

**Dev.to, Hashnode, Medium (Technical)**
- Articles from verified authors
- High-engagement posts
- Tutorial content

**Characteristics**:
- Accessible writing
- Practical examples
- Community engagement
- Variable quality

**When to Use**: Tutorials, getting started guides, practical examples

**Limitations**: Variable quality, may have errors, limited review

---

### Tier 4: General Content (Use with Caution)

**Personal Blogs (Unknown Authors)**
- Individual blog posts
- Personal experiences
- Unverified claims

**When to Use**: Only when no better sources available, verify elsewhere

**Red Flags**: No author info, unclear credentials, factual errors

---

**Forum Posts (General)**
- Technical forums
- Discussion boards
- Community sites

**When to Use**: Supplement other research, multiple confirmations needed

**Red Flags**: Single source, no verification, outdated

---

**AI-Generated Content**
- ChatGPT outputs
- AI-written articles
- Automated content

**When to Use**: Never as primary source, always verify

**Red Flags**: Confident but incorrect, no citations, generic

---

## Evaluation Criteria

### 1. Authority

**Questions to Ask**:
- Who is the author?
- What are their credentials?
- Are they recognized in the field?
- Is this official documentation?
- Is the organization reputable?

**Red Flags**:
- Anonymous author
- No credentials listed
- Unknown organization
- Content farm indicators

**How to Verify**:
- Check author's other work
- Look for recognizable affiliations
- Search for author's reputation
- Check domain authority

---

### 2. Currency

**Questions to Ask**:
- When was this published?
- When was it last updated?
- Is it still relevant?
- What version does it reference?

**Red Flags**:
- No date visible
- 3+ years old for technical content
- Deprecated approaches
- Outdated version references

**How to Verify**:
- Check publication date
- Check last modified date
- Verify against current versions
- Look for update history

**Special Considerations**:
- Fundamental concepts age better than implementation details
- Framework-specific content outdates quickly (6-12 months)
- Core programming concepts remain relevant longer
- Always check version compatibility

---

### 3. Accuracy

**Questions to Ask**:
- Are facts verifiable?
- Are claims supported by evidence?
- Do other sources agree?
- Are there citations?

**Red Flags**:
- Factual errors
- Unsubstantiated claims
- No sources cited
- Contradicts authoritative sources

**How to Verify**:
- Cross-check with other sources
- Verify technical claims
- Test code examples
- Check official docs

---

### 4. Purpose

**Questions to Ask**:
- Why was this created?
- Is it educational or promotional?
- Is there bias or agenda?
- Who benefits from this information?

**Red Flags**:
- Heavy promotion of product/service
- Affiliate links without disclosure
- One-sided presentation
- Marketing language

**Source Types by Purpose**:
- **Educational**: Tutorials, guides, documentation
- **Promotional**: Product marketing, case studies, ads
- **Advocacy**: Opinion pieces, recommendations
- **News**: Announcements, releases, updates

---

### 5. Coverage

**Questions to Ask**:
- How comprehensive is the treatment?
- Are limitations discussed?
- Are alternatives mentioned?
- Is context provided?

**Red Flags**:
- Superficial treatment
- No mention of trade-offs
- Ignores alternatives
- Missing context

**Depth Indicators**:
- Discusses pros AND cons
- Mentions when NOT to use
- Provides context and rationale
- Acknowledges limitations

---

### 6. Objectivity

**Questions to Ask**:
- Is the perspective balanced?
- Are multiple viewpoints presented?
- Is bias disclosed?
- Are limitations acknowledged?

**Red Flags**:
- Absolute statements ("always", "never")
- Ignoring trade-offs
- Dismissing alternatives
- No acknowledgment of limitations

**Bias Types**:
- **Commercial**: Promoting products/services
- **Ideological**: Promoting particular approaches
- **Confirmation**: Seeking to confirm existing beliefs
- **Recency**: Assuming newest is always best

---

## Source Evaluation Checklist

For each source, evaluate:

### Quick Assessment (30 seconds)
- [ ] Author/organization identified?
- [ ] Publication date visible and recent?
- [ ] Professional appearance?
- [ ] No obvious red flags?

### Standard Assessment (2 minutes)
- [ ] Author credentials verified?
- [ ] Content is current (< 2-3 years)?
- [ ] Claims are specific and verifiable?
- [ ] Purpose is clear?
- [ ] Bias is minimal or disclosed?

### Deep Assessment (5 minutes)
- [ ] Author is recognized expert?
- [ ] Multiple sources confirm key claims?
- [ ] Trade-offs and limitations discussed?
- [ ] Citations provided for important claims?
- [ ] Context and rationale explained?
- [ ] Alternatives considered?

## Special Cases

### Evaluating Official Documentation
**Strengths**: Definitive, maintained, version-specific

**Weaknesses**: May lack context, examples, or critical perspective

**How to Use**: Primary source for facts, supplement with expert analysis

---

### Evaluating Stack Overflow
**Strengths**: Practical, code examples, community-validated

**Weaknesses**: Variable quality, context-specific, may be outdated

**Evaluation Criteria**:
- Check vote count (prefer 10+ votes)
- Check accepted answer status
- Check answer date (prefer < 2 years)
- Verify code actually works
- Read comments for caveats

---

### Evaluating Blog Posts
**Strengths**: Detailed, personal experience, accessible

**Weaknesses**: Individual perspective, variable quality, may be outdated

**Evaluation Criteria**:
- Who is the author? Check their background
- When was it written? Is it current?
- Are claims cited?
- Do examples work?
- Do other sources agree?

---

### Evaluating GitHub Issues
**Strengths**: Real problems, maintainer input, community solutions

**Weaknesses**: May be unresolved, version-specific, unclear

**Evaluation Criteria**:
- Is it resolved?
- Did a maintainer respond?
- What version?
- Does solution work for your version?
- Are there alternative solutions?

---

### Evaluating Comparisons
**Strengths**: Structured analysis, multiple options

**Weaknesses**: May be biased, outdated, incomplete

**Evaluation Criteria**:
- Who wrote it? Any commercial interest?
- When? Options change quickly
- Are all major options covered?
- Are criteria relevant?
- Is analysis fair and balanced?

---

## Handling Common Situations

### When Official Docs Are Poor
1. Supplement with expert blogs
2. Check GitHub README and discussions
3. Look for community-maintained docs
4. Search for conference talks by maintainers
5. Note documentation quality in research

### When Sources Conflict
1. Prioritize more authoritative source
2. Check publication dates
3. Consider context differences
4. Look for third source
5. Note conflict in research

### When Information Is Scarce
1. Expand to adjacent topics
2. Check related projects
3. Look for case studies
4. Consider experimentation
5. Note information gaps

### When Everything Seems Promotional
1. Look for independent reviews
2. Check negative experiences
3. Find comparisons from neutral parties
4. Examine with skepticism
5. Note promotional nature

## Confidence Levels

### High Confidence
Assign when:
- Multiple authoritative sources agree
- Information is current (< 1 year)
- Official documentation supports
- Expert consensus exists
- Verified through multiple tiers

### Medium Confidence
Assign when:
- Limited authoritative sources
- Some disagreement exists
- Information is somewhat dated (1-2 years)
- Relies on lower-tier sources
- Limited verification

### Low Confidence
Assign when:
- Only lower-tier sources available
- Sources conflict significantly
- Information is dated (2+ years)
- No authoritative sources found
- Unable to verify claims

### Always Note Confidence
In research reports, explicitly note confidence levels for key findings

## Source Documentation

### Minimum Citation Information
- Title/description
- Author or organization
- Publication date
- URL
- Access date (when you read it)

### Optional but Valuable
- Version references
- Specific section citations
- Screenshot or archive link
- Note about source quality

### Citation Format
```markdown
[Finding] [1]

## References
1. [Title] - [Author/Organization] ([Publication Date]) - [URL] - Accessed [Access Date]
```

**Example**:
```markdown
React 18 introduced automatic batching for state updates [1].

## References
1. "React 18 Release Notes" - React Team (March 2022) - https://react.dev/blog/2022/03/29/react-v18 - Accessed 2025-10-20
```

## Red Flags Summary

**Immediate Disqualifiers**:
- Factually incorrect information
- Promoting malicious practices
- No identifiable author or source
- Obviously AI-generated without verification

**Strong Warnings**:
- 3+ years old for implementation details
- Heavy commercial promotion without disclosure
- Anonymous or unknown author
- No citations for important claims
- Absolute statements without nuance

**Minor Concerns**:
- 1-2 years old (verify still current)
- Individual blog (supplement with other sources)
- Community content (verify from multiple sources)
- Promotional tone (seek independent verification)

## Best Practices

1. **Start with Tier 1 sources always**
2. **Use multiple sources for important claims**
3. **Check dates for technical content**
4. **Cross-verify with different source types**
5. **Note source quality in research**
6. **Lower confidence when sources are lower-tier**
7. **Document why sources were trusted**
8. **Be skeptical and verify**
9. **Acknowledge when sources are limited**
10. **Update research when better sources emerge**

## Quality Over Quantity

Better to deeply read and verify 5 high-quality sources than skim 20 low-quality sources.

**Preferred**:
- 3-5 Tier 1 sources, thoroughly reviewed
- 2-3 Tier 2 sources for perspective
- Tier 3 for specific examples only

**Not Preferred**:
- 15+ sources skimmed quickly
- Heavy reliance on Tier 3/4 sources
- No Tier 1 sources consulted
- Single-source dependency
