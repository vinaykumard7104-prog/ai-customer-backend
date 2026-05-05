"""
Initialize database with test users for email login
Run this script once to create test accounts
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
from app import Base, EmailUser

# Database setup
DATABASE_URL = "sqlite:///./analytics.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Create test users
def create_test_users():
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
            "password": "password123",
            "name": "Example User"
        }
    ]
    
    for user_data in test_users:
        # Check if user already exists
        existing_user = db.query(EmailUser).filter(
            EmailUser.email == user_data["email"]
        ).first()
        
        if not existing_user:
            # Hash password
            password_hash = hashlib.sha256(user_data["password"].encode()).hexdigest()
            
            # Create user
            new_user = EmailUser(
                email=user_data["email"],
                password=password_hash,
                name=user_data["name"],
                picture=""
            )
            
            db.add(new_user)
            print(f"✅ Created user: {user_data['email']} (password: {user_data['password']})")
        else:
            print(f"⏭️  User already exists: {user_data['email']}")
    
    db.commit()
    db.close()
    
    print("\n" + "="*60)
    print("✅ Database initialized successfully!")
    print("="*60)
    print("\n📱 Test Credentials for Android App:\n")
    for user_data in test_users:
        print(f"Email: {user_data['email']}")
        print(f"Password: {user_data['password']}\n")
    print("="*60)

if __name__ == "__main__":
    create_test_users()
