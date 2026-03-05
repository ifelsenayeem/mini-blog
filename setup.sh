#!/bin/bash

# Mini Blog Training - Setup Script
# This script helps you get the project running quickly

echo "=========================================="
echo "Mini Blog Training - Setup Script"
echo "=========================================="
echo ""

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "Choose setup method:"
echo "1) Docker (Recommended - Easiest)"
echo "2) Manual Setup (Backend + Frontend)"
echo "3) Backend Only"
echo "4) Frontend Only"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🐳 Setting up with Docker..."
        echo ""
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker is not installed. Please install Docker first."
            exit 1
        fi

        if ! command -v docker-compose &> /dev/null; then
            echo "❌ Docker Compose is not installed. Please install Docker Compose first."
            exit 1
        fi

        echo "✅ Docker found"
        echo ""
        echo "Starting services with Docker Compose..."
        docker-compose up --build -d
        
        echo ""
        echo "⏳ Waiting for services to start (30 seconds)..."
        sleep 30
        
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "📝 Access the application:"
        echo "   Frontend: http://localhost:3000"
        echo "   Backend API: http://localhost:5000"
        echo "   MySQL: localhost:3306"
        echo ""
        echo "🔐 Default login credentials:"
        echo "   Admin: admin / admin123"
        echo "   User: john_doe / password123"
        echo ""
        echo "📊 View logs: docker-compose logs -f"
        echo "🛑 Stop services: docker-compose down"
        ;;
        
    2)
        echo ""
        echo "🔧 Manual Setup - Backend + Frontend"
        echo ""
        
        # Check Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 is not installed"
            exit 1
        fi
        echo "✅ Python found: $(python3 --version)"
        
        # Check Node.js
        if ! command -v node &> /dev/null; then
            echo "❌ Node.js is not installed"
            exit 1
        fi
        echo "✅ Node.js found: $(node --version)"
        
        # Check MySQL
        if ! command -v mysql &> /dev/null; then
            echo "⚠️  MySQL not found. Make sure MySQL is installed and running."
        else
            echo "✅ MySQL found"
        fi
        
        echo ""
        echo "Setting up Backend..."
        cd backend
        
        # Setup Python virtual environment
        python3 -m venv venv
        source venv/bin/activate
        
        # Install dependencies
        pip install -r requirements.txt
        
        # Setup environment
        if [ ! -f ".env" ]; then
            cp .env.example .env
            echo "⚠️  Please edit backend/.env with your MySQL credentials"
            read -p "Press Enter after editing .env file..."
        fi
        
        # Initialize database
        echo "Initializing database..."
        python setup_db.py
        
        # Start backend in background
        echo "Starting backend server..."
        python app.py &
        BACKEND_PID=$!
        
        cd ..
        
        echo ""
        echo "Setting up Frontend..."
        cd frontend
        
        # Install dependencies
        npm install
        
        # Setup environment
        if [ ! -f ".env" ]; then
            cp .env.example .env
        fi
        
        # Start frontend
        echo "Starting frontend server..."
        npm start &
        FRONTEND_PID=$!
        
        cd ..
        
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "📝 Services running:"
        echo "   Backend PID: $BACKEND_PID"
        echo "   Frontend PID: $FRONTEND_PID"
        echo ""
        echo "🛑 To stop services:"
        echo "   kill $BACKEND_PID $FRONTEND_PID"
        ;;
        
    3)
        echo ""
        echo "🔧 Backend Only Setup"
        echo ""
        
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 is not installed"
            exit 1
        fi
        
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        
        if [ ! -f ".env" ]; then
            cp .env.example .env
            echo "⚠️  Please edit .env with your settings"
            read -p "Press Enter after editing .env file..."
        fi
        
        python setup_db.py
        
        echo ""
        echo "✅ Backend setup complete!"
        echo ""
        echo "To start the backend:"
        echo "   cd backend"
        echo "   source venv/bin/activate"
        echo "   python app.py"
        ;;
        
    4)
        echo ""
        echo "🔧 Frontend Only Setup"
        echo ""
        
        if ! command -v node &> /dev/null; then
            echo "❌ Node.js is not installed"
            exit 1
        fi
        
        cd frontend
        npm install
        
        if [ ! -f ".env" ]; then
            cp .env.example .env
        fi
        
        echo ""
        echo "✅ Frontend setup complete!"
        echo ""
        echo "To start the frontend:"
        echo "   cd frontend"
        echo "   npm start"
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "For more information, see:"
echo "   QUICKSTART.md - Quick start guide"
echo "   README.md - Full documentation"
echo "   docs/ - Deployment guides"
