# Invention Disclosure Form

**Use this form to document your invention before filing a patent. This helps organize your thoughts and provides the foundation for your patent application.**

---

## Basic Information

**Date**: [Today's date]

**Inventor(s)**:
- Name: [Your name]
- Address: [Your address]
- Email: [Your email]
- Affiliation: [Company/University, if any]

**Invention Title**:
```
[Brief descriptive title - what does it do?]
```

---

## Section 1: The Problem

### What problem does your invention solve?

[Describe the problem in detail. Why does this problem matter?]

**Example**:
"Large language models using standard transformer architectures require significant computational resources due to O(n²) attention complexity. As sequence lengths increase, training becomes prohibitively expensive, limiting model size and accessibility."

### Why is this problem important?

- **Impact**: [Who is affected by this problem?]
- **Current Cost**: [What does this problem cost in time, money, resources?]
- **Frequency**: [How often does this problem occur?]

### What currently exists to solve this problem?

**Existing Solution 1**:
- What: [Brief description]
- Limitations: [What are its problems?]

**Existing Solution 2**:
- What: [Brief description]
- Limitations: [What are its problems?]

**Existing Solution 3** (if applicable):
- What: [Brief description]
- Limitations: [What are its problems?]

### Why are existing solutions inadequate?

[Explain why current approaches don't fully solve the problem]

---

## Section 2: Your Solution

### High-Level Description

In one paragraph, describe what your invention is and how it works:

```
[Your description here]
```

**Example**:
"My invention is a novel attention mechanism for transformer models that reduces computational complexity from O(n²) to O(n log n) through hierarchical clustering. The mechanism groups tokens by semantic similarity, computes attention within clusters at high resolution, and between clusters at lower resolution, achieving similar quality to standard attention while being 10x faster for long sequences."

### What makes it novel/unique?

List the key aspects that are NEW and different from anything that exists:

1. [Novel aspect 1]
2. [Novel aspect 2]
3. [Novel aspect 3]

**Example**:
1. Hierarchical clustering approach to token grouping (not used in prior attention mechanisms)
2. Adaptive cluster size based on sequence length and computational budget
3. End-to-end trainable without manual hyperparameter tuning

### Key Technical Details

**Main Components**:
1. [Component 1]: [What it does]
2. [Component 2]: [What it does]
3. [Component 3]: [What it does]

**How They Work Together**:
[Step-by-step description of the process]

**Example**:
```
1. Input tokens → Embedding layer → Dense representations
2. Clustering module → Groups tokens into sqrt(n) clusters
3. Intra-cluster attention → High-resolution attention within each cluster
4. Inter-cluster attention → Lower-resolution attention between cluster representatives
5. Combination layer → Merges intra and inter-cluster attention scores
6. Output → Attention-weighted token representations
```

---

## Section 3: Technical Implementation

### Algorithm/Process

Describe your algorithm or process step-by-step:

**Step 1**: [What happens first]
- Technical details:
- Why this step:

**Step 2**: [What happens next]
- Technical details:
- Why this step:

**Step 3**: [Continue...]

### Mathematical Formulation (if applicable)

```
[Include equations, formulas, or mathematical descriptions]

Example:
Input: X ∈ R^(n×d) (n tokens, d dimensions)

Step 1: Compute clusters
C = HierarchicalCluster(X, k=√n)

Step 2: Intra-cluster attention
A_intra = Softmax(Q_i K_i^T / √d) V_i  for each cluster i

Step 3: Inter-cluster attention
C_rep = {centroid(C_i) for i in clusters}
A_inter = Softmax(Q K_rep^T / √d) V_rep

Step 4: Combine
A_final = α·A_intra + (1-α)·A_inter
```

### Pseudocode

```python
# Provide pseudocode showing how it works
def your_invention(inputs):
    # Step 1
    result1 = process_step_1(inputs)

    # Step 2
    result2 = process_step_2(result1)

    # Step 3
    output = process_step_3(result2)

    return output

# Example for attention mechanism:
def hierarchical_attention(Q, K, V, n_clusters):
    # Cluster tokens
    clusters = hierarchical_cluster(K, k=sqrt(len(K)))

    # Intra-cluster attention
    intra_scores = []
    for cluster in clusters:
        scores = scaled_dot_product_attention(
            Q, cluster.keys, cluster.values
        )
        intra_scores.append(scores)

    # Inter-cluster attention
    cluster_reps = [cluster.centroid() for cluster in clusters]
    inter_scores = scaled_dot_product_attention(
        Q, cluster_reps, cluster_reps
    )

    # Combine
    final_attention = combine(intra_scores, inter_scores)
    return final_attention
```

---

## Section 4: Advantages and Benefits

### Quantifiable Improvements

Compared to existing solutions, your invention provides:

**Performance Metrics**:
- Metric 1: [Old value] → [New value] ([% improvement])
- Metric 2: [Old value] → [New value] ([% improvement])
- Metric 3: [Old value] → [New value] ([% improvement])

**Example**:
- Training Speed: 10 hours → 5 hours (50% faster)
- Memory Usage: 16GB → 10GB (37.5% reduction)
- Accuracy: 85% → 87% (+2 percentage points)
- Scalability: Max 10K tokens → Max 100K tokens (10x)

### Qualitative Benefits

**Benefit 1**: [Description]
- Why it matters: [Impact]

**Benefit 2**: [Description]
- Why it matters: [Impact]

**Benefit 3**: [Description]
- Why it matters: [Impact]

**Example**:
- **Easier to Use**: No manual hyperparameter tuning required, making it accessible to non-experts
- **More Robust**: Works across different sequence lengths without architecture changes
- **Environmentally Friendly**: 50% less compute = 50% less energy consumption

---

## Section 5: Applications and Use Cases

### Primary Application

**Application**: [Main use case]
**Market**: [Who would use this?]
**Value**: [What value does it provide?]

**Example**:
- **Application**: Training large language models
- **Market**: AI research labs, tech companies, startups
- **Value**: Enables training of larger models on existing hardware, reducing costs by 40-60%

### Additional Applications

**Application 2**: [Use case]
- Market: [Users]
- Value: [Benefits]

**Application 3**: [Use case]
- Market: [Users]
- Value: [Benefits]

**Example**:
- **Real-time chatbots**: Low-latency inference enables real-time responses with long conversation histories
- **Document analysis**: Process long documents (100+ pages) efficiently
- **Code understanding**: Analyze entire codebases in one forward pass

---

## Section 6: Development History

### When was it conceived?

**Date**: [When did you first have this idea?]
**Circumstances**: [What led to this invention?]

### How was it developed?

**Timeline**:
- [Date]: [Milestone 1 - e.g., Initial idea]
- [Date]: [Milestone 2 - e.g., First prototype]
- [Date]: [Milestone 3 - e.g., Successful testing]
- [Date]: [Milestone 4 - e.g., Today - ready to file]

### Who contributed?

**Primary Inventor(s)**:
- [Name]: [Their contribution]

**Contributors** (if any):
- [Name]: [Their contribution]

**Note**: Only list people who contributed to the INVENTIVE concept, not just implementation help.

---

## Section 7: Prior Art Search

### Have you searched for similar inventions?

**Search Sources**:
- [ ] Google Patents: [Searched terms]
- [ ] USPTO Database: [Searched terms]
- [ ] Academic Papers: [Searched sources]
- [ ] GitHub/Open Source: [Searched repositories]

### What did you find?

**Closest Prior Art 1**:
- Reference: [Patent number or paper citation]
- What it does: [Brief description]
- Key difference from your invention: [How yours is different]

**Closest Prior Art 2**:
- Reference: [Patent number or paper citation]
- What it does: [Brief description]
- Key difference from your invention: [How yours is different]

**Closest Prior Art 3**:
- Reference: [Patent number or paper citation]
- What it does: [Brief description]
- Key difference from your invention: [How yours is different]

### How is your invention different/better?

[Summarize what makes your invention novel compared to everything you found]

---

## Section 8: Experimental Results

### Have you tested your invention?

**Test 1**: [Description]
- Setup: [How you tested]
- Results: [What happened]
- Conclusion: [What it shows]

**Test 2**: [Description]
- Setup: [How you tested]
- Results: [What happened]
- Conclusion: [What it shows]

### Performance Data

| Test Case | Baseline | Your Method | Improvement |
|-----------|----------|-------------|-------------|
| [Test 1] | [Value] | [Value] | [%] |
| [Test 2] | [Value] | [Value] | [%] |
| [Test 3] | [Value] | [Value] | [%] |

**Example**:
| Test Case | Standard Attention | Hierarchical Attention | Improvement |
|-----------|-------------------|----------------------|-------------|
| 1K tokens | 0.1s | 0.05s | 50% faster |
| 10K tokens | 10s | 1.3s | 7.7x faster |
| 50K tokens | 250s | 12s | 20.8x faster |

---

## Section 9: Drawings and Diagrams

### Architecture Diagram

[Sketch or describe your system architecture]

```
[ASCII diagram or note "See attached image"]

Example:
┌─────────────┐
│   Inputs    │
└──────┬──────┘
       │
       ↓
┌──────────────┐
│  Component 1 │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  Component 2 │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│   Outputs    │
└──────────────┘
```

### Flowchart

[Sketch or describe the process flow]

### Other Figures

[Any other diagrams that help explain your invention]

---

## Section 10: Commercialization

### Is there a market for this?

**Market Size**: [Estimate]
**Target Customers**: [Who would buy/use this?]
**Competitive Advantage**: [Why would they choose your solution?]

### Are you planning to commercialize?

- [ ] Yes, I plan to start a company
- [ ] Yes, I plan to license it
- [ ] Maybe, exploring options
- [ ] No, academic interest only

### Have you disclosed this invention publicly?

**IMPORTANT**: Public disclosure can affect patent rights!

- [ ] No public disclosure yet (GOOD - file patent first!)
- [ ] Published paper: [Date, venue]
- [ ] Gave presentation: [Date, venue]
- [ ] Demo'd to outside parties: [Date, who]
- [ ] Posted on GitHub/social media: [Date, platform]

**If disclosed**: You have 1 year in US to file patent, but NO grace period internationally.

---

## Section 11: Ready to File?

### Checklist

Review your responses above. You're ready to file a provisional patent if:

- [ ] Problem is clearly defined
- [ ] Solution is technically detailed
- [ ] Novel aspects are identified
- [ ] Advantages are quantified
- [ ] At least one application is identified
- [ ] Prior art has been searched
- [ ] Testing/results documented (if available)
- [ ] Diagrams prepared (even hand-drawn is OK)
- [ ] No public disclosure yet (or within 1 year)

### Next Steps

1. **Use this disclosure to write provisional patent**
   - Template: [provisional_patent_template.md](provisional_patent_template.md)
   - Cost: $130 (micro entity)
   - Time: 2-4 hours

2. **File with USPTO**
   - URL: https://www.uspto.gov/patents/apply/patent-center
   - Establishes priority date
   - Gives 12 months to file utility patent

3. **Invoke patent-specialist SubAgent for guidance**
   - Ask: "Help me file a patent for [your invention]"
   - Get step-by-step personalized guidance

---

## Appendix: Additional Information

### Supporting Documents

List any additional documents that support your invention:
- [ ] Research papers (yours or related)
- [ ] Technical specifications
- [ ] Code repositories
- [ ] Test results
- [ ] User feedback
- [ ] Market research

### Confidentiality

Who has been told about this invention?

**Internal** (within your organization):
- [Name]: [Role] - [Date disclosed]

**External** (outside your organization):
- [Name]: [Organization] - [Date disclosed] - [Under NDA? Yes/No]

**Note**: Keep invention confidential until patent is filed!

---

**Form Completed By**: [Your name]
**Date**: [Today's date]
**Status**: Ready to file patent

**Next Action**: Use this disclosure to complete [provisional_patent_template.md](provisional_patent_template.md)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-28
**Template for**: AI/ML Inventions
