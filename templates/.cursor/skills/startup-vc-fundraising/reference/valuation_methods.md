# Valuation Methods

Pre-money/post-money math, comparable analysis, revenue multiples, and SAFE/convertible note conversion.

## Pre-Money and Post-Money Basics

```
Post-money valuation = Pre-money valuation + Investment amount
Investor ownership   = Investment amount ÷ Post-money valuation
Founder ownership    = Pre-money valuation ÷ Post-money valuation
```

**Example**:
- Pre-money: $8M, Investment: $2M
- Post-money: $10M
- Investor ownership: $2M ÷ $10M = 20%
- Founder ownership: $8M ÷ $10M = 80%

## Valuation Ranges by Stage

| Stage | Pre-Money Range | Typical Revenue Multiple |
|-------|----------------|-------------------------|
| Pre-Seed | $1M - $5M | N/A (pre-revenue) |
| Seed | $4M - $15M | 20-100x ARR |
| Series A | $15M - $50M | 10-30x ARR |
| Series B | $50M - $150M | 8-20x ARR |
| Series C+ | $150M - $1B+ | 6-15x ARR |

*Ranges vary significantly by industry, market conditions, growth rate, and competitive dynamics.*

## Comparable Analysis

### Step 1: Identify Comparables
Find 5-10 companies that are similar in:
- Stage and round size
- Industry and business model
- Growth rate and metrics
- Geographic market
- Recency (last 12-18 months preferred)

### Step 2: Gather Data
For each comparable, collect:
- Round size and valuation
- ARR or revenue at time of raise
- Growth rate (MoM or YoY)
- Revenue multiple (valuation ÷ ARR)
- Investor and lead firm

### Step 3: Calculate Your Range
```
Your valuation range = Your ARR × Comparable revenue multiple range

Example:
  Your ARR: $1.2M
  Comparable multiples: 15x - 25x (median 20x)
  Valuation range: $18M - $30M (target: $24M)
```

### Step 4: Adjust for Differentiators
Adjust up or down based on:
- **Higher growth rate** than comps → higher multiple
- **Stronger retention** (NRR > 120%) → higher multiple
- **Larger TAM** → higher multiple
- **Weaker unit economics** → lower multiple
- **Competitive market** → lower multiple
- **Hot sector** (AI, climate, etc.) → higher multiple

### Data Sources for Comparables
| Source | Cost | Coverage |
|--------|------|---------|
| Crunchbase | $29-99/mo | Broad startup database |
| PitchBook | $7,000+/yr | Detailed deal data |
| CB Insights | $10,000+/yr | Market intelligence |
| AngelList | Free | Early-stage deals |
| Public filings (SEC) | Free | Late-stage and IPO data |

## Revenue Multiple Method

### SaaS Multiples (2024-2026 Market)
| Growth Rate | Typical Multiple |
|-------------|-----------------|
| < 50% YoY | 5-10x ARR |
| 50-100% YoY | 10-20x ARR |
| 100-200% YoY | 20-40x ARR |
| > 200% YoY | 40-100x ARR |

### Adjustments to Base Multiple
| Factor | Impact |
|--------|--------|
| Net revenue retention > 130% | +20-50% to multiple |
| Gross margins > 80% | +10-20% |
| CAC payback < 12 months | +10-20% |
| Rule of 40 score > 60 | +20-30% |
| Founder with prior exit | +10-20% |
| Market downturn | -20-40% |
| Crowded market | -10-20% |

## Discounted Cash Flow (DCF)

Rarely used for early-stage startups but relevant for Series B+:

```
Enterprise Value = Σ (FCF_t / (1 + r)^t) + Terminal Value / (1 + r)^n

Where:
  FCF_t = Free cash flow in year t
  r     = Discount rate (typically 25-40% for startups)
  n     = Projection period (usually 5-7 years)
```

High discount rates reflect startup risk. DCF is more useful as a sanity check than a primary valuation method.

## SAFE Conversion Math

### Cap-Only SAFE
```
SAFE amount: $500k
Valuation cap: $8M

At Series A ($12M pre-money):
  SAFE converts at: min($8M cap, $12M round price) = $8M
  SAFE ownership: $500k ÷ ($8M + $500k) ≈ 5.9%
```

### Discount-Only SAFE
```
SAFE amount: $500k
Discount: 20%

At Series A ($12M pre-money):
  Effective valuation: $12M × 0.80 = $9.6M
  SAFE ownership: $500k ÷ ($9.6M + $500k) ≈ 5.0%
```

### Cap + Discount SAFE
```
SAFE amount: $500k
Cap: $8M, Discount: 20%

At Series A ($12M pre-money):
  Cap price: $8M
  Discount price: $12M × 0.80 = $9.6M
  Converts at: min($8M, $9.6M) = $8M (cap is better for investor)
  SAFE ownership: $500k ÷ ($8M + $500k) ≈ 5.9%
```

### Convertible Note Conversion
```
Note: $500k, 6% interest, 24-month term, $8M cap, 20% discount

After 18 months:
  Accrued interest: $500k × 6% × 1.5 = $45k
  Total converting: $545k

At Series A ($12M pre-money):
  Cap price: $8M
  Discount price: $12M × 0.80 = $9.6M
  Converts at: min($8M, $9.6M) = $8M
  Note ownership: $545k ÷ ($8M + $545k) ≈ 6.4%
```

## Valuation Negotiation Tips

1. **Anchor with data** — present 5-10 comparable deals
2. **Lead with growth** — high growth rate justifies higher multiples
3. **Show the path** — demonstrate how this valuation leads to a markup at the next round
4. **Don't fixate on valuation alone** — terms (liquidation preference, board control) matter more
5. **Consider the option pool** — a higher valuation with a larger pre-money pool may net less founder ownership
6. **Market timing matters** — bull markets support higher multiples; adjust expectations in downturns
7. **Get multiple offers** — competition between investors is the best valuation driver
