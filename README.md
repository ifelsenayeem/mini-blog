# Mini Blog Training Application

A well-designed mini-blog application for training purposes, featuring a React frontend and Python backend with MySQL database.

## 🏗️ Architecture Overview

This application is designed to be deployed in multiple ways:
- **Single EC2 Instance** - Simple deployment for quick setup
- **Serverless** - AWS Lambda + Amplify for scalability
- **Containerized** - Docker + AWS ECS for production-ready deployments

## 📁 Project Structure

```
mini-blog-training/
├── frontend/          # React application
├── backend/           # Python Flask API
├── docker/            # Docker configurations
└── docs/              # Additional documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- MySQL 8.0+
- Docker (optional)

### Running Locally

#### 1. Start the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py  # Initialize database
python app.py
```

The backend will run on `http://localhost:5000`

#### 2. Start the Frontend
```bash
cd frontend
npm install
npm start
```

The frontend will run on `http://localhost:3000`

### Running with Docker

```bash
docker-compose up --build
```

Access the application at `http://localhost:3000`

## 🎯 Features

- **User Authentication** - Login and registration
- **Blog Post Management** - Create, edit, and delete posts
- **Rich Text Editor** - Format your blog posts
- **Responsive Design** - Mobile-friendly interface
- **Comment System** - Engage with readers
- **Tags & Categories** - Organize your content
- **Search Functionality** - Find posts quickly

## 📚 API Documentation

See [API Documentation](docs/API.md) for detailed endpoint information.

## 🎓 Training Objectives

This project demonstrates:
1. React component architecture and state management
2. RESTful API design with Python Flask
3. MySQL database design and migrations
4. Modern deployment strategies (EC2, serverless, containers)
5. Security best practices
6. CI/CD pipeline setup

## 📦 Deployment Options

### Option 1: EC2 Deployment
See [EC2 Deployment Guide](docs/EC2_DEPLOYMENT.md)

### Option 2: Serverless (AWS Lambda + Amplify)
See [Serverless Deployment Guide](docs/SERVERLESS_DEPLOYMENT.md)

### Option 3: Docker + ECS
See [ECS Deployment Guide](docs/ECS_DEPLOYMENT.md)

## 🛠️ Technology Stack

**Frontend:**
- React 18
- React Router
- Axios
- TailwindCSS
- React Quill (Rich text editor)

**Backend:**
- Python 3.9+
- Flask
- SQLAlchemy
- MySQL
- JWT Authentication
- Flask-CORS

**DevOps:**
- Docker
- AWS (EC2, Lambda, Amplify, ECS)
- GitHub Actions

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- SQL injection protection via SQLAlchemy
- Environment variable management

## 📄 License

MIT License - Feel free to use this for training purposes.

## 🤝 Contributing

This is a training project. Feel free to fork and modify for your learning needs.
