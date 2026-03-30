# AI/ML Patent Strategies

**Comprehensive guide to patenting AI/ML inventions with focus on what's patentable, claim strategies, and examples from successful patents.**

---

## Table of Contents

1. [What's Patentable in AI/ML](#whats-patentable-in-aiml)
2. [What's NOT Patentable](#whats-not-patentable)
3. [AI Patent Claim Strategies](#ai-patent-claim-strategies)
4. [Patent Categories for AI](#patent-categories-for-ai)
5. [Successful AI Patent Examples](#successful-ai-patent-examples)
6. [Common Pitfalls](#common-pitfalls)
7. [Best Practices](#best-practices)

---

## What's Patentable in AI/ML

### ✅ Novel Architectures

**Patentable**: New neural network structures, layer designs, connection patterns

**Examples**:
- Transformer architecture (attention mechanism)
- Residual connections (ResNet)
- Attention mechanisms (self-attention, cross-attention)
- Novel activation functions with technical advantages
- Layer normalization variants
- New pooling strategies

**Why Patentable**: Specific technical implementation that improves performance

### ✅ Training Methods

**Patentable**: Novel ways to train models

**Examples**:
- New loss functions
- Novel optimization algorithms
- Training schedules/curricula
- Data augmentation techniques
- Regularization methods
- Distillation approaches
- RLHF (Reinforcement Learning from Human Feedback)

**Why Patentable**: Specific process with technical steps

### ✅ Inference Optimization

**Patentable**: Methods to make predictions faster/cheaper

**Examples**:
- Model compression techniques
- Quantization methods
- Pruning strategies
- Knowledge distillation
- Early exit mechanisms
- Caching strategies

**Why Patentable**: Technical solution to computational problem

### ✅ Data Processing

**Patentable**: Novel ways to prepare/process data

**Examples**:
- Tokenization methods
- Feature extraction techniques
- Data cleaning pipelines
- Synthetic data generation
- Data augmentation algorithms

**Why Patentable**: Specific technical method

### ✅ Domain-Specific Applications

**Patentable**: Applying AI to solve specific technical problems

**Examples**:
- Medical image analysis with novel preprocessing
- Code generation with syntax-aware mechanisms
- Drug discovery with molecular representation
- Autonomous driving with sensor fusion

**Why Patentable**: Technical solution to domain problem

### ✅ Hardware Implementations

**Patentable**: Hardware designs for AI/ML

**Examples**:
- Custom AI accelerators (TPU, NPU)
- FPGA implementations
- Neuromorphic hardware
- Specialized memory architectures

**Why Patentable**: Physical device with technical improvements

---

## What's NOT Patentable

### ❌ Abstract Ideas

**Not Patentable**: "Use AI to solve X" without technical details

**Example**:
- ❌ "Use machine learning to predict stock prices"
- ❌ "Apply neural networks to diagnose disease"
- ❌ "AI system for recommendation"

**Why Not**: Too abstract, no specific technical implementation

**How to Fix**: Add specific technical details about HOW you do it

### ❌ Mathematical Formulas Alone

**Not Patentable**: Pure math without application

**Example**:
- ❌ "Formula for calculating attention scores"
- ❌ "Equation for gradient descent"

**Why Not**: Laws of nature, mathematical truths

**How to Fix**: Patent the METHOD that uses the formula in a specific way

### ❌ Data Alone

**Not Patentable**: Datasets, even if valuable

**Example**:
- ❌ "Dataset of 1 million labeled images"
- ❌ "Curated training data for sentiment analysis"

**Why Not**: Data is not an invention

**How to Fix**: Patent the METHOD for creating/processing the data

### ❌ Trained Model Weights

**Not Patentable**: Model parameters themselves

**Example**:
- ❌ "Weights for BERT trained on Wikipedia"
- ❌ "Parameters for GPT-3 model"

**Why Not**: Data, not a process or system

**How to Fix**: Patent the ARCHITECTURE or TRAINING METHOD

### ❌ Business Methods Without Tech

**Not Patentable**: Business processes without technical innovation

**Example**:
- ❌ "Business model for AI consulting"
- ❌ "Pricing strategy for ML services"

**Why Not**: Business method exception

**How to Fix**: Add specific technical implementation

---

## AI Patent Claim Strategies

### Strategy 1: Multiple Independent Claims

**Approach**: Patent different aspects separately

**Example Claims for Attention Mechanism**:

```
Claim 1 (System): A neural network system comprising [architecture]...
Claim 2 (Training Method): A method for training comprising [steps]...
Claim 3 (Inference Method): A method for generating predictions comprising [steps]...
Claim 4 (Computer-Readable Medium): A non-transitory medium storing instructions...
```

**Benefit**: If one claim is rejected, others may still be granted

### Strategy 2: Broad-to-Narrow Progression

**Approach**: Start broad, add specifics in dependent claims

**Example**:

```
Claim 1 (Broad): A system for processing sequences with attention mechanism...
Claim 2 (Narrower): The system of claim 1, wherein the attention uses hierarchical clustering...
Claim 3 (Even Narrower): The system of claim 2, wherein k-means clustering is used...
Claim 4 (Most Specific): The system of claim 3, wherein k = sqrt(sequence_length)...
```

**Benefit**: Fallback protection if broad claim is rejected

### Strategy 3: Focus on Technical Implementation

**Approach**: Emphasize HOW it works, not WHAT it does

**Bad (Abstract)**:
```
Claim: A system that uses AI to improve accuracy...
```

**Good (Technical)**:
```
Claim: A neural network system comprising:
  a) an encoder with N transformer layers;
  b) each layer including a multi-head attention mechanism with H heads;
  c) wherein attention is computed using hierarchical clustering
     reducing complexity from O(n²) to O(n log n);
  d) a decoder configured to generate output sequences...
```

### Strategy 4: Quantify Improvements

**Approach**: Include measurable benefits in claims

**Example**:
```
Claim: A method for training, wherein the method:
  - reduces training time by at least 40% compared to standard methods
  - achieves accuracy within 2% of full-precision baseline
  - requires less than 50% of memory compared to uncompressed model
```

**Benefit**: Shows concrete technical improvement

### Strategy 5: Claim Multiple Embodiments

**Approach**: Cover variations in dependent claims

**Example**:
```
Claim 1: A system with hierarchical attention...
Claim 2: The system of claim 1, wherein clustering uses k-means
Claim 3: The system of claim 1, wherein clustering uses hierarchical agglomerative clustering
Claim 4: The system of claim 1, wherein clustering uses DBSCAN
Claim 5: The system of claim 1, wherein k is dynamically adjusted
Claim 6: The system of claim 1, wherein k is fixed at sqrt(n)
```

**Benefit**: Covers different implementations

---

## Patent Categories for AI

### Category 1: Architecture Patents

**What**: Novel neural network structures

**Example Structure**:
```
Independent Claim: System comprising specific architecture
Dependent Claims: Variations in layer types, connections, dimensions
```

**Real Example**: Google's Transformer patent
- Claims attention mechanism structure
- Multiple heads, scaled dot-product
- Positional encoding

### Category 2: Training Patents

**What**: Methods for training models

**Example Structure**:
```
Independent Claim: Method comprising training steps
Dependent Claims: Specific loss functions, optimizers, schedules
```

**Real Example**: OpenAI's RLHF patent
- Claims reinforcement learning from human feedback process
- Reward model training
- Policy optimization steps

### Category 3: Optimization Patents

**What**: Making models faster/smaller/cheaper

**Example Structure**:
```
Independent Claim: Method for compressing/optimizing model
Dependent Claims: Specific compression techniques, quantization levels
```

**Real Example**: Quantization patents
- Claims specific bit-width reductions
- Calibration methods
- Hardware implementations

### Category 4: Application Patents

**What**: Applying AI to specific domains

**Example Structure**:
```
Independent Claim: System for [domain task] using AI with [novel aspect]
Dependent Claims: Domain-specific preprocessing, post-processing
```

**Real Example**: AlphaFold protein folding
- Claims specific architecture for protein structure
- Novel geometric attention mechanism
- Structure-aware loss function

---

## Successful AI Patent Examples

### Example 1: Attention Mechanism (Google)

**Patent**: US 10,XXX,XXX - "Attention-based sequence transduction"

**Key Claims**:
- Self-attention mechanism structure
- Multi-head attention with parallel computations
- Scaled dot-product attention formula
- Positional encoding method

**What Made It Patentable**:
- Specific technical implementation
- Novel architecture different from RNNs
- Quantifiable improvements (parallelizable, faster)
- Detailed mathematical formulation

**Strategy**: Claimed both system and method aspects

### Example 2: BERT Pre-training (Google)

**Patent**: US 10,XXX,XXX - "Bidirectional encoder representations"

**Key Claims**:
- Masked language modeling objective
- Next sentence prediction task
- Bidirectional training approach
- Fine-tuning method

**What Made It Patentable**:
- Novel training objective (MLM)
- Departure from unidirectional models
- Specific two-stage process (pre-train + fine-tune)
- Demonstrated improvements across benchmarks

**Strategy**: Focused on training method, not architecture alone

### Example 3: ResNet (Microsoft)

**Patent**: US 9,XXX,XXX - "Deep residual learning"

**Key Claims**:
- Residual connection structure (skip connections)
- Identity mapping bypassing layers
- Gradient flow improvement
- Very deep networks (100+ layers)

**What Made It Patentable**:
- Solved vanishing gradient problem
- Enabled training of much deeper networks
- Specific architectural element (residual block)
- Clear technical advantage

**Strategy**: Claimed architectural element + benefits

### Example 4: Dropout (Hinton et al.)

**Patent**: US 9,XXX,XXX - "Dropout training for neural networks"

**Key Claims**:
- Randomly dropping units during training
- Probability parameter for dropout
- Ensemble effect interpretation
- Reduced overfitting

**What Made It Patentable**:
- Novel regularization technique
- Specific random dropping process
- Demonstrated improvement in generalization
- Applicable across architectures

**Strategy**: Claimed training method with specific steps

---

## Common Pitfalls

### Pitfall 1: Too Abstract

**Problem**: Claims are too high-level

**Bad Example**:
```
Claim: A system that uses AI to improve performance
```

**Why Bad**: No specific technical details

**Fix**: Add architecture, process steps, specific methods

**Good Example**:
```
Claim: A neural network system comprising:
  a) an encoder with transformer layers
  b) each layer having multi-head attention (H=8)
  c) hierarchical clustering reducing O(n²) to O(n log n)
```

### Pitfall 2: Claiming Standard Techniques

**Problem**: Trying to patent well-known methods

**Bad Example**:
```
Claim: Using backpropagation to train neural networks
```

**Why Bad**: Already known, not novel

**Fix**: Claim your NOVEL variation or application

**Good Example**:
```
Claim: A training method using backpropagation with:
  - adaptive learning rate based on loss landscape curvature
  - gradient clipping with dynamic thresholds
  - novel warm-up schedule
```

### Pitfall 3: Ignoring Prior Art

**Problem**: Not searching for similar inventions

**Consequence**: Patent rejected during examination

**Fix**:
- Search USPTO and Google Patents
- Read recent papers in your area
- Check GitHub for open-source implementations
- Distinguish your invention from prior art

### Pitfall 4: Publishing Before Filing

**Problem**: Publicly disclosing invention

**Consequence**:
- US: 1-year grace period (can still file)
- International: NO grace period (lose rights!)

**Fix**:
- File provisional patent BEFORE publishing
- File BEFORE conference presentations
- File BEFORE public demos/launches

### Pitfall 5: Insufficient Technical Detail

**Problem**: Provisional patent lacks detail

**Consequence**: Utility patent can't claim new matter

**Fix**:
- Include extensive technical description
- Add multiple embodiments/variations
- Provide pseudocode and equations
- Include experimental results

---

## Best Practices

### ✅ Do: File Provisional First

**Strategy**: Quick, cheap provisional → Refine for utility

**Timeline**:
- Day 1: File provisional ($130)
- Months 1-12: Refine, test, gather evidence
- Month 11: File utility patent ($10K-$30K)

**Benefit**: Establishes priority date immediately

### ✅ Do: Claim Multiple Aspects

**Strategy**: System + Method + Medium claims

**Example**:
- Claim 1: System architecture
- Claim 2: Training method
- Claim 3: Inference method
- Claim 4: Computer-readable medium

**Benefit**: Multiple protection angles

### ✅ Do: Include Experimental Results

**What to Include**:
- Benchmark comparisons
- Ablation studies
- Performance metrics
- Scalability tests

**Benefit**: Demonstrates concrete improvements

### ✅ Do: Use Dependent Claims

**Strategy**: Broad independent + narrow dependents

**Benefit**: Fallback protection if broad claim rejected

### ✅ Do: Focus on Technical Implementation

**Strategy**: Emphasize HOW not WHAT

**Example**:
- ❌ "System for better accuracy"
- ✅ "System comprising [specific architecture] configured to [specific operations]"

### ✅ Do: Consider International Filing

**When**: If global market potential

**Strategy**:
- Month 12: File PCT application
- Month 30: Enter national phase in key countries

**Countries to Consider**:
- US (largest tech market)
- Europe (EPO covers many countries)
- China (manufacturing, large market)
- Japan (tech market)

### ✅ Do: Work with Patent Attorney

**When**: For utility patent ($10K-$30K)

**What They Provide**:
- Professional claim drafting
- Prior art search
- USPTO prosecution
- Strategic advice

**DIY OK For**: Provisional patent ($130)

---

## Quick Reference: Is My AI Invention Patentable?

### ✅ Likely Patentable

- [ ] Novel neural network architecture
- [ ] New training algorithm/method
- [ ] Optimization technique with technical improvements
- [ ] Data processing method (specific steps)
- [ ] Hardware implementation for AI
- [ ] Domain-specific AI application with novel technical aspects
- [ ] Has quantifiable improvements over prior art
- [ ] Not publicly disclosed (or <1 year ago in US)

### ❌ Likely NOT Patentable

- [ ] Using standard methods (BERT, GPT) without modification
- [ ] Dataset alone
- [ ] Trained model weights
- [ ] Abstract idea ("use AI for X")
- [ ] Mathematical formula alone
- [ ] Business method without technical innovation
- [ ] Already published (>1 year ago or international)

### 🤔 Maybe Patentable (Need Expert Review)

- [ ] Minor modifications to existing architectures
- [ ] Combination of known techniques in novel way
- [ ] Application of existing method to new domain
- [ ] Implementation details of known concepts

**Recommendation**: Consult patent attorney or use patent-specialist SubAgent

---

## Resources

### Patent Search
- **USPTO**: https://patft.uspto.gov/
- **Google Patents**: https://patents.google.com/

### AI Patent Examples
- Search: "neural network" + "attention" + "transformer"
- Filter by assignee: Google, Facebook, Microsoft, OpenAI

### Academic Papers
- **arXiv.org**: AI/ML preprints
- **Papers With Code**: Implementation + papers
- **Google Scholar**: Citation search

---

**Version**: 1.0.0
**Last Updated**: 2025-10-28
**Applies To**: AI/ML Patents
**Status**: Production Ready
