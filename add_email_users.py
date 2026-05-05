"""
Script to add test users with email/password authentication
Run this once to create demo accounts for testing
"""

import hashlib
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "sqlite:///./analytics.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model (must match app.py)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    auth_type = Column(String, default="google")

# Create tables
Base.metadata.create_all(bind=engine)

def add_test_users():
    """Add test users with email/password authentication"""
    
    db = SessionLocal()
    
    test_users = [
        {
            "email": "admin@insightflow.ai",
            "password": "admin123",
            "name": "Admin User"
        },
        {
            "email": "demo@insightflow.ai",
            "password": "demo123",
            "name": "Demo User"
        },
        {
            "email": "test@gmail.com",
            "password": "test123",
            "name": "Test User"
        },
        {
            "email": "user@example.com",
            "password": "user123",
            "name": "Example User"
        }
    ]
    
    print("=" * 60)
    print("Adding Test Users to Database")
    print("=" * 60)
    
    for user_data in test_users:
        email = user_data["email"]
        password = user_data["password"]
        name = user_data["name"]
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        
        if existing_user:
            print(f"❌ User already exists: {email}")
            continue
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create new user
        new_user = User(
            email=email,
            name=name,
            password_hash=password_hash,
            auth_type="email",
            picture=""
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"✅ Created user: {email}")
        print(f"   Name: {name}")
        print(f"   Password: {password}")
        print(f"   User ID: {new_user.id}")
        print()
    
    db.close()
    
    print("=" * 60)
    print("Test User Credentials:")
    print("=" * 60)
    print("Email: admin@insightflow.ai")
    print("Password: admin123")
    print()
    print("Email: demo@insightflow.ai")
    print("Password: demo123")
    print()
    print("Email: test@gmail.com")
    print("Password: test123")
    print()
    print("Email: user@example.com")
    print("Password: user123")
    print("=" * 60)

if __name__ == "__main__":
    add_test_users()
