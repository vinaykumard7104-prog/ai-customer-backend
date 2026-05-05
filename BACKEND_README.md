# 🐍 InsightFlow AI - Python Backend

## 🎯 What's Included

This is the **enhanced Python backend** with:
- ✅ Email/Password Authentication (NEW!)
- ✅ Google OAuth Authentication
- ✅ ML Predictions with RandomForest
- ✅ Analytics & Dashboard Endpoints
- ✅ Test Users Pre-configured

---

## 🚀 Super Quick Start (2 Commands!)

```bash
# 1. Auto setup (installs dependencies + creates test users)
python setup.py

# 2. Start server
python start_server.py
```

✅ Backend is now running on **http://localhost:8000**

Test it: Open **http://localhost:8000/docs**

---

## 🔐 Test Credentials (Ready to Use!)

After running `setup.py`, these users are created:

| Email | Password | Name |
|-------|----------|------|
| admin@insightflow.ai | admin123 | Admin User |
| demo@insightflow.ai | demo123 | Demo User |
| test@gmail.com | test123 | Test User |
| user@example.com | user123 | Example User |

---

## 📋 Manual Setup (If Preferred)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Test Users
```bash
python add_email_users.py
```

### Step 3: Start Server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 API Endpoints

### Authentication

#### Email/Password Login ⭐ NEW
```http
POST /auth/email
Content-Type: application/json

{
  "email": "admin@insightflow.ai",
  "password": "admin123"
}

Response:
{
  "status": "success",
  "user_id": 1,
  "email": "admin@insightflow.ai",
  "name": "Admin User",
  "picture": "",
  "is_new_user": false
}
```

#### Google OAuth Login
```http
POST /auth/google
Content-Type: application/json

{
  "id_token": "google_token_here"
}

Response:
{
  "status": "success",
  "user_id": 2,
  "email": "user@gmail.com",
  "name": "Google User",
  "picture": "https://...",
  "is_new_user": false
}
```

### Predictions

#### Quick Prediction (GET)
```http
GET /predict

Response:
{
  "engagement_probability": 0.78,
  "churn_risk": 0.23,
  "conversion_chance": 0.65
}
```

#### ML Prediction (POST)
```http
POST /predict
Content-Type: application/json

{
  "time_spent": 15.5,
  "clicks": 42,
  "pages": 8
}

Response:
{
  "engagement_probability": 0.82,
  "churn_risk": 0.18,
  "conversion_chance": 0.71,
  "model_used": "RandomForest"
}
```

### Analytics

#### History
```http
GET /analytics/history?limit=10

Response:
[
  {
    "id": 1,
    "engagement": 0.78,
    "churn": 0.22,
    "conversion": 0.65,
    "time_spent": 15.5,
    "clicks": 42,
    "pages": 8
  }
]
```

#### Summary
```http
GET /analytics/summary

Response:
{
  "avg_engagement": 0.756,
  "avg_churn": 0.234,
  "avg_conversion": 0.623,
  "total_records": 156
}
```

### Health Check
```http
GET /
GET /health
```

---

## ✨ What's New

### Enhanced Authentication
- ✅ Email/password login endpoint
- ✅ Password hashing with SHA-256
- ✅ Auth type tracking (Google vs Email)
- ✅ Test users script included

### Database Updates
- ✅ `password_hash` field added
- ✅ `auth_type` field added
- ✅ `google_id` now nullable
- ✅ Backward compatible!

### New Scripts
- ✅ `add_email_users.py` - Creates test users
- ✅ `setup.py` - One-command setup
- ✅ `start_server.py` - Easy server start

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main FastAPI application ⭐ Enhanced |
| `add_email_users.py` | Create test email users ⭐ NEW |
| `setup.py` | Automatic setup script ⭐ NEW |
| `start_server.py` | Quick server launcher ⭐ NEW |
| `analytics.db` | SQLite database (auto-created) |
| `model.pkl` | Trained ML model |
| `train_model.py` | Model training script |
| `.env` | Google OAuth configuration |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation ⭐ Updated |
| `QUICKSTART.md` | Quick start guide ⭐ NEW |

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    google_id VARCHAR UNIQUE,      -- Google user ID (nullable)
    email VARCHAR UNIQUE NOT NULL,  -- Email address
    name VARCHAR,                   -- User name
    picture VARCHAR,                -- Profile picture URL
    password_hash VARCHAR,          -- SHA-256 hash (for email login)
    auth_type VARCHAR DEFAULT 'google'  -- 'google' or 'email'
);
```

### Analytics Table
```sql
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY,
    engagement FLOAT,
    churn FLOAT,
    conversion FLOAT,
    time_spent FLOAT,
    clicks INTEGER,
    pages INTEGER
);
```

---

## 🔧 Configuration

### Environment Variables
**File**: `.env`

```env
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

Already configured with a test Client ID!

### Database
- **Type**: SQLite
- **File**: `analytics.db`
- **Auto-created**: Yes
- **Migration**: Automatic

### ML Model
- **File**: `model.pkl`
- **Algorithm**: RandomForest Classifier
- **Training**: `python train_model.py`
- **Fallback**: Rule-based if model not found

---

## 🧪 Testing the Backend

### Option 1: Web Browser
Open: **http://localhost:8000**

Should see:
```json
{
  "status": "AI Customer Analyzer API is running",
  "version": "2.0",
  "model_loaded": true
}
```

### Option 2: API Documentation
Open: **http://localhost:8000/docs**

Interactive Swagger UI with all endpoints!

### Option 3: Test Email Login
Using curl:
```bash
curl -X POST "http://localhost:8000/auth/email" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@insightflow.ai",
    "password": "admin123"
  }'
```

Should return success with user data!

### Option 4: Test with Android App
1. Update Android app's `RetrofitClient.kt`
2. Run Android app
3. Login with test credentials

---

## 📱 Android App Integration

### Backend URL Configuration

In Android app's `RetrofitClient.kt`:

**For Android Emulator:**
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/"
```

**For Real Device:**
1. Find your computer's IP address:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `ip addr`
2. Update:
```kotlin
private const val BASE_URL = "http://192.168.1.XXX:8000/"
```

### Network Requirements
- Same WiFi network (for real device)
- Firewall allows port 8000
- Server running before app connects

---

## 🔐 Security

### Password Security
- Passwords hashed with SHA-256
- Never stored in plain text
- Hash comparison for authentication

### Token Verification
- Google tokens verified with Google servers
- Invalid tokens rejected
- Proper error handling

### CORS Configuration
- Enabled for Android app
- Allows all origins (development)
- Restrict in production!

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Use different port
uvicorn app:app --port 8001

# Or find and kill process using port 8000
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

### "No test users exist"
```bash
python add_email_users.py
```

### "Invalid email or password"
1. Check email is exact: `admin@insightflow.ai`
2. Check password is exact: `admin123`
3. Run `add_email_users.py` again

### Google Login Not Working
1. Check `.env` has correct `GOOGLE_CLIENT_ID`
2. Verify using Web Client ID (not Android ID)
3. Check token being sent from Android app

### Database Locked
```bash
# Close all connections and restart
rm analytics.db
python add_email_users.py
python start_server.py
```

---

## 🚀 Deployment

### Development (Current)
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment
- Use PostgreSQL instead of SQLite
- Set environment variables properly
- Use HTTPS
- Implement JWT tokens
- Add rate limiting
- Enable CORS restrictions

---

## 📊 How It Works

### Email/Password Login Flow
1. Android sends email + password
2. Backend hashes password with SHA-256
3. Database lookup by email
4. Hash comparison
5. Return user profile if match

### Google OAuth Login Flow
1. Android gets Google ID token
2. Sends to backend `/auth/google`
3. Backend verifies with Google servers
4. Extracts user info
5. Creates/updates user in database
6. Returns user profile

### ML Prediction Flow
1. Android sends customer data
2. Backend loads RandomForest model
3. Model predicts churn probability
4. Calculates engagement & conversion
5. Saves to analytics database
6. Returns predictions

---

## 🎯 Adding More Users

### Method 1: Modify Script
Edit `add_email_users.py`:
```python
test_users = [
    {
        "email": "newuser@example.com",
        "password": "password123",
        "name": "New User"
    }
]
```

Run:
```bash
python add_email_users.py
```

### Method 2: Directly in Database
```python
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Your code here
```

---

## 📚 Additional Documentation

- **README.md** - Complete API documentation
- **QUICKSTART.md** - Step-by-step setup guide
- **app.py** - Inline code comments
- **Swagger UI** - http://localhost:8000/docs

---

## 🔗 Connect with Android App

This backend is fully compatible with **InsightFlow AI Android App**.

Download separately: **InsightFlow_Android_App.zip**

The Android app has:
- Dual login UI (Email + Google)
- All endpoints pre-configured
- Settings that work
- Beautiful design

---

## ✅ Pre-flight Checklist

Before connecting Android app:

- [ ] Backend running on port 8000
- [ ] Test users created
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:8000/docs
- [ ] Email login works in Swagger UI
- [ ] Firewall allows port 8000
- [ ] Know your computer's IP address

---

## 🎉 You're Ready!

Your backend is enhanced and ready for the Android app!

### Quick Commands
```bash
# Setup once
python setup.py

# Start server
python start_server.py

# Add more users
python add_email_users.py

# Test
open http://localhost:8000/docs
```

---

**Made with ❤️ using Python, FastAPI & SQLAlchemy**
