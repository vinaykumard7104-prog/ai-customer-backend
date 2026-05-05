#!/usr/bin/env python3
"""
InsightFlow AI Backend - One-Command Setup
Run this script to set up everything automatically
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Success!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Error:")
        print(result.stderr)
        return False
    
    return True

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          InsightFlow AI - Backend Setup                 ║
║          Email/Password + Google OAuth                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n⚠️  Dependency installation failed. Please install manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Step 2: Add email users
    if not run_command(
        f"{sys.executable} add_email_users.py",
        "Creating test email/password users"
    ):
        print("\n⚠️  User creation failed (may already exist)")
    
    # Step 3: Check if model exists
    if not os.path.exists("model.pkl"):
        print(f"\n{'='*60}")
        print("📊 ML Model not found. Training new model...")
        print(f"{'='*60}")
        
        if not run_command(
            f"{sys.executable} train_model.py",
            "Training ML model"
        ):
            print("\n⚠️  Model training failed. Server will use rule-based fallback.")
    else:
        print(f"\n{'='*60}")
        print("✅ ML model already exists (model.pkl)")
        print(f"{'='*60}")
    
    # Final instructions
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                 ✅ Setup Complete!                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🚀 To start the server, run:

   uvicorn app:app --reload --host 0.0.0.0 --port 8000

   Or simply:

   python start_server.py

📱 Connect your Android app to:
   • Emulator: http://10.0.2.2:8000/
   • Real Device: http://YOUR_IP:8000/

🔐 Test Email Login Credentials:
   ┌─────────────────────────┬─────────────┬──────────────┐
   │ Email                   │ Password    │ Name         │
   ├─────────────────────────┼─────────────┼──────────────┤
   │ admin@insightflow.ai    │ admin123    │ Admin User   │
   │ demo@insightflow.ai     │ demo123     │ Demo User    │
   │ test@gmail.com          │ test123     │ Test User    │
   │ user@example.com        │ user123     │ Example User │
   └─────────────────────────┴─────────────┴──────────────┘

📚 API Documentation: http://localhost:8000/docs

════════════════════════════════════════════════════════════
    """)

if __name__ == "__main__":
    main()
