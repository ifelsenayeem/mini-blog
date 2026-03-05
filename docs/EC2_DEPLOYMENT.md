# EC2 Deployment Guide

This guide walks you through deploying the Mini Blog application on a single AWS EC2 instance.

## Prerequisites

- AWS account with EC2 access
- SSH key pair for EC2 access
- Domain name (optional, but recommended)

## Step 1: Launch EC2 Instance

1. **Launch an EC2 instance:**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.medium (or larger for production)
   - Storage: 20GB or more
   - Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS), 3000 (Frontend), 5000 (Backend)

2. **Connect to your instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

## Step 2: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Install MySQL
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv
```

## Step 3: Clone Repository

```bash
# Clone your repository
git clone https://github.com/your-username/mini-blog-training.git
cd mini-blog-training
```

## Step 4: Setup MySQL Database

```bash
# Set up MySQL
sudo mysql

# In MySQL shell:
CREATE DATABASE miniblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bloguser'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON miniblog.* TO 'bloguser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Step 5: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Initialize database
python setup_db.py

# Test the backend
python app.py
```

## Step 6: Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
nano .env  # Update REACT_APP_API_URL to your EC2 public IP

# Build for production
npm run build
```

## Step 7: Setup for Production

### Option A: Using Docker Compose (Recommended)

```bash
cd ..

# Update docker-compose.yml with production settings
nano docker-compose.yml

# Start services
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

### Option B: Using systemd services

**Backend Service:**

```bash
sudo nano /etc/systemd/system/miniblog-backend.service
```

```ini
[Unit]
Description=Mini Blog Backend
After=network.target mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/mini-blog-training/backend
Environment="PATH=/home/ubuntu/mini-blog-training/backend/venv/bin"
ExecStart=/home/ubuntu/mini-blog-training/backend/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 'app:create_app()'
Restart=always

[Install]
WantedBy=multi-user.target
```

**Frontend with Nginx:**

```bash
# Install Nginx
sudo apt install -y nginx

# Copy build files
sudo cp -r /home/ubuntu/mini-blog-training/frontend/build/* /var/www/html/

# Configure Nginx
sudo nano /etc/nginx/sites-available/miniblog
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or EC2 public IP
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/miniblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start backend service
sudo systemctl start miniblog-backend
sudo systemctl enable miniblog-backend
```

## Step 8: Setup SSL (Optional but Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

## Step 9: Monitoring and Logs

```bash
# Check backend logs
sudo journalctl -u miniblog-backend -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Docker logs (if using Docker)
docker-compose logs -f
```

## Maintenance

### Update Application

```bash
cd mini-blog-training
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart miniblog-backend

# Frontend
cd ../frontend
npm install
npm run build
sudo cp -r build/* /var/www/html/
sudo systemctl restart nginx
```

### Backup Database

```bash
# Backup
mysqldump -u bloguser -p miniblog > backup_$(date +%Y%m%d).sql

# Restore
mysql -u bloguser -p miniblog < backup_20260305.sql
```

## Troubleshooting

**Backend not starting:**
- Check logs: `sudo journalctl -u miniblog-backend -n 50`
- Verify database connection: `mysql -u bloguser -p -e "SHOW DATABASES;"`
- Check if port is available: `sudo netstat -tulpn | grep 5000`

**Frontend showing blank page:**
- Check Nginx config: `sudo nginx -t`
- Verify API URL in frontend build
- Check browser console for errors

**Database connection errors:**
- Verify MySQL is running: `sudo systemctl status mysql`
- Check credentials in .env file
- Verify user permissions in MySQL

## Security Best Practices

1. Change all default passwords
2. Keep system updated: `sudo apt update && sudo apt upgrade`
3. Configure firewall: `sudo ufw enable`
4. Use SSH keys instead of passwords
5. Enable fail2ban: `sudo apt install fail2ban`
6. Regular backups
7. Monitor logs regularly
