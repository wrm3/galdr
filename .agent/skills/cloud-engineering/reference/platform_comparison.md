# Cloud Platform Comparison

Service mapping and selection criteria for AWS, GCP, and Azure.

## Service Mapping

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Compute | EC2, ECS, Lambda | GCE, GKE, Cloud Run | VMs, AKS, Functions |
| Database | RDS, DynamoDB | Cloud SQL, Firestore | SQL DB, Cosmos DB |
| Storage | S3 | Cloud Storage | Blob Storage |
| Kubernetes | EKS | GKE | AKS |
| Serverless | Lambda | Cloud Functions | Functions |
| CDN | CloudFront | Cloud CDN | Azure CDN |
| DNS | Route 53 | Cloud DNS | Azure DNS |
| IAM | IAM | Cloud IAM | Entra ID |
| Secrets | Secrets Manager | Secret Manager | Key Vault |
| Monitoring | CloudWatch | Cloud Monitoring | Azure Monitor |

## Platform Selection Criteria

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Enterprise/Legacy | AWS or Azure | Mature ecosystem, compliance certifications |
| ML/Data | GCP | BigQuery, Vertex AI, TPU access |
| Kubernetes | GCP (GKE) | Best managed K8s, Autopilot mode |
| Microsoft stack | Azure | Native integration with AD, Office 365 |
| Startups | AWS | Widest adoption, most third-party tooling |
| Cost-sensitive | GCP | Sustained-use discounts, committed-use pricing |

## AWS Compute Options

| Service | Use Case | Pricing Model |
|---------|----------|---------------|
| EC2 | General compute | Per-hour |
| ECS/Fargate | Containers | Per-vCPU/memory |
| Lambda | Event-driven | Per-invocation |
| App Runner | Simple containers | Per-vCPU/memory |

### EC2 Instance Families

```
General Purpose (M-series): Balanced compute/memory
- m6i.large: 2 vCPU, 8 GB — ~$0.096/hr
- m6i.xlarge: 4 vCPU, 16 GB — ~$0.192/hr

Compute Optimized (C-series): CPU-intensive workloads
- c6i.large: 2 vCPU, 4 GB — ~$0.085/hr
- c6i.xlarge: 4 vCPU, 8 GB — ~$0.170/hr

Memory Optimized (R-series): Memory-intensive workloads
- r6i.large: 2 vCPU, 16 GB — ~$0.126/hr
- r6i.xlarge: 4 vCPU, 32 GB — ~$0.252/hr

GPU (P/G-series): ML/Graphics
- g4dn.xlarge: 4 vCPU, 16 GB, T4 GPU — ~$0.526/hr
- p4d.24xlarge: 96 vCPU, 1152 GB, 8x A100 — ~$32.77/hr
```

## Common AWS Architectures

**Web Application (Standard)**
```
CloudFront → ALB → ECS/EC2 → RDS
                 ↓
              ElastiCache
```

**Serverless**
```
API Gateway → Lambda → DynamoDB
                    ↓
                   S3
```

**Event-Driven**
```
SQS/SNS → Lambda → DynamoDB
   ↑
EventBridge
```

## Multi-Cloud Strategy

**Go multi-cloud when:**
- Regulatory requirements demand it
- Vendor negotiation leverage is needed
- Best-of-breed services span providers
- Disaster recovery requires provider diversity

**Stay single-cloud when:**
- Small team (complexity hurts velocity)
- Limited budget
- No specific regulatory requirement

**Cloud-agnostic technologies:**
- Kubernetes (runs anywhere)
- Terraform (multi-cloud IaC)
- PostgreSQL (managed or self-hosted)
- Redis (managed or self-hosted)
- S3-compatible storage APIs
