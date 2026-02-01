# CheckBhai: AI-Powered Scam Detection Platform for Bangladesh 🇧🇩

![CheckBhai Logo](https://img.shields.io/badge/CheckBhai-AI%20Scam%20Detection-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)

CheckBhai is an AI-powered scam detection platform designed specifically for Bangladesh. It helps users identify scams in messages written in **English, Bangla, or Banglish** across various categories including job offers, investment opportunities, sales pitches, and more.

## 🚀 Features

- **AI-Powered Detection**: Machine learning model trained on 50+ examples
- **Multi-language Support**: Works with English, Bangla (Unicode), and Banglish (Romanized)
- **Rules Engine**: Pattern-based detection for obvious scam indicators
- **Risk Assessment**: Classifies messages as Low, Medium, or High risk
- **Red Flags Detection**: Identifies urgency tactics, payment requests, overpromises
- **Human-in-Loop**: Admin can retrain the AI model with new examples
- **Payment Integration**: Supports Bkash, Rocket, and Bank payments
- **User History**: Track previously checked messages
- **Mobile-First Design**: Responsive UI optimized for mobile devices

## 📦 Project Structure

```
checkbhai/
├── checkbhai-backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── database.py        # Database models & config
│   │   ├── auth.py            # JWT authentication
│   │   ├── models.py          # Pydantic schemas
│   │   ├── ai_engine.py       # AI text classifier
│   │   ├── rules_engine.py    # Pattern-based detection
│   │   ├── training_data.py   # Training dataset (50+ examples)
│   │   └── routers/           # API endpoints
│   │       ├── auth.py        # Register/Login
│   │       ├── check.py       # Scam detection
│   │       ├── history.py     # User history
│   │       ├── payment.py     # Payment processing
│   │       └── admin.py       # Admin dashboard
│   ├── requirements.txt
│   └── Dockerfile
│
└── checkbhai-frontend/        # Next.js frontend
    ├── app/
    │   ├── page.tsx          # Landing page
    │   ├── history/          # History page
    │   ├── payment/          # Payment page
    │   └── admin/            # Admin dashboard
    ├── components/
    │   ├── CheckBhaiAvatar.tsx
    │   ├── RiskBadge.tsx
    │   └── RedFlagsList.tsx
    ├── lib/
    │   └── api.ts            # API client
    └── package.json
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with async SQLAlchemy
- **AI/ML**: scikit-learn (TF-IDF + Multinomial NB)
- **Auth**: JWT with bcrypt password hashing
- **Server**: Uvicorn (ASGI)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **UI**: Mobile-first responsive design

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Supabase account)
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/Tafhim512/Checkbhai.git
cd Checkbhai/checkbhai-backend
```

2. **Create virtual environment** (Optional for local testing)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run the backend**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd checkbhai-frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.local.example .env.local
# Edit NEXT_PUBLIC_API_URL if backend is not on localhost:8000
```

4. **Run the development server**
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 📚 API Documentation

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Scam Detection
- `POST /check/message` - Check if message is scam
  ```json
  {
    "message": "text to check"
  }
  ```
  Response:
  ```json
  {
    "risk_level": "High|Medium|Low",
    "confidence": 0.95,
    "red_flags": ["⚠️ Creates artificial urgency", ...],
    "explanation": "...",
    "message_id": "uuid"
  }
  ```

### History
- `GET /history/` - Get user's check history
- `GET /history/stats` - Get user statistics

### Payment
- `POST /payment/` - Create payment
- `GET /payment/history` - Get payment history

### Admin (Requires admin role)
- `GET /admin/stats` - Platform statistics
- `GET /admin/messages` - All messages
- `POST /admin/retrain` - Retrain AI model

## 🎯 AI Training Dataset

The initial model is trained on 50+ examples covering:

- **Job Scams**: Fake recruiters, advance fees
- **Agent Scams**: Visa fraud, guarantees
- **Seller Scams**: Too-good prices, prepayment required
- **Investment Scams**: High returns, pyramid schemes
- **Course Scams**: Fake certifications, urgency tactics

**Languages**: English, Bangla (Unicode), Banglish (Romanized)

## 🔐 Default Admin Credentials

**Email**: admin@checkbhai.com  
**Password**: admin123

⚠️ **Change these in production!**

## 🌐 Deployment

### Backend (Railway/Render)
1. Connect your GitHub repository
2. Set environment variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `ADMIN_EMAIL`
   - `ADMIN_PASSWORD`
3. Deploy from `checkbhai-backend` directory

### Frontend (Vercel)
1. Import project from GitHub
2. Set Root Directory to `checkbhai-frontend`
3. Add environment variable:
   - `NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app`
4. Deploy

## 🧪 Testing the System

### Test Messages

**High Risk Scam (English)**:
```
Work from home and earn $5000/month! No experience needed. Just pay $200 registration fee to start earning today!
```

**High Risk Scam (Banglish)**:
```
Apni selected hoyechen! Dubai job paben, salary 80000 taka. Taka pathao 15000, visa processing er jonno. Taratari koren!
```

**Legitimate Message**:
```
Thank you for applying to our Software Engineer position. We'd like to schedule an interview next week. Please confirm your availability.
```

## 🔄 Human-in-Loop AI Retraining

1. Login as admin
2. Navigate to `/admin`
3. Add new training examples with labels
4. Click "Add to Training & Retrain Model"
5. Model is automatically retrained with new data

## 🛣️ Roadmap

- [ ] Screenshot/image OCR detection
- [ ] Telegram/WhatsApp bot integration
- [ ] Community reporting system
- [ ] API integration with marketplaces
- [ ] Premium subscription plans
- [ ] Multi-device sync
- [ ] Email alerts for suspicious patterns

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions, please open an issue on GitHub or contact admin@checkbhai.com

---

**Built with ❤️ for Bangladesh** 🇧🇩
