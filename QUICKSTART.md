# Quick Start Guide

Get the Mini Blog application running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] MySQL 8.0+ installed (or Docker)
- [ ] Git installed

## Option 1: Quick Start with Docker (Recommended)

**Easiest way to get started!**

```bash
# 1. Clone or navigate to the project
cd mini-blog-training

# 2. Start everything with Docker
docker-compose up --build

# 3. Wait for services to start (2-3 minutes)
# Backend will be at: http://localhost:5000
# Frontend will be at: http://localhost:3000
# MySQL will be at: localhost:3306
```

That's it! Open http://localhost:3000 in your browser.

**Default credentials:**
- Username: `admin` / Password: `admin123`
- Username: `john_doe` / Password: `password123`

## Option 2: Manual Setup

### Step 1: Setup Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials

# Initialize database
python setup_db.py

# Start backend server
python app.py
```

Backend running at http://localhost:5000 ✅

### Step 2: Setup Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Default API URL is already set

# Start frontend
npm start
```

Frontend opening at http://localhost:3000 ✅

### Step 3: Access the Application

Open http://localhost:3000 in your browser.

**Login with default credentials:**
- Admin: `admin` / `admin123`
- User: `john_doe` / `password123`

## What to Try First

1. **Browse Posts** - Check out the sample blog posts
2. **Login** - Use the credentials above
3. **Create a Post** - Click "Write" in the navigation
4. **Add Comments** - Comment on existing posts
5. **Edit Your Profile** - Update your user information

## Next Steps

### For Learning

1. **Explore the Code**
   - Backend: `backend/routes/` - API endpoints
   - Frontend: `frontend/src/pages/` - React components
   - Database: `backend/models.py` - Data models

2. **Read Documentation**
   - [API Documentation](docs/API.md)
   - [Backend README](backend/README.md)
   - [Frontend README](frontend/README.md)

3. **Try Adding Features**
   - See [CONTRIBUTING.md](CONTRIBUTING.md) for ideas

### For Deployment

Choose your deployment strategy:

1. **Single EC2 Instance** - [EC2 Deployment Guide](docs/EC2_DEPLOYMENT.md)
2. **Serverless (Lambda + Amplify)** - [Serverless Guide](docs/SERVERLESS_DEPLOYMENT.md)
3. **Containerized (ECS)** - [ECS Deployment Guide](docs/ECS_DEPLOYMENT.md)

## Troubleshooting

### Docker Issues

**Services not starting:**
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down
docker-compose up --build
```

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "3001:80"  # Frontend
  - "5001:5000"  # Backend
```

### Manual Setup Issues

**Backend won't start:**
```bash
# Check if MySQL is running
mysql --version

# Verify database exists
mysql -e "SHOW DATABASES;"

# Check Python version
python --version  # Should be 3.9+
```

**Frontend won't start:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Database errors:**
```bash
# Reset database (WARNING: Deletes all data)
cd backend
python setup_db.py
```

## Common Commands

### Backend

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run development server
python app.py

# Run production server
gunicorn --bind 0.0.0.0:5000 'app:create_app()'

# Reset database
python setup_db.py
```

### Frontend

```bash
# Development server
npm start

# Production build
npm run build

# Run tests
npm test
```

### Docker

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build
```

## Development Workflow

1. **Make changes** to code
2. **Test locally** - Backend and frontend auto-reload
3. **Commit changes** - Use conventional commit messages
4. **Push to GitHub** - Triggers CI/CD (if configured)
5. **Deploy** - Choose your deployment method

## File Structure Overview

```
mini-blog-training/
├── backend/              # Python Flask API
│   ├── routes/          # API endpoints
│   ├── models.py        # Database models
│   ├── app.py           # Main application
│   └── setup_db.py      # Database setup
├── frontend/            # React application
│   ├── src/
│   │   ├── pages/      # Page components
│   │   ├── components/ # Reusable components
│   │   └── services/   # API client
│   └── public/         # Static files
├── docs/               # Documentation
├── docker-compose.yml  # Docker configuration
└── README.md          # Main documentation
```

## Getting Help

- 📖 **Documentation**: Check the `docs/` folder
- 🐛 **Issues**: Found a bug? Open an issue on GitHub
- 💬 **Questions**: Check existing discussions or start a new one
- 🤝 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## What's Included

### Features
- ✅ User authentication (register, login, JWT)
- ✅ Blog post CRUD operations
- ✅ Rich text editor
- ✅ Comments and nested replies
- ✅ Categories and tags
- ✅ Responsive design
- ✅ MySQL database
- ✅ RESTful API
- ✅ Docker support
- ✅ Multiple deployment options

### Tech Stack
- **Backend**: Python, Flask, SQLAlchemy, MySQL, JWT
- **Frontend**: React, React Router, Tailwind CSS, Axios
- **DevOps**: Docker, AWS (EC2, Lambda, ECS, Amplify)

## Learning Resources

**Python/Flask:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

**React:**
- [React Documentation](https://react.dev/)
- [React Router](https://reactrouter.com/)

**Deployment:**
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Docker Documentation](https://docs.docker.com/)

## Ready to Build?

Now that everything is running, start building! 

Try these learning exercises:
1. Add a new API endpoint
2. Create a new React component
3. Add a new database model
4. Implement a new feature
5. Deploy to the cloud

Happy coding! 🚀
