"""
Database setup script
Run this to initialize the database and create all tables
"""
import os
import sys
from dotenv import load_dotenv
import pymysql
from app import create_app
from models import db, User, Category, Tag

# Load environment variables
load_dotenv()

def create_database():
    """Create database if it doesn't exist"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        db_name = os.getenv('DB_NAME', 'miniblog')
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{db_name}' created or already exists")
        
        connection.close()
        return True
    
    except Exception as e:
        print(f"✗ Error creating database: {str(e)}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✓ All tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {str(e)}")
        return False

def seed_initial_data():
    """Seed database with initial data"""
    try:
        app = create_app()
        with app.app_context():
            # Check if data already exists
            if User.query.first():
                print("ℹ Database already has data, skipping seed")
                return True
            
            # Create admin user
            admin = User(
                username='admin',
                email='admin@miniblog.com',
                full_name='Admin User',
                bio='Blog administrator',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create sample user
            user = User(
                username='john_doe',
                email='john@example.com',
                full_name='John Doe',
                bio='Tech enthusiast and writer'
            )
            user.set_password('password123')
            db.session.add(user)
            
            # Create categories
            categories_data = [
                {'name': 'Technology', 'slug': 'technology', 'description': 'All about tech'},
                {'name': 'Travel', 'slug': 'travel', 'description': 'Travel stories and tips'},
                {'name': 'Food', 'slug': 'food', 'description': 'Recipes and food reviews'},
                {'name': 'Lifestyle', 'slug': 'lifestyle', 'description': 'Lifestyle and wellness'},
                {'name': 'Tutorial', 'slug': 'tutorial', 'description': 'How-to guides and tutorials'}
            ]
            
            for cat_data in categories_data:
                category = Category(**cat_data)
                db.session.add(category)
            
            # Create tags
            tags_data = [
                'python', 'javascript', 'react', 'flask', 'web-development',
                'tutorial', 'beginner', 'advanced', 'tips', 'best-practices'
            ]
            
            for tag_name in tags_data:
                tag = Tag(name=tag_name, slug=tag_name.lower())
                db.session.add(tag)
            
            db.session.commit()
            print("✓ Initial data seeded successfully")
            print("\n📝 Login credentials:")
            print("   Admin: admin / admin123")
            print("   User:  john_doe / password123")
            
        return True
    
    except Exception as e:
        print(f"✗ Error seeding data: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("Mini Blog Database Setup")
    print("=" * 50)
    print()
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        sys.exit(1)
    print()
    
    # Step 2: Create tables
    print("Step 2: Creating tables...")
    if not create_tables():
        sys.exit(1)
    print()
    
    # Step 3: Seed initial data
    print("Step 3: Seeding initial data...")
    if not seed_initial_data():
        sys.exit(1)
    print()
    
    print("=" * 50)
    print("✓ Database setup completed successfully!")
    print("=" * 50)
    print("\nYou can now run the application with: python app.py")

if __name__ == '__main__':
    main()
