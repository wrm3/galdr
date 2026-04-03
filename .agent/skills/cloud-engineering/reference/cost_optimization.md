# Cost Optimization

Pricing strategies, reserved instances, lifecycle policies, and monthly cost review checklists.

## Quick Wins

| Strategy | Savings | Effort |
|----------|---------|--------|
| Reserved Instances (1yr) | 30-40% | Low |
| Spot Instances | 60-90% | Medium |
| Right-sizing | 20-50% | Medium |
| S3 Lifecycle Policies | 30-70% | Low |
| Scheduled scaling | 20-40% | Medium |

## Reserved vs Spot vs On-Demand

| Type | Best For | Savings | Risk |
|------|----------|---------|------|
| On-Demand | Variable workloads, testing | 0% | None |
| Reserved (1yr) | Steady workloads | 30-40% | Commitment |
| Reserved (3yr) | Long-term stable | 50-60% | Commitment |
| Spot | Fault-tolerant, batch jobs | 60-90% | Interruption |
| Savings Plans | Flexible commitment | 30-40% | Commitment |

## S3 Lifecycle Policy

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

## Cost Allocation Tags

Always tag resources for cost attribution:

```hcl
tags = {
  Name        = "web-server-1"
  Environment = "production"
  Team        = "platform"
  CostCenter  = "engineering"
  Project     = "main-app"
}
```

## Monthly Cost Checklist

```
□ Review Cost Explorer
  □ Check for unexpected spikes
  □ Identify unused resources
  □ Review Reserved Instance coverage

□ Right-sizing
  □ Check EC2 CPU/memory utilization
  □ Review RDS instance sizes
  □ Check Lambda memory settings

□ Storage
  □ Review S3 storage classes
  □ Delete old snapshots
  □ Clean up unused EBS volumes

□ Network
  □ Check NAT Gateway usage
  □ Review data transfer costs
  □ Optimize CloudFront caching
```

## GCP-Specific Savings

- **Sustained-use discounts**: Automatic 30% discount for instances running >25% of month
- **Committed-use discounts**: 1yr (37%) or 3yr (55%) for vCPU/memory commitments
- **Preemptible VMs**: Up to 80% discount, 24hr max lifetime
- **Flat-rate BigQuery**: Predictable pricing for heavy analytics workloads

## Azure-Specific Savings

- **Reserved Instances**: 1yr (30-40%) or 3yr (50-60%)
- **Azure Hybrid Benefit**: Use existing Windows/SQL licenses for up to 85% savings
- **Spot VMs**: Up to 90% discount for interruptible workloads
- **Dev/Test pricing**: Reduced rates for non-production environments
