# Kubernetes Configurations

Deployment YAMLs, service definitions, Helm patterns, and managed K8s comparison.

## Managed Kubernetes Comparison

| Feature | EKS (AWS) | GKE (GCP) | AKS (Azure) |
|---------|-----------|-----------|--------------|
| Control plane cost | $0.10/hr | Free (Autopilot: per-pod) | Free |
| Auto-scaling | Karpenter / Cluster Autoscaler | Autopilot / Node Auto-provisioning | KEDA / Cluster Autoscaler |
| Service mesh | App Mesh | Anthos Service Mesh | Open Service Mesh |
| Best for | AWS-native workloads | K8s-first teams | Azure/Microsoft shops |

## Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
        - name: web-app
          image: myregistry/web-app:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

## Service (LoadBalancer)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
```

## Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Helm Chart Structure

```
my-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   └── _helpers.tpl
└── charts/           # sub-chart dependencies
```

## Helm Commands

```bash
helm repo add stable https://charts.helm.sh/stable
helm search repo nginx
helm install my-release stable/nginx-ingress
helm upgrade my-release stable/nginx-ingress --set controller.replicaCount=3
helm rollback my-release 1
helm uninstall my-release
```
