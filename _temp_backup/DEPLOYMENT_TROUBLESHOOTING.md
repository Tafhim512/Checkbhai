# 🚨 Railway Deployment Troubleshooting Guide

## Your Current Error: "Error deploying from source"

### Root Cause Analysis:

The error is likely caused by one or more of these issues:

1. **Wrong root directory** - Railway needs to build from `checkbhai-backend`
2. **Missing asyncpg in DATABASE_URL** - Python async requires special dialect
3. **Invalid SECRET_KEY** - You didn't actually generate one
4. **Missing environment variables** - Some required vars not set

---

## ✅ STEP-BY-STEP FIX

### Step 1: Verify Root Directory

In Railway:
1. Click on your service
2. Go to **Settings** tab
3. Find **Root Directory**
4. Make sure it says: `checkbhai-backend`
5. If not, click Edit and set it to `checkbhai-backend`

### Step 2: Generate SECRET_KEY

Run this command in your terminal (or I'll generate one):
```bash
openssl rand -hex 32
```

You'll get something like:
```
a3f5d8c2e1b4a7f9d2c5e8b1a4d7f0c3e6b9d2a5f8c1e4b7d0a3f6c9e2b5d8a1
```

**SAVE THIS!** You'll use it in the next step.

### Step 3: Set Environment Variables CORRECTLY

In Railway, go to **Variables** tab and set these EXACT values:

```
DATABASE_URL
postgresql+asyncpg://postgres:kaynat103286@db.finpvpvbagygdsqugxao.supabase.co:5432/postgres

SECRET_KEY
[PASTE THE OUTPUT FROM OPENSSL COMMAND HERE]

ADMIN_EMAIL
admin@checkbhai.com

ADMIN_PASSWORD
kaynat103286

PORT
8000

ALLOWED_ORIGINS
https://checkbhai.vercel.app
```

**⚠️ CRITICAL**: Notice `postgresql+asyncpg://` - the `+asyncpg` is REQUIRED!

### Step 4: Configure Build Settings

Still in Railway, verify these settings:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Python Version:**
- Should auto-detect Python 3.11+
- If not, add a `runtime.txt` file with: `python-3.11`

### Step 5: Redeploy

1. Click **Deploy** button in Railway
2. Watch the logs for errors
3. Deployment should take 3-5 minutes

---

## 🔍 Common Deployment Errors & Solutions

### Error: "ModuleNotFoundError: No module named 'asyncpg'"

**Solution**: 
- Check `requirements.txt` includes `asyncpg==0.29.0`
- If missing, I'll add it

### Error: "Could not connect to database"

**Solutions**:
1. Verify DATABASE_URL has `asyncpg` dialect
2. Check Supabase database is running
3. Verify password is correct: `kaynat103286`
4. Ensure port 5432 is specified

### Error: "No module named 'app'"

**Solution**:
- Root directory MUST be `checkbhai-backend`
- Start command should reference `app.main:app`

### Error: "SECRET_KEY is not set"

**Solution**:
- Generate with: `openssl rand -hex 32`
- Copy output to Railway environment variables

### Error: "Port already in use"

**Solution**:
- Make sure start command uses `$PORT` variable
- Don't hardcode port 8000

---

## 📋 Deployment Checklist

Before clicking Deploy, verify:

- [ ] Root Directory = `checkbhai-backend`
- [ ] DATABASE_URL contains `asyncpg`
- [ ] SECRET_KEY is a 64-character hex string
- [ ] All 6 environment variables are set
- [ ] Build command is correct
- [ ] Start command is correct

---

## 🧪 After Deployment - Test These

Once Railway shows "Active":

1. **Health Check**:
   ```
   https://your-app.railway.app/health
   ```
   Should return: `{"status":"healthy","service":"CheckBhai API"}`

2. **API Documentation**:
   ```
   https://your-app.railway.app/docs
   ```
   Should show Swagger UI

3. **Check Logs**:
   - Look for: "Application startup complete"
   - Look for: "Admin user created" or "Admin user already exists"
   - Should NOT see: Connection errors, module errors

---

## 🆘 If Still Failing

### Get Detailed Error Logs:

1. In Railway, click **Deployments** tab
2. Click on the failed deployment
3. Click **View Logs**
4. Look for red ERROR lines
5. **Share the exact error message with me**

### Common Log Errors:

**"Failed to install requirements"**
- Check requirements.txt exists in checkbhai-backend
- Verify file has correct packages

**"Application startup failed"**
- Database connection issue
- Check DATABASE_URL format

**"Module not found"**
- Wrong root directory
- Check it's set to `checkbhai-backend`

---

## 🎯 Quick Fix Checklist

Try these in order:

1. ✅ Set Root Directory to `checkbhai-backend`
2. ✅ Update DATABASE_URL to use `asyncpg`
3. ✅ Generate and set SECRET_KEY properly
4. ✅ Click "Deploy" again
5. ✅ Watch logs for specific errors
6. ✅ Share error message if still failing

---

## 💡 Alternative: Use Render Instead

If Railway continues to fail, try Render:

1. Go to https://render.com
2. Sign in with GitHub
3. Create **Web Service**
4. Connect: Tafhim512/Checkbhai
5. Root Directory: `checkbhai-backend`
6. Runtime: Python 3
7. Build: `pip install -r requirements.txt`
8. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
9. Add same environment variables

Render has similar setup but sometimes works better for Python apps.

---

**Next: After backend is deployed, I'll help you deploy the frontend to Vercel!**
