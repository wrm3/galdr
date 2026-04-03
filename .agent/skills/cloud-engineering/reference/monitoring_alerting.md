# Monitoring & Alerting

CloudWatch/Stackdriver configurations, key metrics, and alert thresholds.

## Key Metrics to Monitor

| Service | Metric | Alert Threshold |
|---------|--------|-----------------|
| EC2 | CPUUtilization | >80% |
| RDS | CPUUtilization | >80% |
| RDS | FreeStorageSpace | <20% remaining |
| ALB | TargetResponseTime | >1s (P95) |
| ALB | HTTPCode_ELB_5XX | >1% of requests |
| Lambda | Errors | >1% of invocations |
| Lambda | Duration | >80% of timeout |
| SQS | ApproximateAgeOfOldestMessage | >5 min |
| DynamoDB | ThrottledRequests | >0 |

## CloudWatch Alarm (Terraform)

```hcl
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-utilization-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "CPU utilization exceeded 80%"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    InstanceId = aws_instance.web.id
  }
}
```

## GCP Cloud Monitoring Equivalent

```yaml
# Alert policy (gcloud or Terraform google_monitoring_alert_policy)
displayName: "High CPU Utilization"
conditions:
  - displayName: "CPU > 80%"
    conditionThreshold:
      filter: 'metric.type="compute.googleapis.com/instance/cpu/utilization"'
      comparison: COMPARISON_GT
      thresholdValue: 0.8
      duration: "300s"
      aggregations:
        - alignmentPeriod: "60s"
          perSeriesAligner: ALIGN_MEAN
notificationChannels:
  - projects/my-project/notificationChannels/12345
```

## Observability Stack Options

| Layer | AWS Native | Open Source | GCP Native |
|-------|-----------|-------------|------------|
| Metrics | CloudWatch | Prometheus + Grafana | Cloud Monitoring |
| Logs | CloudWatch Logs | ELK / Loki | Cloud Logging |
| Traces | X-Ray | Jaeger / Zipkin | Cloud Trace |
| Dashboards | CloudWatch Dashboards | Grafana | Cloud Monitoring |

## Dashboard Essentials

Every production service should have a dashboard showing:

1. **Request rate** — Requests per second over time
2. **Error rate** — 4xx and 5xx as percentage of total
3. **Latency** — P50, P95, P99 response times
4. **Saturation** — CPU, memory, disk, connection pool utilization
5. **Dependencies** — Health of downstream services and databases
