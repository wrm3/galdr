# Cap Table Management

Equity types, dilution calculations, option pool strategy, SAFE/convertible note mechanics, and cap table tools.

## Equity Types

### Common Stock
- Issued to founders and employees
- 1 vote per share
- Last in liquidation preference order
- Subject to vesting (typically 4-year with 1-year cliff)

### Preferred Stock
- Issued to investors
- Liquidation preference (1x typical)
- Converts to common (1:1 typical)
- Protective provisions and voting rights
- Anti-dilution protection

### Stock Options
- Granted to employees from the option pool
- Strike price set by 409A valuation
- Standard: 4-year vesting, 1-year cliff
- 10-year exercise window (post-termination varies: 90 days to 10 years)
- Taxed as ordinary income on exercise (NSOs) or at sale (ISOs)

### RSUs (Restricted Stock Units)
- Common for later-stage companies (Series B+)
- No strike price or exercise cost
- 4-year vesting typical
- Taxed as ordinary income when vested

## Cap Table by Stage

### Pre-Seed
```
Founders:     90-95%
Advisors:     1-3% (0.25-1% each)
Option pool:  10%
```

### After Seed ($2M at $8M pre-money)
```
Founders:       72%  (90% × 80%)
Advisors:       0.8% (1% × 80%)
Employees:      7.2% (9% × 80%)
Seed investors: 20%
Option pool:    refreshed to 10%
```

### After Series A ($10M at $30M pre-money)
```
Founders:         54%  (72% × 75%)
Advisors:         0.6%
Employees:        9.4%
Seed investors:   15%  (20% × 75%)
Series A:         25%
Option pool:      6% remaining
```

## Dilution Math

### Basic Formula
```
New ownership % = Old ownership % × (1 - Investor % of post-money)
```

### With Option Pool Increase
```
New ownership % = Old % × (1 - (Investment% + Pool increase%) / (100% + Pool increase%))

Example:
  Current ownership: 80%
  Investment: 20% of post-money
  Option pool increase: 10% of post-money

  New = 80% × (1 - 30%/110%) = 80% × 72.7% = 58.2%
```

### Typical Dilution Per Round
| Stage | Dilution | Founder Ownership After |
|-------|----------|------------------------|
| Pre-Seed | 10-20% | 80-90% |
| Seed | 15-25% | 60-75% |
| Series A | 20-30% | 45-55% |
| Series B | 15-25% | 35-45% |
| Series C+ | 10-20% | 25-35% |
| At IPO/exit | cumulative | 15-30% (successful companies) |

## Option Pool Strategy

### Recommended Pool Size
| Stage | Pool Size (% of fully diluted) |
|-------|-------------------------------|
| Pre-Seed | 10-15% |
| Seed | 10-15% (refresh if depleted) |
| Series A | 10-15% (refresh) |
| Series B+ | 8-12% (refresh) |

### Pre-Money vs Post-Money Pool Creation
- **Pre-money pool** (investor-friendly): Pool carved from founders' share before investment
- **Post-money pool** (founder-friendly): Pool created after investment, dilutes everyone equally

Negotiate for post-money pool when possible. Justify smaller pre-money pools with a detailed hiring plan.

## SAFE Notes (Simple Agreement for Future Equity)

### Key Terms
- **Valuation cap**: Maximum valuation at which the SAFE converts
- **Discount**: Percentage discount to the next round's price (typically 15-25%)
- **MFN (Most Favored Nation)**: Investor gets best terms of any future SAFE
- **Pro-rata rights**: Right to participate in future rounds

### Conversion Example
```
SAFE: $500k with $8M cap and 20% discount
Series A: $12M pre-money valuation

Cap conversion price:  $8M ÷ shares = lower price per share
Discount price:        $12M × 0.80 = $9.6M effective valuation
Investor converts at:  min($8M cap, $9.6M discount) = $8M cap
```

### SAFE vs Convertible Note
| Feature | SAFE | Convertible Note |
|---------|------|-----------------|
| Interest | None | 2-8% annually |
| Maturity date | None | 12-24 months |
| Repayment obligation | No | Yes (at maturity) |
| Complexity | Simple | More complex |
| Best for | Pre-seed/seed | Seed (when debt preferred) |

## Cap Table Tools

### Early Stage (Free/Low Cost)
- **Google Sheets**: Simple tracking, full control
- **Carta**: Free for basic cap tables
- **Pulley**: Free for early stage
- **Capshare**: Free basic plan

### Growth Stage (Paid)
- **Carta**: $1,200-$6,000/year (industry standard)
- **Pulley**: $500-$2,000/year
- **AngelList**: For syndicates
- **Shareworks**: Enterprise pricing

### Key Features to Look For
- Cap table modeling and scenario planning
- 409A valuation support
- Equity management for employees
- Investor reporting
- Round modeling and dilution analysis
- Electronic signatures and document storage

## Exit Scenario Modeling

Always model multiple exit values to understand founder proceeds under different term sheets:

```
Exit values to model: $10M, $50M, $100M, $500M

For each: calculate founder proceeds under
  - 1x non-participating preferred
  - 1x participating preferred
  - Current cap table ownership percentages
```

This reveals the true cost of unfavorable liquidation preferences at different exit sizes.
