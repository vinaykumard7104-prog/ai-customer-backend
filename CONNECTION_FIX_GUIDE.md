# 🔧 BACKEND CONNECTION FIX GUIDE

## 🚨 Problem: "Server Unreachable" or "Backend Not Connected"

This guide will fix your connection issues step by step.

---

## ✅ SOLUTION 1: Quick Fix for Emulator (EASIEST)

### Step 1: Start Backend Properly

```bash
cd ai-backend

# Make sure you're running on 0.0.0.0 (not localhost)
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Important:** Use `0.0.0.0` NOT `127.0.0.1` or `localhost`

### Step 2: Test Backend is Running

Open browser and go to: **http://localhost:8000**

You should see:
```json
{
  "status": "AI Customer Analyzer API is running"
}
```

✅ If you see this, backend is working!

### Step 3: Update Android App for Emulator

**File:** `app/src/main/java/com/example/aicustomeranalyzer/RetrofitClient.kt`

Change to:
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/"
```

**DO NOT USE:**
- ❌ `http://localhost:8000/`
- ❌ `http://127.0.0.1:8000/`
- ❌ `http://192.168.x.x:8000/` (for emulator)

### Step 4: Enable Cleartext Traffic

**File:** `app/src/main/AndroidManifest.xml`

Add this inside `<application>` tag:
```xml
<application
    android:usesCleartextTraffic="true"
    ...>
```

Full example:
```xml
<application
    android:allowBackup="true"
    android:usesCleartextTraffic="true"
    android:icon="@mipmap/ic_launcher"
    android:label="@string/app_name"
    ...>
```

### Step 5: Rebuild and Run

1. In Android Studio: **Build** → **Clean Project**
2. **Build** → **Rebuild Project**
3. Run the app again

✅ Should work now!

---

## ✅ SOLUTION 2: Fix for Real Android Phone

### Step 1: Find Your Computer's IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" like: `192.168.1.100`

**Mac/Linux:**
```bash
ifconfig
# or
ip addr
```
Look for inet like: `192.168.1.100`

### Step 2: Start Backend on 0.0.0.0

```bash
cd ai-backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3: Test From Phone's Browser

On your phone, open browser and go to:
```
http://YOUR_COMPUTER_IP:8000
```

Example: `http://192.168.1.100:8000`

You should see the API response!

If NOT working:
- Check firewall (see Step 5 below)
- Make sure phone and computer on same WiFi

### Step 4: Update Android App

**File:** `app/src/main/java/com/example/aicustomeranalyzer/RetrofitClient.kt`

```kotlin
private const val BASE_URL = "http://192.168.1.100:8000/"
```
(Replace with YOUR IP address)

### Step 5: Allow Firewall (IMPORTANT!)

**Windows Firewall:**
1. Open "Windows Defender Firewall"
2. Click "Allow an app through firewall"
3. Click "Change settings"
4. Click "Allow another app"
5. Add Python or allow port 8000

Or run this command as Administrator:
```cmd
netsh advfirewall firewall add rule name="Python Port 8000" dir=in action=allow protocol=TCP localport=8000
```

**Mac Firewall:**
System Preferences → Security & Privacy → Firewall → Firewall Options → Add Python

**Linux:**
```bash
sudo ufw allow 8000
```

### Step 6: Enable Cleartext Traffic

Same as Solution 1 Step 4:

**File:** `app/src/main/AndroidManifest.xml`
```xml
<application
    android:usesCleartextTraffic="true"
    ...>
```

### Step 7: Rebuild and Test

1. Clean Project
2. Rebuild Project  
3. Run on phone
4. Try login!

---

## ✅ SOLUTION 3: Network Security Config (If Still Failing)

If cleartext traffic doesn't work, use network security config:

### Step 1: Create Network Security Config

**File:** `app/src/main/res/xml/network_security_config.xml`

Create this file with:
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">192.168.1.1</domain>
        <domain includeSubdomains="true">192.168.1.2</domain>
        <domain includeSubdomains="true">192.168.1.100</domain>
    </domain-config>
</network-security-config>
```

### Step 2: Reference in Manifest

**File:** `app/src/main/AndroidManifest.xml`
```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    android:usesCleartextTraffic="true"
    ...>
```

---

## 🧪 TESTING CHECKLIST

Run through this checklist:

### Backend Tests:
- [ ] Backend running on 0.0.0.0:8000
- [ ] Can access http://localhost:8000 in browser
- [ ] See JSON response with "status"
- [ ] Can access http://localhost:8000/docs
- [ ] Swagger UI loads

### Emulator Tests:
- [ ] RetrofitClient.kt has `http://10.0.2.2:8000/`
- [ ] Cleartext traffic enabled in manifest
- [ ] App rebuilt after changes
- [ ] Backend shows connection in logs when app starts

### Real Phone Tests:
- [ ] Phone and computer on same WiFi
- [ ] Can access backend from phone browser
- [ ] RetrofitClient.kt has correct IP
- [ ] Firewall allows port 8000
- [ ] Cleartext traffic enabled

---

## 🔍 DEBUG MODE - Check Logs

### Backend Logs:
When you start backend, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

When Android app connects, you'll see:
```
INFO:     10.0.2.2:xxxxx - "POST /auth/email HTTP/1.1" 200 OK
```

### Android Logs (Logcat):
In Android Studio → Logcat, filter for "Retrofit" or "OkHttp"

Look for:
```
D/OkHttp: --> POST http://10.0.2.2:8000/auth/email
```

If you see connection errors, that's the issue!

---

## 📝 COMMON ERRORS & FIXES

### Error: "Failed to connect to /10.0.2.2:8000"
**Fix:** Backend not running. Start backend first!

### Error: "Unable to resolve host"
**Fix:** Wrong URL in RetrofitClient.kt or no internet

### Error: "Cleartext HTTP traffic not permitted"
**Fix:** Add `android:usesCleartextTraffic="true"` to manifest

### Error: "Connection refused"
**Fix:** Backend running on localhost instead of 0.0.0.0

### Error: "Timeout"
**Fix:** Firewall blocking. Check firewall settings.

### Error: "SSL handshake failed"
**Fix:** You're using https instead of http. Use http for development.

---

## 🎯 RECOMMENDED SETUP

### For Development (Testing):

**Emulator:**
```kotlin
// RetrofitClient.kt
private const val BASE_URL = "http://10.0.2.2:8000/"
```

**Real Phone:**
```kotlin
// RetrofitClient.kt  
private const val BASE_URL = "http://192.168.1.XXX:8000/"
```

**Backend:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Manifest:**
```xml
<application android:usesCleartextTraffic="true" ...>
```

---

## ⚡ QUICK DEBUG STEPS

1. **Test backend in browser:**
   ```
   http://localhost:8000
   ```
   Should see JSON response

2. **Test from phone browser (if using real phone):**
   ```
   http://YOUR_IP:8000
   ```
   Should see same JSON response

3. **Check Android code has correct URL**

4. **Rebuild Android app** (Clean → Rebuild)

5. **Check Logcat** for connection errors

---

## 🚀 STILL NOT WORKING?

### Option 1: Use ngrok (Easiest for Real Phone)

1. Install ngrok: https://ngrok.com/
2. Start backend normally
3. Run ngrok:
   ```bash
   ngrok http 8000
   ```
4. Copy the https URL (like: https://abc123.ngrok.io)
5. Update RetrofitClient.kt:
   ```kotlin
   private const val BASE_URL = "https://abc123.ngrok.io/"
   ```
6. Works on any phone anywhere!

### Option 2: Use USB Debugging with ADB Reverse

1. Connect phone via USB
2. Enable USB debugging
3. Run:
   ```bash
   adb reverse tcp:8000 tcp:8000
   ```
4. Use in app:
   ```kotlin
   private const val BASE_URL = "http://localhost:8000/"
   ```

---

## ✅ FINAL VERIFICATION

When working correctly, you should see:

### In Backend Terminal:
```
INFO:     10.0.2.2:50123 - "POST /auth/email HTTP/1.1" 200 OK
```

### In Android App:
- Login screen loads
- Click "Sign in with Email"
- Enter credentials
- Loading spinner shows
- ✅ Successfully logged in!

---

## 📞 Need More Help?

If still not working, check:
1. Backend terminal - any errors?
2. Android Logcat - connection errors?
3. Firewall settings
4. Same WiFi network (for real phone)
5. Correct IP address

**Most common issue:** Backend running on localhost instead of 0.0.0.0
**Fix:** `uvicorn app:app --host 0.0.0.0 --port 8000`

---

**This guide covers 99% of connection issues. Follow it step by step!** 🚀
