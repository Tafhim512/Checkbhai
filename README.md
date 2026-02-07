# 🛡️ CHECKBHAI - Bangladesh's Anti-Scam & Fraud Verification Layer

**Community-Powered Trust Intelligence Platform**

> The place people check before sending money.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CHECKBHAI PLATFORM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    HTTPS/REST    ┌──────────────────────┐    │
│  │   FRONTEND   │ ◄──────────────► │      BACKEND         │    │
│  │  (Next.js)   │                  │     (FastAPI)        │    │
│  │  Vercel      │                  │     Render           │    │
│  └──────────────┘                  └──────────┬───────────┘    │
│                                               │                 │
│                                    ┌──────────▼───────────┐    │
│                                    │    AI ENGINE          │    │
│                                    │  ┌─────────────────┐ │    │
│                                    │  │ Rules Engine     │ │    │
│                                    │  │ (Deterministic)  │ │    │
│                                    │  └─────────────────┘ │    │
│                                    │  ┌─────────────────┐ │    │
│                                    │  │ LangChain + LLM  │ │    │
│                                    │  │ (Explanation)    │ │    │
│                                    │  └─────────────────┘ │    │
│                                    │  ┌─────────────────┐ │    │
│                                    │  │ ML Classifier    │ │    │
│                                    │  │ (TF-IDF + NB)   │ │    │
│                                    │  └─────────────────┘ │    │
│                                    └──────────┬───────────┘    │
│                                               │                 │
│                                    ┌──────────▼───────────┐    │
│                                    │   PostgreSQL DB       │    │
│                                    │   (Supabase/Render)   │    │
│                                    └──────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Schema

### Core Tables

| Table | Purpose |
|-------|---------|
| `users` | User accounts with reputation scores |
| `entities` | Tracked entities (phones, FB pages, shops, agents, payment numbers) |
| `messages` | Message check history with risk analysis |
| `reports` | Community scam reports (append-only) |
| `evidence` | Supporting evidence for reports |
| `entity_claims` | Business profile claim requests |
| `votes` | Community verification votes |
| `payments` | Premium payment records |
| `activity_logs` | Audit trail for all actions |
| `training_data` | Verified AI training data |

### Entity Types
- `phone` - Phone numbers
- `fb_page` - Facebook Pages
- `fb_profile` - Facebook Profiles
- `whatsapp` - WhatsApp numbers
- `shop` - Online shop URLs
- `agent` - Agents (visa, job, travel)
- `bkash` - bKash payment numbers
- `nagad` - Nagad payment numbers
- `rocket` - Rocket payment numbers

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user info |

### Entity Check System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/entities/check?type=phone&identifier=01XXXXXXXXX` | Check entity risk |
| GET | `/entities/{id}` | Get entity details |
| GET | `/entities/{id}/reports` | Get entity's reports |

### Message Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/check/message` | Analyze message for scam patterns |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reports/` | Submit scam report |
| GET | `/reports/` | List all reports |
| GET | `/reports/{id}` | Get report details |

### Business Claims
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/claims/` | Submit business claim |
| GET | `/claims/{id}` | Check claim status |

### History
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/history/` | Get user's check history |
| GET | `/history/stats` | Get user statistics |

### Payment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payment/` | Create payment |
| GET | `/payment/history` | Get payment history |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/stats` | Platform statistics |
| GET | `/admin/reports` | All reports with filters |
| PUT | `/admin/reports/{id}/verify` | Verify a report |
| DELETE | `/admin/reports/{id}` | Mark report as spam |

---

## 🤖 AI Logic Flow

```
User Input (Message/Entity)
        │
        ▼
┌───────────────────┐
│  RULES ENGINE     │ ◄── Source of Truth for Risk Level
│  (Deterministic)  │
│                   │
│  Checks:          │
│  • Urgency words  │
│  • Payment reqs   │
│  • Overpromises   │
│  • PIN/OTP phish  │
│  • Job/visa fees  │
│  • Price anomaly  │
│  • Lottery scams  │
│                   │
│  Output:          │
│  • Red flags []   │
│  • Risk score     │
│  • Risk level     │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  LangChain LLM    │ ◄── Explanation Only (Not Risk Source)
│  (GPT-4o-mini)    │
│                   │
│  Provides:        │
│  • English reason │
│  • Bangla reason  │
│  • Semantic flags │
│  • Category       │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  ML CLASSIFIER    │ ◄── Pattern Matching Backup
│  (TF-IDF + NB)    │
│                   │
│  Trained on:      │
│  • 50+ examples   │
│  • EN/BN/Banglish │
│  • 8 categories   │
└───────────────────┘
```

---

## 💰 Monetization Logic

| Tier | Price | Features |
|------|-------|----------|
| Free | ৳0 | 3 checks/day, basic risk info |
| Premium Monthly | ৳300/mo | Unlimited checks, full reports, AI reasoning |
| One-time Deep Check | ৳50 | Single detailed verification |
| Business API | ৳2000/mo | API access, bulk checks, network graphs |
| Verified Badge | ৳5000 one-time | Verified seller badge on profile |

---

## 🛡️ Risk & Abuse Prevention

1. **Rate Limiting**: 3 free checks/day per fingerprint
2. **False Report Protection**: Disclaimer + reputation system
3. **Appeal System**: Business claim process for wrongly flagged entities
4. **Moderation Queue**: Admin panel for report verification
5. **Append-Only Reports**: Reports cannot be deleted, only marked as spam
6. **Reputation Scoring**: Higher rep users have more vote weight
7. **Evidence Validation**: AI validates screenshot authenticity (planned)

---

## 🚀 Deployment

### Backend (Render)
- **URL**: https://checkbhai.onrender.com
- **Branch**: `main`
- **Root Directory**: `checkbhai-backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
- **URL**: https://checkbhai.vercel.app
- **Branch**: `main`
- **Root Directory**: `checkbhai-frontend`
- **Framework**: Next.js
- **Environment Variable**: `NEXT_PUBLIC_API_URL=https://checkbhai.onrender.com`

### Required Environment Variables (Backend)
```
DATABASE_URL=postgresql+asyncpg://...
SECRET_KEY=your-secret-key
ADMIN_EMAIL=admin@checkbhai.com
ADMIN_PASSWORD=your-admin-password
OPENAI_API_KEY=sk-... (optional)
LANGCHAIN_API_KEY=ls__... (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=checkbhai-backend
```

---

## 🗺️ Future Expansion Roadmap

### Phase 1 (Current - MVP)
- ✅ Entity check system
- ✅ AI scam analysis (Rules + LLM)
- ✅ Evidence-based reporting
- ✅ Community verification
- ✅ Admin moderation panel
- ✅ Business claim system

### Phase 2 (Next 30 days)
- [ ] Payment gateway integration (bKash, Nagad)
- [ ] Evidence upload (screenshots)
- [ ] Network detection visualization
- [ ] Mobile app (React Native)
- [ ] SMS-based checking

### Phase 3 (60-90 days)
- [ ] Browser extension
- [ ] WhatsApp bot integration
- [ ] Verified seller badges
- [ ] API marketplace
- [ ] Regional expansion (India, Pakistan)

### Phase 4 (6 months)
- [ ] Government partnership
- [ ] Bank integration
- [ ] Real-time scam alerts
- [ ] Machine learning model v2
- [ ] Multi-language support

---

## 📝 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TailwindCSS |
| Backend | FastAPI, Python 3.11 |
| Database | PostgreSQL (async via asyncpg) |
| AI/ML | LangChain, OpenAI GPT-4o-mini, scikit-learn |
| Auth | JWT (python-jose), bcrypt |
| Hosting | Vercel (frontend), Render (backend) |
| Monitoring | LangSmith (AI tracing) |

---

## 🏃 Quick Start (Local Development)

### Backend
```bash
cd checkbhai-backend
pip install -r requirements.txt
# Set DATABASE_URL in .env or use SQLite fallback
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd checkbhai-frontend
npm install
npm run dev
```

---

**© 2026 CHECKBHAI - Community-Powered Trust Infrastructure for Bangladesh**
