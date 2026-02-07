# CheckBhai Deployment Checklist

## ✅ Pre-Deployment Checklist

- [x] Code complete and pushed to GitHub
- [x] All dependencies listed in requirements.txt and package.json
- [x] Environment variable templates created
- [x] Deployment configuration files ready
- [ ] Cloud accounts created (Supabase, Railway/Render, Vercel)
- [ ] Admin password changed from default

## 🚀 Deployment Steps

### Step 1: Supabase Database Setup (5 minutes)

1. **Create Account & Project**
   - [ ] Go to https://supabase.com and sign up
   - [ ] Create new project: "checkbhai"
   - [ ] Choose region: Southeast Asia (closest to Bangladesh)
   - [ ] Set strong database password and save it
   - [ ] Wait for project to initialize (~2 minutes)

2. **Get Database Connection String**
   - [ ] Go to Project Settings → Database
   - [ ] Copy "Connection string" (Connection pooling mode)
   - [ ] Replace `[YOUR-PASSWORD]` with your database password
   - [ ] Change `postgresql://` to `postgresql+asyncpg://` for async Python
   - [ ] Save this connection string for Railway deployment

### Step 2: Railway Backend Deployment (10 minutes)

1. **Create Railway Account**
   - [ ] Go to https://railway.app
   - [ ] Sign in with GitHub account

2. **Create New Project**
   - [ ] Click "New Project"
   - [ ] Select "Deploy from GitHub repo"
   - [ ] Choose: Tafhim512/Checkbhai
   - [ ] Select root directory: `checkbhai-backend`

3. **Configure Build Settings**
   - [ ] Railway will auto-detect Python
   - [ ] Build Command: `pip install -r requirements.txt`
   - [ ] Start Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   Click "Variables" tab and add:
   ```
   DATABASE_URL = [Your Supabase connection string with asyncpg]
   SECRET_KEY = [Generate with: openssl rand -hex 32]
   ADMIN_EMAIL = admin@checkbhai.com
   ADMIN_PASSWORD = [Your secure password - NOT admin123]
   PORT = 8000
   ALLOWED_ORIGINS = https://checkbhai.vercel.app
   ```

5. **Deploy**
   - [ ] Click "Deploy"
   - [ ] Wait for deployment to complete (~3-5 minutes)
   - [ ] Copy your Railway URL (e.g., checkbhai-production.up.railway.app)
   - [ ] Test health endpoint: https://YOUR-URL.railway.app/health
   - [ ] Check API docs: https://YOUR-URL.railway.app/docs

### Step 3: Vercel Frontend Deployment (5 minutes)

1. **Create Vercel Account**
   - [ ] Go to https://vercel.com
   - [ ] Sign in with GitHub

2. **Import Project**
   - [ ] Click "Add New..." → "Project"
   - [ ] Select repository: Tafhim512/Checkbhai
   - [ ] Framework: Next.js (auto-detected)
   - [ ] Root Directory: `checkbhai-frontend`

3. **Configure Environment Variable**
   Add:
   ```
   NEXT_PUBLIC_API_URL = https://YOUR-RAILWAY-URL.railway.app
   ```
   (Use the Railway URL from Step 2)

4. **Deploy**
   - [ ] Click "Deploy"
   - [ ] Wait for deployment (~2-3 minutes)
   - [ ] Copy your Vercel URL (e.g., checkbhai.vercel.app)

5. **Update Backend CORS** (Important!)
   - [ ] Go back to Railway
   - [ ] Update `ALLOWED_ORIGINS` variable to include your Vercel URL
   - [ ] Railway will auto-redeploy with new CORS settings

### Step 4: Verify Deployment (10 minutes)

1. **Test Backend API**
   - [ ] Visit: https://YOUR-BACKEND.railway.app/health
   - [ ] Expected: `{"status":"healthy","service":"CheckBhai API"}`
   - [ ] Visit: https://YOUR-BACKEND.railway.app/docs
   - [ ] Expected: Swagger UI interface

2. **Test Frontend**
   - [ ] Visit: https://YOUR-FRONTEND.vercel.app
   - [ ] Expected: Landing page with CheckBhai avatar
   - [ ] Check mobile responsiveness

3. **Test Scam Detection** (High Risk)
   - [ ] Input: "Work from home and earn $5000/month! Pay $200 registration fee!"
   - [ ] Click "Check for Scam"
   - [ ] Expected: High risk with red flags (urgency, payment request)

4. **Test Scam Detection** (Banglish)
   - [ ] Input: "Apni selected hoyechen! Dubai job paben. Taka pathao 15000"
   - [ ] Expected: High risk with multilingual detection

5. **Test Scam Detection** (Legitimate)
   - [ ] Input: "Job interview scheduled for Monday"
   - [ ] Expected: Low risk, no major flags

6. **Test Authentication**
   - [ ] Register new user: test@example.com / password123
   - [ ] Login successfully
   - [ ] Navigate to /history
   - [ ] Expected: Stats dashboard showing 0 checks initially

7. **Test Admin Dashboard**
   - [ ] Login with admin credentials
   - [ ] Navigate to /admin
   - [ ] Expected: Platform statistics visible
   - [ ] Test AI retraining: Add new example
   - [ ] Expected: Success notification

8. **Test Payment UI**
   - [ ] Navigate to /payment
   - [ ] Select package (10 checks)
   - [ ] Choose Bkash payment
   - [ ] Enter mobile: 01712345678
   - [ ] Submit payment
   - [ ] Expected: Payment simulation successful

### Step 5: Production Hardening

1. **Security**
   - [ ] Verify admin password is changed from admin123
   - [ ] Verify SECRET_KEY is strong random string
   - [ ] Enable HTTPS only (Vercel/Railway do this automatically)
   - [ ] Review CORS origins

2. **Database**
   - [ ] Check Supabase dashboard for created tables
   - [ ] Verify admin user exists in users table
   - [ ] Review database connection pooling settings

3. **Monitoring**
   - [ ] Set up Railway email alerts for errors
   - [ ] Monitor Vercel deployment logs
   - [ ] Check Supabase database metrics

## 📊 Expected Results

After deployment, you should have:

✅ **Live Frontend**: https://checkbhai.vercel.app
✅ **Live Backend**: https://checkbhai-production.railway.app
✅ **API Docs**: https://checkbhai-production.railway.app/docs
✅ **GitHub Repo**: https://github.com/Tafhim512/Checkbhai

## 🧪 Test Messages for QA

### English Scams:
1. "Send money urgently to secure your account" - Expected: High Risk
2. "Earn 50k in one day with this course" - Expected: High Risk
3. "100% guaranteed visa approval. Pay 50000 BDT now" - Expected: High Risk

### Banglish Scams:
1. "Dubai job, salary 80000 taka. Taka pathao 15000 visa processing" - Expected: High Risk
2. "Lottery jitechen 10 lakh taka! 5000 fee pathao" - Expected: High Risk

### Legitimate:
1. "Job interview scheduled for Monday" - Expected: Low Risk
2. "Thank you for your application. We'll review and contact you" - Expected: Low Risk

## 🚨 Common Issues & Solutions

**Issue**: Backend won't start
- Solution: Check DATABASE_URL is correct format with `asyncpg`
- Solution: Verify all environment variables are set

**Issue**: Frontend can't connect to backend
- Solution: Check NEXT_PUBLIC_API_URL is correct
- Solution: Verify ALLOWED_ORIGINS includes frontend URL

**Issue**: CORS errors
- Solution: Update ALLOWED_ORIGINS in Railway to include Vercel URL
- Solution: Wait for Railway auto-redeploy

**Issue**: Database tables not created
- Solution: Check Railway logs - tables auto-create on first startup
- Solution: Verify DATABASE_URL connection is successful

**Issue**: Admin login fails
- Solution: Check admin user was created (check logs on first startup)
- Solution: Verify password matches ADMIN_PASSWORD environment variable

## 📝 Post-Deployment

- [ ] Document live URLs
- [ ] Test all features end-to-end
- [ ] Take screenshots for documentation
- [ ] Share URLs with stakeholders
- [ ] Monitor for errors in first 24 hours
- [ ] Plan for payment gateway integration (Bkash, Rocket, Nagad)

## 🎉 Success Criteria

✅ Frontend loads and is mobile-responsive
✅ Backend API returns healthy status
✅ Can submit messages and get risk assessments
✅ Multi-language detection works (English, Bangla, Banglish)
✅ Authentication flow works
✅ Admin dashboard accessible
✅ Payment UI functional (simulation mode)
✅ No CORS errors
✅ All endpoints responding correctly

---

**Total Time**: ~30 minutes for complete deployment
**Cost**: $0 (all free tiers)
**Status**: Ready to deploy ✅
