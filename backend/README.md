# Mini Blog Backend

Python Flask REST API for the Mini Blog training application.

## Technology Stack

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **MySQL** - Database
- **JWT** - Authentication
- **bcrypt** - Password hashing
- **Flask-CORS** - CORS support
- **Gunicorn** - Production server

## Project Structure

```
backend/
├── app.py                 # Main application file
├── config.py             # Configuration management
├── models.py             # Database models
├── auth.py               # Authentication utilities
├── setup_db.py           # Database initialization script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── Dockerfile           # Docker configuration
└── routes/              # API route handlers
    ├── auth.py          # Authentication endpoints
    ├── posts.py         # Blog post endpoints
    ├── comments.py      # Comment endpoints
    └── categories_tags.py # Categories and tags endpoints
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

Required environment variables:
- `DB_HOST` - MySQL host (default: localhost)
- `DB_PORT` - MySQL port (default: 3306)
- `DB_USER` - MySQL username
- `DB_PASSWORD` - MySQL password
- `DB_NAME` - Database name
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret key

### 4. Initialize Database

```bash
# Run setup script
python setup_db.py
```

This will:
- Create the database if it doesn't exist
- Create all tables
- Seed initial data (categories, tags, sample users)

Default login credentials:
- Admin: `admin` / `admin123`
- User: `john_doe` / `password123`

### 5. Run Development Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 6. Run Production Server

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 'app:create_app()'
```

## API Endpoints

See [API Documentation](../docs/API.md) for detailed endpoint information.

### Quick Reference

**Authentication:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

**Posts:**
- `GET /api/posts` - List posts
- `GET /api/posts/:id` - Get single post
- `POST /api/posts` - Create post (auth required)
- `PUT /api/posts/:id` - Update post (auth required)
- `DELETE /api/posts/:id` - Delete post (auth required)

**Comments:**
- `GET /api/comments?post_id=:id` - Get comments for post
- `POST /api/comments` - Create comment (auth required)

**Categories & Tags:**
- `GET /api/categories` - List categories
- `GET /api/tags` - List tags

## Database Schema

### Users Table
- id (PK)
- username (unique)
- email (unique)
- password_hash
- full_name
- bio
- avatar_url
- is_active
- is_admin
- created_at
- updated_at

### Posts Table
- id (PK)
- title
- slug (unique)
- content
- excerpt
- featured_image
- status (draft/published/archived)
- view_count
- author_id (FK -> users)
- category_id (FK -> categories)
- published_at
- created_at
- updated_at

### Comments Table
- id (PK)
- content
- author_id (FK -> users)
- post_id (FK -> posts)
- parent_id (FK -> comments, for nested comments)
- is_approved
- created_at
- updated_at

### Categories Table
- id (PK)
- name (unique)
- slug (unique)
- description
- created_at

### Tags Table
- id (PK)
- name (unique)
- slug (unique)
- created_at

## Testing

```bash
# Run tests (when implemented)
python -m pytest

# Check code style
flake8 .

# Type checking
mypy .
```

## Docker

```bash
# Build image
docker build -t miniblog-backend .

# Run container
docker run -p 5000:5000 \
  -e DB_HOST=host.docker.internal \
  -e DB_PASSWORD=yourpassword \
  miniblog-backend
```

## Common Tasks

### Create Admin User

```python
from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    user = User(
        username='admin',
        email='admin@example.com',
        is_admin=True
    )
    user.set_password('secure_password')
    db.session.add(user)
    db.session.commit()
```

### Database Migration

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Reset Database

```bash
python setup_db.py
```

Warning: This will delete all existing data!

## Troubleshooting

**Import errors:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Database connection errors:**
- Verify MySQL is running: `mysql --version`
- Check credentials in .env file
- Ensure database exists: `mysql -e "SHOW DATABASES;"`

**Permission errors:**
- Check MySQL user permissions
- Verify file/directory permissions

## Security Notes

- Change default SECRET_KEY and JWT_SECRET_KEY in production
- Use strong passwords for database and admin users
- Enable HTTPS in production
- Keep dependencies updated
- Use environment variables for sensitive data
- Implement rate limiting for production

## Contributing

This is a training project. Feel free to add features:
- Rate limiting
- Email verification
- Password reset
- Image upload to S3
- Full-text search
- API versioning
- GraphQL endpoint
