#!/usr/bin/env python3
"""
InsightFlow AI Backend - Startup Script
Initializes database and starts the server
"""
import os
import sys
import subprocess

def print_banner():
    print("=" * 70)
    print("  InsightFlow AI - Backend Server")
    print("  Customer Intelligence Platform")
    print("=" * 70)
    print()

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Dependencies check passed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def initialize_database():
    """Initialize database with test users"""
    print("\n🗄️  Initializing database...")
    
    if os.path.exists("analytics.db"):
        print("   Database already exists")
    else:
        print("   Creating new database...")
    
    try:
        subprocess.run([sys.executable, "init_users.py"], check=True)
    except subprocess.CalledProcessError:
        print("   ⚠️  Could not initialize users (might already exist)")

def show_test_credentials():
    """Display test credentials"""
    print("\n" + "=" * 70)
    print("  📱 TEST CREDENTIALS FOR ANDROID APP")
    print("=" * 70)
    print("\n  Email Login:")
    print("  • admin@insightflow.ai  /  admin123")
    print("  • demo@insightflow.ai   /  demo123")
    print("  • test@gmail.com        /  test123")
    print("\n" + "=" * 70)

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting server...")
    print("\n📝 API Documentation will be available at:")
    print("   http://localhost:8000/docs")
    print("\n📍 Server running on:")
    print("   http://0.0.0.0:8000")
    print("\n💡 For Android Emulator, use: http://10.0.2.2:8000")
    print("💡 For Real Device, use: http://YOUR_LOCAL_IP:8000")
    print("\n" + "=" * 70)
    print("\n⏹️  Press CTRL+C to stop the server\n")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def main():
    print_banner()
    check_dependencies()
    initialize_database()
    show_test_credentials()
    
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
