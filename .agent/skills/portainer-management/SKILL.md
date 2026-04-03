---
name: portainer-management
description: Portainer CE/BE—stacks, Docker/Swarm/K8s environments, RBAC, API, and Edge agents.
---

# Portainer Management Skill

Comprehensive Portainer container management platform operations for Docker and Kubernetes environments.

## Overview

This skill provides:
- **Portainer Setup**: Installation and configuration for CE/BE
- **Environment Management**: Docker, Swarm, Kubernetes, Edge
- **Stack Deployments**: Compose stacks, GitOps integration
- **User Management**: RBAC, teams, OAuth/LDAP
- **API Operations**: Programmatic access and automation
- **Edge Computing**: Remote environment management

## When to Use This Skill

Activate when the user needs to:
- Install or configure Portainer
- Deploy stacks through Portainer
- Manage container environments
- Configure user access and RBAC
- Set up Edge agents
- Use Portainer API
- Troubleshoot Portainer issues

## Prerequisites

### Portainer Access
```bash
# Portainer URL (replace with actual)
PORTAINER_URL=https://portainer.example.com

# Check Portainer health
curl -k ${PORTAINER_URL}/api/status
```

### API Authentication
```bash
# Get JWT token
TOKEN=$(curl -s -X POST "${PORTAINER_URL}/api/auth" \
  -H "Content-Type: application/json" \
  -d '{"Username":"admin","Password":"yourpassword"}' \
  --insecure | jq -r '.jwt')

# Verify token
echo $TOKEN
```

## Core Workflows

### 1. Install Portainer

**Docker Standalone:**
```bash
# Create volume
docker volume create portainer_data

# Deploy Portainer CE
docker run -d \
  --name portainer \
  --restart=always \
  -p 8000:8000 \
  -p 9443:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

# Access at https://localhost:9443
```

**Docker Swarm:**
```bash
# Deploy as stack
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-stack.yml
docker stack deploy -c portainer-stack.yml portainer
```

**Kubernetes:**
```bash
# Using Helm
helm repo add portainer https://portainer.github.io/k8s/
helm repo update
helm upgrade --install portainer portainer/portainer \
  --create-namespace \
  --namespace portainer \
  --set service.type=LoadBalancer
```

### 2. Deploy Stack

**Via API:**
```bash
# Create stack from inline compose
curl -X POST "${PORTAINER_URL}/api/stacks/create/standalone/string?endpointId=1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "myapp",
    "stackFileContent": "version: '\''3.8'\''\nservices:\n  web:\n    image: nginx:alpine\n    ports:\n      - \"80:80\""
  }' --insecure
```

**Via Git Repository:**
```bash
curl -X POST "${PORTAINER_URL}/api/stacks/create/standalone/repository?endpointId=1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "myapp",
    "repositoryURL": "https://github.com/user/repo",
    "repositoryReferenceName": "refs/heads/main",
    "composeFile": "docker-compose.yml",
    "env": [
      {"name": "DB_PASSWORD", "value": "secret"}
    ]
  }' --insecure
```

### 3. Manage Environments

**List Environments:**
```bash
curl -X GET "${PORTAINER_URL}/api/endpoints" \
  -H "Authorization: Bearer ${TOKEN}" \
  --insecure | jq
```

**Add Docker Environment:**
```bash
curl -X POST "${PORTAINER_URL}/api/endpoints" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: multipart/form-data" \
  -F "Name=production" \
  -F "EndpointCreationType=1" \
  -F "URL=tcp://docker.example.com:2376" \
  --insecure
```

### 4. Edge Agent Setup

**Generate Edge Key:**
```bash
# Via UI: Environments > Add environment > Edge Agent > Generate key

# Or via API
EDGE_KEY=$(curl -X POST "${PORTAINER_URL}/api/endpoints" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "edge-device-1",
    "EndpointCreationType": 4
  }' --insecure | jq -r '.EdgeKey')
```

**Deploy Edge Agent:**
```bash
docker run -d \
  --name portainer_edge_agent \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /var/lib/docker/volumes:/var/lib/docker/volumes \
  -e EDGE=1 \
  -e EDGE_ID=<edge_id> \
  -e EDGE_KEY=${EDGE_KEY} \
  -e EDGE_INSECURE_POLL=1 \
  portainer/agent:latest
```

## API Reference

### Authentication
```bash
# Login
curl -X POST "${PORTAINER_URL}/api/auth" \
  -H "Content-Type: application/json" \
  -d '{"Username":"admin","Password":"password"}' \
  --insecure

# Response: {"jwt":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

### Stacks
```bash
# List stacks
curl -X GET "${PORTAINER_URL}/api/stacks" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Get stack
curl -X GET "${PORTAINER_URL}/api/stacks/{id}" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Update stack
curl -X PUT "${PORTAINER_URL}/api/stacks/{id}?endpointId=1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"stackFileContent":"...","env":[],"prune":false}' --insecure

# Delete stack
curl -X DELETE "${PORTAINER_URL}/api/stacks/{id}?endpointId=1" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Start/Stop stack
curl -X POST "${PORTAINER_URL}/api/stacks/{id}/start?endpointId=1" \
  -H "Authorization: Bearer ${TOKEN}" --insecure
curl -X POST "${PORTAINER_URL}/api/stacks/{id}/stop?endpointId=1" \
  -H "Authorization: Bearer ${TOKEN}" --insecure
```

### Containers
```bash
# List containers
curl -X GET "${PORTAINER_URL}/api/endpoints/{endpointId}/docker/containers/json?all=true" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Start container
curl -X POST "${PORTAINER_URL}/api/endpoints/{endpointId}/docker/containers/{id}/start" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Stop container
curl -X POST "${PORTAINER_URL}/api/endpoints/{endpointId}/docker/containers/{id}/stop" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Restart container
curl -X POST "${PORTAINER_URL}/api/endpoints/{endpointId}/docker/containers/{id}/restart" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Get logs
curl -X GET "${PORTAINER_URL}/api/endpoints/{endpointId}/docker/containers/{id}/logs?stdout=true&stderr=true&tail=100" \
  -H "Authorization: Bearer ${TOKEN}" --insecure
```

### Users and Teams
```bash
# List users
curl -X GET "${PORTAINER_URL}/api/users" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Create user
curl -X POST "${PORTAINER_URL}/api/users" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"password123","role":2}' --insecure

# List teams
curl -X GET "${PORTAINER_URL}/api/teams" \
  -H "Authorization: Bearer ${TOKEN}" --insecure

# Create team
curl -X POST "${PORTAINER_URL}/api/teams" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name":"developers"}' --insecure
```

## Stack Templates

### Web Application Stack
```yaml
version: '3.8'

services:
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
    networks:
      - web

  backend:
    image: ${BACKEND_IMAGE}
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - database
      - redis
    networks:
      - web
      - backend

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - backend

networks:
  web:
  backend:

volumes:
  postgres_data:
  redis_data:
```

### Monitoring Stack
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'

volumes:
  prometheus_data:
  grafana_data:
```

## Best Practices

### Do ✅
- Use HTTPS for Portainer access
- Enable RBAC and team-based access
- Use GitOps for stack deployments
- Set up automatic backups
- Use environment variables for secrets
- Enable audit logging
- Use Edge agents for remote sites
- Regular updates to latest version

### Don't ❌
- Expose Portainer without TLS
- Use admin for everything
- Store secrets in stack files
- Skip access control setup
- Deploy directly without stacks
- Ignore update notifications
- Use default passwords
- Skip backup configuration

## Backup & Recovery

### Backup Portainer
```bash
# Stop Portainer
docker stop portainer

# Backup data
docker run --rm \
  -v portainer_data:/data \
  -v $(pwd):/backup \
  alpine tar cvf /backup/portainer-backup-$(date +%Y%m%d).tar /data

# Start Portainer
docker start portainer
```

### Restore Portainer
```bash
# Stop Portainer
docker stop portainer

# Restore data
docker run --rm \
  -v portainer_data:/data \
  -v $(pwd):/backup \
  alpine sh -c "rm -rf /data/* && tar xvf /backup/portainer-backup.tar -C /"

# Start Portainer
docker start portainer
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Agent connection failed | Check network connectivity, verify ports 9001/8000 |
| Stack deployment failed | Validate compose syntax, check environment variables |
| Cannot access endpoint | Verify Docker socket permissions, check TLS certs |
| Edge agent offline | Check edge key, verify outbound connectivity |
| Authentication failed | Reset admin password via CLI |

### Reset Admin Password
```bash
docker exec -it portainer /bin/sh
# Inside container:
./portainer --admin-password-reset
```

## Related Skills
- **kubernetes-operations**: K8s cluster management
- **docker-specialist**: Container optimization
- **cicd-pipelines**: Deployment automation
- **devops-engineer**: Infrastructure automation

## Related Agents
- `portainer-specialist`: Full Portainer expertise
- `docker-specialist`: Container management
- `devops-engineer`: Infrastructure automation
- `security-auditor`: Security review

---

**Note:** Portainer simplifies container management but still requires proper security practices. Use it as a management layer, not a replacement for good DevOps practices.
