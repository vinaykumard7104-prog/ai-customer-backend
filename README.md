# AI Customer Analyzer - Backend (Enhanced)

## ✨ NEW: Email/Password Authentication Added!

This backend now supports **both** Google OAuth and Email/Password authentication.

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Google OAuth (Optional - for Google Sign-In)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → APIs & Services → Credentials
3. Create **OAuth 2.0 Client ID** → Android (for your app)
4. Also create a **Web Application** client ID (for backend verification)
5. Copy the Web Client ID
6. Create/update `.env` file:
```
GOOGLE_CLIENT_ID=your-web-client-id.apps.googleusercontent.com
```

**Note:** `.env` already exists with a Client ID. You can use it for testing or replace it with yours.

### 3. Add Test Users for Email/Password Login
```bash
python add_email_users.py
```

This creates test accounts:
- `admin@insightflow.ai` / `admin123`
- `demo@insightflow.ai` / `demo123`
- `test@gmail.com` / `test123`
- `user@example.com` / `user123`

### 4. Train the ML model (Optional)
```bash
python train_model.py
```

### 5. Run the server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API
Open: http://localhost:8000/docs

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health |
| POST | `/auth/google` | Google login (send `id_token`) |
| POST | `/auth/email` | **NEW** Email/password login |
| GET | `/user/{user_id}` | Get user profile |
| GET | `/predict` | Quick random prediction |
| POST | `/predict` | ML prediction with input data |
| GET | `/analytics` | Store + return analytics |
| GET | `/analytics/history` | Last N records |
| GET | `/analytics/summary` | Averages & totals |

---

## Authentication Methods

### 1. Google OAuth Login

In your Android app, after Google Sign-In succeeds:

```kotlin
// Get the ID token from Google Sign-In result
val idToken = account.idToken

// Send to your backend
POST http://YOUR_SERVER_IP:8000/auth/google
Body: { "id_token": "..." }

// Response contains user_id, email, name, picture
```

### 2. Email/Password Login ✨ NEW

```kotlin
// Send email and password
POST http://YOUR_SERVER_IP:8000/auth/email
Body: {
  "email": "admin@insightflow.ai",
  "password": "admin123"
}

// Response:
{
  "status": "success",
  "user_id": 1,
  "email": "admin@insightflow.ai",
  "name": "Admin User",
  "picture": "",
  "is_new_user": false
}
```

---

## Test Credentials

After running `add_email_users.py`:

| Email | Password | Name |
|-------|----------|------|
| admin@insightflow.ai | admin123 | Admin User |
| demo@insightflow.ai | demo123 | Demo User |
| test@gmail.com | test123 | Test User |
| user@example.com | user123 | Example User |

---

## Database

SQLite database (`analytics.db`) is created automatically.

**Tables:**
- `users` — stores both Google and Email/Password users
  - `id` — User ID
  - `google_id` — Google user ID (nullable)
  - `email` — Email address (unique)
  - `name` — User name
  - `picture` — Profile picture URL
  - `password_hash` — SHA-256 hashed password (for email login)
  - `auth_type` — "google" or "email"
  
- `analytics` — stores prediction results
  - `id` — Record ID
  - `engagement` — Engagement score
  - `churn` — Churn risk
  - `conversion` — Conversion probability
  - `time_spent` — Time spent (optional)
  - `clicks` — Number of clicks (optional)
  - `pages` — Pages viewed (optional)

---

## Security Notes

- Passwords are hashed with SHA-256 before storage
- Google OAuth tokens are verified with Google's servers
- CORS is enabled for Android app connectivity
- Never commit `.env` file with real credentials to version control

---

## Android App Integration

The backend is fully compatible with the **InsightFlow AI** Android app.

Make sure to update the backend URL in your Android app:
- **Emulator**: `http://10.0.2.2:8000/`
- **Real Device**: `http://YOUR_COMPUTER_IP:8000/`

---

## Troubleshooting

### Issue: "Invalid email or password"
- Run `add_email_users.py` to create test users
- Use exact credentials as shown above
- Passwords are case-sensitive

### Issue: Google login fails
- Check `.env` file has correct `GOOGLE_CLIENT_ID`
- Ensure Web Client ID (not Android Client ID) is used
- Verify token is being sent correctly from Android app

### Issue: Can't connect from Android
- Check firewall allows port 8000
- Use correct IP address (10.0.2.2 for emulator)
- Ensure both devices on same network (for real device)

---

## Files

- `app.py` — Main FastAPI application ✨ Enhanced with email auth
- `add_email_users.py` — ✨ NEW: Script to add test email users
- `analytics.db` — SQLite database (auto-created)
- `model.pkl` — Trained ML model
- `train_model.py` — Model training script
- `.env` — Environment variables (Google Client ID)
- `requirements.txt` — Python dependencies
