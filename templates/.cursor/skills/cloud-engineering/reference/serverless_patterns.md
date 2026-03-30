# Serverless Patterns

Lambda/Cloud Functions patterns, API Gateway integration, and event-driven architectures.

## Serverless Service Comparison

| Feature | AWS Lambda | GCP Cloud Functions | Azure Functions |
|---------|-----------|-------------------|-----------------|
| Max timeout | 15 min | 60 min (2nd gen) | 10 min (Consumption) |
| Max memory | 10 GB | 32 GB (2nd gen) | 1.5 GB (Consumption) |
| Languages | Node, Python, Java, Go, .NET, Ruby | Node, Python, Java, Go, .NET | Node, Python, Java, C#, PowerShell |
| Cold start | ~100-500ms | ~100-500ms | ~200-1000ms |
| Pricing | Per-invocation + duration | Per-invocation + duration | Per-execution + duration |

## Common Patterns

**REST API**
```
API Gateway → Lambda → DynamoDB
```

**Async Processing**
```
SQS Queue → Lambda → S3 / DynamoDB
```

**Event-Driven Pipeline**
```
S3 Upload → EventBridge → Lambda → SNS → Email
```

**Scheduled Job**
```
EventBridge Rule (cron) → Lambda → RDS / S3
```

**Stream Processing**
```
Kinesis / DynamoDB Streams → Lambda → ElasticSearch / S3
```

## Lambda Best Practices

1. **Keep functions small** — Single responsibility, <250 MB deployment package
2. **Minimize cold starts** — Use provisioned concurrency for latency-sensitive paths
3. **Set memory wisely** — CPU scales linearly with memory; profile to find the sweet spot
4. **Use layers** — Share common dependencies across functions
5. **Idempotent handlers** — Events may be delivered more than once
6. **Structured logging** — Use JSON logs with request IDs for traceability

## API Gateway Integration

```
HTTP API (v2):
- Lower cost (~$1/million requests)
- Lower latency
- JWT authorizers built-in
- Best for: most new APIs

REST API (v1):
- Request/response transformation
- WAF integration
- API keys and usage plans
- Best for: complex APIs needing fine-grained control
```

## Cost Optimization

- **Right-size memory**: Lambda charges per GB-second; over-provisioning wastes money
- **Use ARM (Graviton2)**: 20% cheaper, often faster than x86
- **Batch with SQS**: Process messages in batches of 10 instead of one-at-a-time
- **Avoid VPC unless needed**: VPC-attached Lambdas have longer cold starts
- **Reserved concurrency**: Prevent runaway costs from unexpected traffic spikes
