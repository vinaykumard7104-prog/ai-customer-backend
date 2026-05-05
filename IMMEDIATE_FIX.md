# 🚨 IMMEDIATE FIX - Server Unreachable Error

## ⚡ Quick 3-Step Fix (Works 95% of the Time!)

### STEP 1: Start Backend Correctly ✅

Open terminal/command prompt in `ai-backend` folder:

```bash
python start_server.py
```

**IMPORTANT:** You should see:
```
Starting server on http://0.0.0.0:8000
```

**NOT `127.0.0.1` or `localhost` - Must be `0.0.0.0`!**

If you don't see `0.0.0.0`, the backend won't work!

---

### STEP 2: Test Backend is Running ✅

Open your web browser and go to:
```
http://localhost:8000
```

You should see:
```json
{
  "status": "AI Customer Analyzer API is running",
  "version": "2.0",
  "model_loaded": true
}
```

✅ **If you see this = Backend is working!**

❌ **If page doesn't load = Backend not started correctly**

---

### STEP 3: Check Android App URL ✅

**File:** `app/src/main/java/com/example/aicustomeranalyzer/RetrofitClient.kt`

**For Emulator (default):**
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/"
```

**For Real Phone:**
1. Look at backend terminal - it shows your IP like `192.168.1.100`
2. Change to:
```kotlin
private const val BASE_URL = "http://192.168.1.100:8000/"
```

**Then in Android Studio:**
1. Build → Clean Project
2. Build → Rebuild Project
3. Run app again

---

## 🎯 That's It!

90% of the time, these 3 steps fix the issue!

---

## 🔍 Still Not Working? Quick Checks:

### Check #1: Backend Really Running?
```bash
# Should show Python process
# Windows:
tasklist | findstr python

# Mac/Linux:
ps aux | grep python
```

### Check #2: Port 8000 Free?
Another app might be using port 8000.

**Fix:** Use different port:
```bash
# Backend
python -m uvicorn app:app --host 0.0.0.0 --port 8001

# Android (RetrofitClient.kt)
private const val BASE_URL = "http://10.0.2.2:8001/"
```

### Check #3: Firewall Blocking?

**Windows:** Run as Administrator:
```cmd
netsh advfirewall firewall add rule name="Python8000" dir=in action=allow protocol=TCP localport=8000
```

**Mac:**
System Preferences → Security & Privacy → Firewall → Allow Python

**Linux:**
```bash
sudo ufw allow 8000
```

### Check #4: Phone on Same WiFi?
If using real phone, both phone and computer MUST be on same WiFi network!

### Check #5: Cleartext Traffic Enabled?
Already done in the latest version, but double-check:

**File:** `app/src/main/AndroidManifest.xml`
```xml
<application
    android:usesCleartextTraffic="true"
    ...>
```

---

## 📱 Test From Phone Browser

**For Emulator:**
1. Open Chrome in emulator
2. Go to: `http://10.0.2.2:8000`
3. Should see JSON response

**For Real Phone:**
1. Open browser on phone
2. Go to: `http://YOUR_IP:8000` (e.g., `http://192.168.1.100:8000`)
3. Should see JSON response

If this works but app doesn't = Android code issue
If this doesn't work = Backend/network issue

---

## 🐛 Debug: Check Logs

### Backend Logs:
When app tries to login, you should see:
```
INFO: 10.0.2.2:xxxxx - "POST /auth/email HTTP/1.1" 200 OK
```

If you don't see this = App not reaching backend

### Android Logs:
In Android Studio → Logcat, search for "Retrofit"

Should see:
```
D/OkHttp: --> POST http://10.0.2.2:8000/auth/email
```

If you see error here, that's the problem!

---

## 🎯 Most Common Issues:

| Issue | Fix |
|-------|-----|
| Backend not started | Run `python start_server.py` |
| Wrong IP in app | Update RetrofitClient.kt |
| Firewall blocking | Allow port 8000 |
| Wrong WiFi | Connect to same network |
| Port already used | Use different port |

---

## ✅ Working Setup Looks Like:

### Backend Terminal:
```
✅ Starting server on http://0.0.0.0:8000
✅ Uvicorn running on http://0.0.0.0:8000
✅ Application startup complete
```

### Browser Test:
```
✅ http://localhost:8000 shows JSON
```

### Android Logcat:
```
✅ POST http://10.0.2.2:8000/auth/email
✅ Response code: 200
```

### App:
```
✅ Login screen loads
✅ Enter credentials
✅ Successfully logged in!
```

---

## 🆘 Emergency Fix: Use ngrok

If NOTHING works, use ngrok (works anywhere!):

1. Download ngrok: https://ngrok.com/download
2. Start your backend normally
3. Run:
   ```bash
   ngrok http 8000
   ```
4. Copy the URL (like: `https://abc123.ngrok.io`)
5. Update Android:
   ```kotlin
   private const val BASE_URL = "https://abc123.ngrok.io/"
   ```
6. Works on any phone, anywhere!

---

## 📞 Last Resort Checklist:

- [ ] Backend shows `0.0.0.0:8000` when starting
- [ ] Can access `http://localhost:8000` in browser
- [ ] RetrofitClient.kt has `http://10.0.2.2:8000/` (emulator) or correct IP (phone)
- [ ] Manifest has `android:usesCleartextTraffic="true"`
- [ ] Rebuilt Android app after changes
- [ ] Firewall allows port 8000
- [ ] Phone and computer on same WiFi (if real phone)

---

**If you followed all steps above, it WILL work! 🚀**

Need more help? Check CONNECTION_FIX_GUIDE.md for advanced troubleshooting.
