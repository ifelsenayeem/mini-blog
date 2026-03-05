# ECS Deployment Guide (Docker + AWS ECS)

This guide demonstrates container-based deployment using AWS ECS (Elastic Container Service).

## Architecture Overview

- **Containers**: Docker containers for frontend and backend
- **Orchestration**: AWS ECS with Fargate
- **Load Balancer**: Application Load Balancer
- **Database**: Amazon RDS for MySQL
- **Registry**: Amazon ECR (Elastic Container Registry)

## Prerequisites

- AWS Account
- AWS CLI configured
- Docker installed
- ECS CLI installed

## Step 1: Setup ECR Repositories

```bash
# Create ECR repositories
aws ecr create-repository --repository-name miniblog-backend
aws ecr create-repository --repository-name miniblog-frontend

# Get registry URI
aws ecr describe-repositories --repository-names miniblog-backend miniblog-frontend
```

## Step 2: Build and Push Docker Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and tag backend
cd backend
docker build -t miniblog-backend .
docker tag miniblog-backend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/miniblog-backend:latest

# Push backend
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/miniblog-backend:latest

# Build and tag frontend
cd ../frontend
docker build -t miniblog-frontend .
docker tag miniblog-frontend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/miniblog-frontend:latest

# Push frontend
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/miniblog-frontend:latest
```

## Step 3: Create RDS Database

```bash
# Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name miniblog-db-subnet \
  --db-subnet-group-description "Mini Blog DB Subnet" \
  --subnet-ids subnet-xxxxx subnet-yyyyy

# Create security group
aws ec2 create-security-group \
  --group-name miniblog-db-sg \
  --description "Mini Blog RDS Security Group" \
  --vpc-id vpc-xxxxx

# Allow MySQL access from ECS
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 3306 \
  --source-group sg-ecs-xxxxx

# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier miniblog-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0 \
  --master-username admin \
  --master-user-password YourSecurePassword123! \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name miniblog-db-subnet \
  --db-name miniblog \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --publicly-accessible false
```

## Step 4: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name miniblog-cluster

# Or use Fargate (serverless containers)
aws ecs create-cluster \
  --cluster-name miniblog-cluster \
  --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy \
    capacityProvider=FARGATE,weight=1 \
    capacityProvider=FARGATE_SPOT,weight=1
```

## Step 5: Create Task Definitions

**backend-task-definition.json:**
```json
{
  "family": "miniblog-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/miniblog-backend:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        },
        {
          "name": "DB_HOST",
          "value": "your-rds-endpoint.rds.amazonaws.com"
        },
        {
          "name": "DB_PORT",
          "value": "3306"
        },
        {
          "name": "DB_NAME",
          "value": "miniblog"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:db-password"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/miniblog-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

**frontend-task-definition.json:**
```json
{
  "family": "miniblog-frontend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "frontend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/miniblog-frontend:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "REACT_APP_API_URL",
          "value": "https://api.yourdomain.com/api"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/miniblog-frontend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register task definitions:
```bash
aws ecs register-task-definition --cli-input-json file://backend-task-definition.json
aws ecs register-task-definition --cli-input-json file://frontend-task-definition.json
```

## Step 6: Create Application Load Balancer

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name miniblog-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --scheme internet-facing \
  --type application

# Create target groups
aws elbv2 create-target-group \
  --name miniblog-backend-tg \
  --protocol HTTP \
  --port 5000 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-path /health

aws elbv2 create-target-group \
  --name miniblog-frontend-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-path /

# Create listeners
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...

# Add rule for API routing
aws elbv2 create-rule \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --priority 1 \
  --conditions Field=path-pattern,Values='/api/*' \
  --actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:.../miniblog-backend-tg
```

## Step 7: Create ECS Services

```bash
# Backend service
aws ecs create-service \
  --cluster miniblog-cluster \
  --service-name miniblog-backend \
  --task-definition miniblog-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-xxxxx,subnet-yyyyy],
    securityGroups=[sg-xxxxx],
    assignPublicIp=DISABLED
  }" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:.../miniblog-backend-tg,
    containerName=backend,
    containerPort=5000"

# Frontend service
aws ecs create-service \
  --cluster miniblog-cluster \
  --service-name miniblog-frontend \
  --task-definition miniblog-frontend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-xxxxx,subnet-yyyyy],
    securityGroups=[sg-xxxxx],
    assignPublicIp=DISABLED
  }" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:.../miniblog-frontend-tg,
    containerName=frontend,
    containerPort=80"
```

## Step 8: Setup Auto Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/miniblog-cluster/miniblog-backend \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/miniblog-cluster/miniblog-backend \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    },
    "ScaleInCooldown": 300,
    "ScaleOutCooldown": 60
  }'
```

## Step 9: Configure SSL/TLS

```bash
# Request certificate from ACM
aws acm request-certificate \
  --domain-name yourdomain.com \
  --subject-alternative-names www.yourdomain.com \
  --validation-method DNS

# Create HTTPS listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

## Step 10: Database Initialization

Run a one-time task to initialize the database:

```bash
aws ecs run-task \
  --cluster miniblog-cluster \
  --task-definition miniblog-backend:1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-xxxxx],
    securityGroups=[sg-xxxxx],
    assignPublicIp=ENABLED
  }" \
  --overrides '{
    "containerOverrides": [{
      "name": "backend",
      "command": ["python", "setup_db.py"]
    }]
  }'
```

## Monitoring and Logging

### CloudWatch Logs

```bash
# View logs
aws logs tail /ecs/miniblog-backend --follow
aws logs tail /ecs/miniblog-frontend --follow
```

### CloudWatch Metrics

- CPU Utilization
- Memory Utilization
- Request Count
- Target Response Time

### Container Insights

```bash
# Enable Container Insights
aws ecs update-cluster-settings \
  --cluster miniblog-cluster \
  --settings name=containerInsights,value=enabled
```

## CI/CD Pipeline with GitHub Actions

**.github/workflows/ecs-deploy.yml:**
```yaml
name: Deploy to ECS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build and push backend
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: miniblog-backend
          IMAGE_TAG: ${{ github.sha }}
        run: |
          cd backend
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster miniblog-cluster \
            --service miniblog-backend \
            --force-new-deployment
```

## Cost Estimation

**Monthly costs:**
- ECS Fargate: ~$30-60 (2 tasks running 24/7)
- ALB: ~$20-25
- RDS t3.micro: ~$20-30
- ECR: ~$1-5
- Data transfer: ~$5-15
- **Total: ~$75-135/month**

## Performance Optimization

1. **Enable caching:**
   - CloudFront CDN for static assets
   - Redis/ElastiCache for session management

2. **Database optimization:**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **Container optimization:**
   - Multi-stage builds
   - Minimize image size
   - Use Alpine base images

## Troubleshooting

**Tasks not starting:**
```bash
aws ecs describe-tasks \
  --cluster miniblog-cluster \
  --tasks TASK_ARN
```

**Health checks failing:**
- Check security group rules
- Verify health check endpoint
- Review container logs

**High memory usage:**
- Increase task memory
- Optimize application code
- Add memory limits per container
