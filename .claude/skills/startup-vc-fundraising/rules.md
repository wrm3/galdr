# VC Fundraising Skill - Rules

Integration rules for the startup-vc-fundraising skill with Cursor IDE.

## Auto-Activation Rules

This skill should be automatically activated when:

### Keywords Detected
- "fundraising", "raise capital", "raising money"
- "VC", "venture capital", "investors", "angel investors"
- "pitch deck", "investor deck", "pitch"
- "term sheet", "investment terms", "valuation"
- "cap table", "dilution", "equity", "ownership"
- "Series A", "Series B", "seed round", "pre-seed"
- "due diligence", "DD", "investor meeting"
- "investor outreach", "VC research", "finding investors"

### File Patterns Detected
- `*pitch*deck*.{ppt,pptx,pdf}`
- `*investor*.{ppt,pptx,pdf,xlsx}`
- `term_sheet*.{pdf,docx}`
- `cap_table*.{xlsx,csv}`
- `financial*model*.{xlsx}`
- `investor*tracking*.{xlsx,csv}`
- `data*room*/`

### Context Patterns
- User mentions they are a founder or CEO
- Discussion of company metrics (ARR, MRR, growth rate)
- Mention of valuation or investment amounts
- Discussion of VC firms or investor names
- Questions about fundraising process or timeline

## When to Use

### Primary Use Cases
1. **Pitch Deck Review**: Analyzing and improving investor pitch decks
2. **VC Research**: Finding and targeting appropriate investors
3. **Term Sheet Analysis**: Understanding and negotiating investment terms
4. **Cap Table Management**: Modeling dilution and equity allocation
5. **Process Planning**: Creating fundraising timeline and strategy
6. **Meeting Preparation**: Preparing for investor meetings and pitches
7. **Due Diligence**: Organizing materials and responding to DD requests

### Secondary Use Cases
- Financial modeling for investors
- Valuation analysis and benchmarking
- Competitive fundraising landscape analysis
- Investor relationship management
- Post-fundraising board management guidance

## Activation Priority

**Priority Level**: HIGH (when fundraising-related)

**Activation Order**:
1. Detect fundraising context
2. Load startup-vc-fundraising skill
3. Activate fundraising-specialist agent if complex analysis needed
4. Apply vc_fundraising.md rules
5. Reference stage-specific guidance (pre-seed, seed, Series A, etc.)

## Integration Points

### Works Best With
- **business-planning**: Use business plan for fundraising narrative
- **financial-modeling**: Build investor-ready financial projections
- **patent-filing-ai**: Strengthen IP story for investors
- **market-research**: Validate market size and opportunity

### Provides Data To
- **business-planner agent**: Funding strategy and milestones
- **financial-analyst**: Unit economics and projections
- **solution-architect**: Investor-ready technical architecture

### Receives Data From
- **business-planning**: Market size, competitive analysis, strategy
- **financial-modeling**: Historical financials, projections, unit economics
- **qa-bug-tracking**: Product quality and stability metrics
- **task-management**: Development roadmap and milestones

## Agent Invocation

### Manual Invocation
```
@fundraising-specialist [request]
```

### Automatic Invocation
Agent automatically activates when:
- Pitch deck file is referenced
- Term sheet analysis requested
- VC research query detected
- Dilution or cap table calculation needed
- Fundraising process planning requested

### Invocation Examples
```
@fundraising-specialist Review my seed pitch deck and provide feedback
@fundraising-specialist Find VCs that invest in AI/ML at seed stage
@fundraising-specialist Analyze this term sheet and highlight concerns
@fundraising-specialist Calculate dilution from $2M at $8M pre-money
@fundraising-specialist Create a fundraising timeline for Q1 2026 close
```

## Context Requirements

### Minimum Context Needed
- **Fundraising stage**: Pre-seed, seed, Series A, B, C+
- **Company profile**: Industry, business model, current traction
- **Ask**: Amount raising, current valuation (if applicable)

### Optimal Context
- Current metrics (ARR, customers, growth rate)
- Previous fundraising history
- Team composition and background
- Product status and roadmap
- Target use of funds
- Geographic location

### Context Gathering
If insufficient context, agent should ask:
1. "What stage are you at?" (pre-seed, seed, Series A, etc.)
2. "What are your current metrics?" (revenue, customers, growth)
3. "How much are you looking to raise?"
4. "What's your industry/business model?"
5. "Where are you located?" (for VC geography targeting)

## Stage-Specific Rules

### Pre-Seed ($50k-$500k)
- Focus on problem validation and team
- Expect limited traction metrics
- Emphasize founder background and domain expertise
- Target angels, pre-seed funds, incubators
- Accept that projections are speculative

### Seed ($500k-$3M)
- Require product-market fit signals
- Expect $10k-$100k MRR or equivalent traction
- Focus on growth rate (15-30% MoM)
- Target seed VCs and angel groups
- Use realistic 3-year projections

### Series A ($3M-$15M)
- Require $1M+ ARR and strong growth (100%+ YoY)
- Expect proven unit economics (LTV/CAC > 3x)
- Focus on scalable go-to-market
- Target institutional VCs (Series A focused)
- Show path to $10M+ ARR

### Series B+ ($15M+)
- Require $10M+ ARR and efficient growth
- Expect category leadership positioning
- Focus on market expansion opportunities
- Target growth-stage VCs and crossover funds
- Show path to profitability and IPO

## Output Standards

### Pitch Deck Reviews
**Format**:
1. Overall score (X/10) and summary
2. Strengths (3-5 bullets)
3. Areas for improvement (prioritized)
4. Slide-by-slide feedback
5. Next steps and timeline

**Quality Criteria**:
- Content: Clear problem, solution, traction
- Story: Compelling narrative arc
- Design: Professional, readable, on-brand
- Data: Accurate metrics, credible projections
- Ask: Clear fundraising request

### VC Research Results
**Format**:
1. Search criteria summary
2. VCs found (count)
3. Tiered prioritization (Tier 1-4)
4. Detailed list with:
   - Firm name
   - Key partner
   - Investment focus
   - Recent investments
   - Warm intro path (if available)
5. Outreach recommendations

**Prioritization Criteria**:
- Tier 1: Perfect fit (thesis, stage, check size, geography)
- Tier 2: Good fit (most criteria match)
- Tier 3: Possible fit (some criteria match)
- Tier 4: Stretch (backup options)

### Term Sheet Analysis
**Format**:
1. Overall assessment (score, founder-friendliness)
2. Key terms summary
3. Red flags and concerns (prioritized)
4. Comparison to market standards
5. Negotiation recommendations (critical, important, nice-to-have)
6. Dilution modeling and exit scenarios
7. Talking points for negotiation

**Analysis Depth**:
- Valuation structure
- Liquidation preferences
- Anti-dilution protection
- Board composition
- Voting rights and protective provisions
- Pro-rata rights
- Other material terms

## Quality Assurance

### Validation Rules
- **Metrics**: Verify metrics are realistic for stage
- **Projections**: Check growth rates against benchmarks
- **Valuation**: Compare to industry comps
- **Terms**: Flag non-standard or founder-unfriendly terms
- **Timeline**: Ensure fundraising timeline is achievable

### Red Flags to Highlight
**Pitch Deck**:
- Unrealistic projections (10x+ growth with no basis)
- Missing traction or metrics
- Weak or incomplete team
- Unclear competitive differentiation
- Vague use of funds

**Term Sheet**:
- Participating preferred stock
- Multiple liquidation preference (2x+)
- Full ratchet anti-dilution
- Excessive board control for investors
- Unreasonable no-shop period (> 60 days)
- Unusual closing conditions

### Benchmarking
Always compare against:
- Industry-standard metrics for stage
- Typical valuation multiples
- Market-standard term sheet terms
- Fundraising timeline expectations
- Dilution ranges by stage

## Best Practices Enforcement

### Fundraising Process
- ✅ Start with 6-9 months runway
- ✅ Build VC list of 100+ firms
- ✅ Pursue warm intros (highest success rate)
- ✅ Batch meetings (2-3 week sprints)
- ✅ Follow up within 24 hours
- ✅ Keep multiple processes parallel (not sequential)
- ✅ Target 3-6 month timeline (don't let drag)

### Pitch Deck
- ✅ 15 slides maximum (main deck)
- ✅ Problem-first, not solution-first
- ✅ Quantify everything (metrics, market, impact)
- ✅ Show traction (not just potential)
- ✅ Current data (< 1 month old)
- ✅ Professional design (clean, readable)
- ✅ Backup slides (appendix) for detailed Q&A

### Term Negotiation
- ✅ Consult startup lawyer always
- ✅ Get multiple term sheets (leverage)
- ✅ Prioritize: partnership > terms > valuation
- ✅ Push for 1x non-participating liquidation preference
- ✅ Ensure broad-based weighted average anti-dilution
- ✅ Limit protective provisions to major events
- ✅ 30-day no-shop period (45 max)

### Due Diligence
- ✅ Organize data room in advance
- ✅ Respond to requests within 24-48 hours
- ✅ Be transparent about challenges
- ✅ Prepare 3-5 customer references
- ✅ Weekly status updates to VC
- ✅ Maintain momentum and urgency

## Error Handling

### Common User Errors

**Insufficient Context**:
- User: "Review my pitch deck"
- Response: Ask for deck file, stage, and current metrics

**Stage Mismatch**:
- User has $0 revenue but wants Series A guidance
- Response: Redirect to appropriate stage (pre-seed or seed)

**Unrealistic Expectations**:
- User expects to raise $10M seed with no traction
- Response: Calibrate expectations with stage-appropriate metrics

**Missing Key Information**:
- User asks for VC list but doesn't specify stage, industry, or geography
- Response: Gather requirements before researching

### Fallback Strategies

**If skill resources unavailable**:
- Provide general best practices from rules.md
- Reference external resources (Y Combinator, First Round)
- Suggest consulting with experienced founders or advisors

**If agent (Opus) unavailable**:
- Provide structured guidance from SKILL.md
- Use reference guides for stage-specific advice
- Recommend manual analysis with provided frameworks

**If user needs exceed skill scope**:
- Recommend consulting professional advisors (lawyers, bankers)
- Suggest founder communities (YC, On Deck, SaaStr)
- Reference additional learning resources

## Maintenance and Updates

### Update Frequency
- **VC Database**: Quarterly (market changes frequently)
- **Metrics Benchmarks**: Semi-annually (industry standards evolve)
- **Term Sheet Standards**: Annually (market practices change slowly)
- **Templates**: As needed (based on user feedback)

### Version Control
- Track skill version in SKILL.md
- Document changes in changelog
- Maintain backward compatibility
- Archive old reference materials

### Quality Metrics
- User satisfaction with guidance
- Fundraising success rate (if trackable)
- Pitch deck quality improvements
- Term sheet negotiation outcomes
- Agent response accuracy

## Privacy and Confidentiality

### Sensitive Information Handling
- **Pitch decks**: Treat as confidential, don't share externally
- **Financials**: Handle with care, don't expose in logs
- **Term sheets**: Highly confidential, analyze privately
- **Cap tables**: Sensitive ownership data, protect carefully
- **VC conversations**: Private communications, don't disclose

### Data Security
- Don't store sensitive financial data
- Don't log cap table details
- Don't share pitch deck content externally
- Remind users to password-protect documents
- Recommend secure data rooms (DocSend, Dropbox)

### Legal Disclaimers
- This skill provides guidance, not legal advice
- Always consult with qualified startup lawyer for legal matters
- Term sheet analysis is educational, not legal counsel
- Valuations are estimates, not professional valuations
- VC research is informational, not investment recommendations

## Success Metrics

### Skill Effectiveness
- Pitch deck quality score improvement (target: +2 points on 10-point scale)
- VC meeting conversion rate (target: 20-25% for warm intros)
- Term sheet terms quality (target: founder-friendly terms achieved)
- Fundraising timeline (target: 3-6 months from start to close)
- User satisfaction (target: 8+/10 rating)

### Agent Performance
- Response accuracy (target: 95%+ correct guidance)
- Response completeness (target: all key areas covered)
- Actionability (target: specific, tactical recommendations)
- Speed (target: comprehensive analysis in < 2 minutes)

---

**Skill**: startup-vc-fundraising
**Version**: 1.0
**Last Updated**: 2025-11-02
**Maintained By**: AI Project Template Team
**Model Compatibility**: All models (Opus recommended for agent)
