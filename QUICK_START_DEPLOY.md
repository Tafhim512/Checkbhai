# CheckBhai - Quick Start Deploy Guide

## 🚀 Deploy in 15 Minutes

### Prerequisites
- GitHub account (you have this ✅)
- Email address for creating accounts

### Step 1: Create Accounts (5 min)
1. **Supabase**: https://supabase.com - Sign up with GitHub
2. **Railway**: https://railway.app - Sign up with GitHub  
3. **Vercel**: https://vercel.com - Sign up with GitHub

### Step 2: Deploy Database (3 min)
1. In Supabase, click "New Project"
2. Name: `checkbhai`
3. Database Password: `[CREATE STRONG PASSWORD]` - SAVE THIS!
4. Region: Southeast Asia
5. Click "Create Project" and wait ~2 min
6. Go to Settings → Database → Copy "Connection string"
7. Replace `[YOUR-PASSWORD]` with your password
8. Change `postgresql://` to `postgresql+asyncpg://`
9. SAVE this connection string!

### Step 3: Deploy Backend (4 min)
1. In Railway, click "New Project" → "Deploy from GitHub repo"
2. Select: `Tafhim512/Checkbhai`
3. Root Directory: `checkbhai-backend`
4. Click "Variables" and add:
   ```
   DATABASE_URL=[Your Supabase connection string]
   SECRET_KEY=[Run: openssl rand -hex 32]
   ADMIN_EMAIL=admin@checkbhai.com
   ADMIN_PASSWORD=[Your strong password, NOT admin123]
   PORT=8000
   ```
5. Click "Deploy"
6. Wait 3-4 minutes
7. Copy your Railway URL (e.g., `checkbhai-production.up.railway.app`)

### Step 4: Deploy Frontend (3 min)
1. In Vercel, click "Add New..." → "Project"
2. Select: `Tafhim512/Checkbhai`
3. Root Directory: `checkbhai-frontend`
4. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://[YOUR-RAILWAY-URL]
   ```
5. Click "Deploy"
6. Wait 2-3 minutes
7. Copy your Vercel URL (e.g., `checkbhai.vercel.app`)

### Step 5: Final Configuration (1 min)
1. Go back to Railway
2. Update `ALLOWED_ORIGINS` variable to:
   ```
   https://[YOUR-VERCEL-URL]
   ```
3. Railway will auto-redeploy

### Step 6: Test! ✅
1. Visit your Vercel URL
2. Enter test message: "Pay $200 to get this job!"
3. Click "Check for Scam"
4. You should see: **High Risk** with red flags!

## 🎉 You're Live!

**Your URLs**:
- Frontend: https://[YOUR-URL].vercel.app
- Backend: https://[YOUR-URL].railway.app
- API Docs: https://[YOUR-URL].railway.app/docs

**Admin Access**:
- Email: admin@checkbhai.com
- Password: [Whatever you set in ADMIN_PASSWORD]
- Dashboard: https://[YOUR-URL].vercel.app/admin

## 📱 Test Messages

Try these in your deployed app:

**English**: "Work from home and earn $5000/month! Pay $200 registration fee!"
**Banglish**: "Dubai job paben, salary 80000 taka. Taka pathao 15000"
**Bangla**: "লটারি জিতেছেন 10 লাখ টাকা! Processing fee 5000 টাকা পাঠাও"

All should show **High Risk** ✅

## 🐛 Troubleshooting

**Backend not starting?**
- Check DATABASE_URL has `asyncpg` in it
- Verify all environment variables are set

**Frontend can't connect?**
- Check NEXT_PUBLIC_API_URL is correct
- Verify ALLOWED_ORIGINS includes your Vercel URL

**CORS errors?**
- Update ALLOWED_ORIGINS in Railway
- Wait for auto-redeploy

## 💡 Next Steps

1. Change admin password from default
2. Test all features thoroughly
3. Add real payment gateway credentials (optional)
4. Share with users!

---

**Need help?** Check DEPLOYMENT_CHECKLIST.md for detailed instructions.
