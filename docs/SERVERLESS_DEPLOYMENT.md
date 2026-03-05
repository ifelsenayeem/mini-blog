# Serverless Deployment Guide (AWS Lambda + Amplify)

This guide shows how to deploy the Mini Blog application using AWS serverless technologies.

## Architecture Overview

- **Frontend**: AWS Amplify (Static hosting)
- **Backend API**: AWS Lambda + API Gateway
- **Database**: Amazon RDS for MySQL
- **Storage**: Amazon S3 (for uploads)

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Node.js 18+
- Python 3.9+

## Part 1: Backend - AWS Lambda

### Step 1: Prepare Backend for Lambda

Create a Lambda handler file:

**backend/lambda_handler.py:**
```python
import os
os.environ['FLASK_ENV'] = 'production'

from app import create_app

app = create_app('production')

def lambda_handler(event, context):
    """AWS Lambda handler"""
    from aws_wsgi import response
    return response(app, event, context)
```

**backend/requirements-lambda.txt:**
```
aws-wsgi==0.2.7
-r requirements.txt
```

### Step 2: Setup RDS MySQL Database

1. **Create RDS Instance:**
   ```bash
   aws rds create-db-instance \
     --db-instance-identifier miniblog-db \
     --db-instance-class db.t3.micro \
     --engine mysql \
     --master-username admin \
     --master-user-password YourPassword123! \
     --allocated-storage 20 \
     --vpc-security-group-ids sg-xxxxxxxx \
     --db-name miniblog
   ```

2. **Get RDS endpoint:**
   ```bash
   aws rds describe-db-instances \
     --db-instance-identifier miniblog-db \
     --query 'DBInstances[0].Endpoint.Address'
   ```

### Step 3: Package Lambda Deployment

```bash
cd backend

# Create deployment package
mkdir lambda_package
pip install -r requirements-lambda.txt -t lambda_package/
cp -r *.py routes/ lambda_package/

# Create ZIP
cd lambda_package
zip -r ../lambda_deployment.zip .
cd ..
```

### Step 4: Create Lambda Function

```bash
# Create IAM role for Lambda
aws iam create-role \
  --role-name MiniBlogLambdaRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policies
aws iam attach-role-policy \
  --role-name MiniBlogLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole

# Create Lambda function
aws lambda create-function \
  --function-name MiniBlogAPI \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/MiniBlogLambdaRole \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://lambda_deployment.zip \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{
    DB_HOST=your-rds-endpoint.rds.amazonaws.com,
    DB_USER=admin,
    DB_PASSWORD=YourPassword123!,
    DB_NAME=miniblog,
    SECRET_KEY=your-secret-key,
    JWT_SECRET_KEY=your-jwt-secret
  }"
```

### Step 5: Setup API Gateway

1. **Create REST API:**
   ```bash
   aws apigateway create-rest-api \
     --name MiniBlogAPI \
     --description "Mini Blog REST API"
   ```

2. **Configure proxy integration:**
   - Use {proxy+} resource
   - ANY method
   - Lambda proxy integration

3. **Deploy API:**
   ```bash
   aws apigateway create-deployment \
     --rest-api-id YOUR_API_ID \
     --stage-name prod
   ```

Your API will be available at:
`https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/api`

### Alternative: Using Serverless Framework

Install Serverless:
```bash
npm install -g serverless
```

**serverless.yml:**
```yaml
service: miniblog-api

provider:
  name: aws
  runtime: python3.9
  stage: prod
  region: us-east-1
  environment:
    DB_HOST: ${env:DB_HOST}
    DB_USER: ${env:DB_USER}
    DB_PASSWORD: ${env:DB_PASSWORD}
    DB_NAME: miniblog
    SECRET_KEY: ${env:SECRET_KEY}
    JWT_SECRET_KEY: ${env:JWT_SECRET_KEY}

functions:
  api:
    handler: lambda_handler.lambda_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    timeout: 30
    memorySize: 512

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: true
```

Deploy:
```bash
serverless deploy
```

## Part 2: Frontend - AWS Amplify

### Step 1: Install Amplify CLI

```bash
npm install -g @aws-amplify/cli
amplify configure
```

### Step 2: Initialize Amplify in Frontend

```bash
cd frontend
amplify init
```

Follow prompts:
- Project name: miniblog-frontend
- Environment: production
- Default editor: Visual Studio Code
- App type: javascript
- Framework: react
- Source directory: src
- Build directory: build
- Build command: npm run build
- Start command: npm start

### Step 3: Configure Environment

Update **.env.production:**
```env
REACT_APP_API_URL=https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/api
```

### Step 4: Deploy to Amplify

**Option A: Using Amplify Console (Recommended)**

1. Go to AWS Amplify Console
2. Connect your GitHub repository
3. Configure build settings:

**amplify.yml:**
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

4. Deploy automatically on push to main branch

**Option B: Using CLI**

```bash
amplify hosting add

# Choose:
# - Hosting with Amplify Console
# - Manual deployment

amplify publish
```

## Part 3: Database Migration

Initialize database on RDS:

```bash
# Connect to RDS
mysql -h your-rds-endpoint.rds.amazonaws.com -u admin -p

# Run migrations
python setup_db.py
```

Or create a one-time Lambda function for initialization.

## Part 4: Additional Services

### S3 for File Uploads

```bash
# Create S3 bucket
aws s3 mb s3://miniblog-uploads

# Set bucket policy for public read
aws s3api put-bucket-policy \
  --bucket miniblog-uploads \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::miniblog-uploads/*"
    }]
  }'

# Update Lambda IAM role to allow S3 access
```

### CloudFront CDN (Optional)

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name miniblog-uploads.s3.amazonaws.com
```

## Cost Estimation

**Monthly costs (assuming moderate traffic):**
- Lambda: ~$5-20 (1M requests)
- API Gateway: ~$3-10
- RDS t3.micro: ~$20-30
- Amplify Hosting: ~$0-5 (first 1000 build minutes free)
- S3: ~$1-5
- **Total: ~$30-70/month**

Free tier covers most of this for the first year!

## Monitoring and Logs

```bash
# View Lambda logs
aws logs tail /aws/lambda/MiniBlogAPI --follow

# View metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=MiniBlogAPI \
  --start-time 2026-03-05T00:00:00Z \
  --end-time 2026-03-06T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## Scaling Considerations

**Lambda:**
- Auto-scales automatically
- Can handle 1000s of concurrent requests
- Configure reserved concurrency if needed

**RDS:**
- Start with t3.micro
- Upgrade to t3.small or larger as needed
- Enable read replicas for high read traffic

**Frontend:**
- Amplify scales automatically
- CloudFront CDN for global performance

## CI/CD with GitHub Actions

**.github/workflows/deploy.yml:**
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Lambda
        run: |
          cd backend
          pip install -r requirements-lambda.txt -t lambda_package/
          cd lambda_package && zip -r ../lambda.zip .
          aws lambda update-function-code \
            --function-name MiniBlogAPI \
            --zip-file fileb://lambda.zip
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Amplify
        run: |
          cd frontend
          npm ci
          npm run build
          amplify publish --yes
```

## Troubleshooting

**Lambda timeout:**
- Increase timeout in Lambda configuration
- Optimize database queries
- Add database connection pooling

**CORS errors:**
- Verify API Gateway CORS settings
- Check Lambda response headers

**Cold starts:**
- Use provisioned concurrency
- Optimize imports and initialization
- Consider Lambda SnapStart (Java only currently)
