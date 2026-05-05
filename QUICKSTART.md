# 🚀 Quick Start Guide - Backend

## Option 1: Automatic Setup (Recommended)

Run the setup script:
```bash
python setup.py
```

Then start the server:
```bash
python start_server.py
```

That's it! ✅

---

## Option 2: Manual Setup

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

## 🔐 Test Login Credentials

| Email | Password |
|-------|----------|
| admin@insightflow.ai | admin123 |
| demo@insightflow.ai | demo123 |
| test@gmail.com | test123 |
| user@example.com | user123 |

---

## 📱 Connect Android App

### For Android Emulator:
Update in `RetrofitClient.kt`:
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/"
```

### For Real Device:
1. Find your computer's IP address:
   - **Windows**: Run `ipconfig` in Command Prompt
   - **Mac**: Run `ifconfig` in Terminal
   - **Linux**: Run `ip addr` or `ifconfig`

2. Update in `RetrofitClient.kt`:
```kotlin
private const val BASE_URL = "http://YOUR_IP:8000/"
```

Example: `http://192.168.1.100:8000/`

---

## ✅ Testing the Backend

### Test in Browser:
1. Open: http://localhost:8000
2. You should see: `{"status": "AI Customer Analyzer API is running"}`

### Test API Documentation:
Open: http://localhost:8000/docs

Try the `/auth/email` endpoint:
1. Click "POST /auth/email"
2. Click "Try it out"
3. Enter:
   ```json
   {
     "email": "admin@insightflow.ai",
     "password": "admin123"
   }
   ```
4. Click "Execute"
5. You should get a success response!

---

## 🔧 Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
Another app is using port 8000. Either:
- Stop that app
- Use a different port: `uvicorn app:app --port 8001`

### Error: "No test users"
```bash
python add_email_users.py
```

### Can't connect from Android
- Check firewall (allow port 8000)
- Ensure devices on same WiFi network
- Use correct IP address

---

## 📊 What's Working

✅ **Email/Password Authentication**
- Login endpoint: `/auth/email`
- Test users created
- Password hashing with SHA-256

✅ **Google OAuth Authentication**
- Login endpoint: `/auth/google`
- Token verification

✅ **ML Predictions**
- GET `/predict` - Quick demo
- POST `/predict` - Real predictions with ML model

✅ **Analytics**
- `/analytics/history` - Historical data
- `/analytics/summary` - Summary statistics

---

## 📝 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main backend (enhanced with email auth) |
| `add_email_users.py` | Creates test email users |
| `setup.py` | Automatic setup script |
| `start_server.py` | Quick server start |
| `analytics.db` | SQLite database (auto-created) |
| `model.pkl` | ML model |
| `.env` | Google OAuth config |

---

## 🎯 Next Steps

1. ✅ Start the backend server
2. ✅ Test email login at http://localhost:8000/docs
3. ✅ Update Android app's RetrofitClient.kt with backend URL
4. ✅ Run Android app and test login
5. ✅ Try both email and Google login methods

---

**You're ready to go! 🎉**
