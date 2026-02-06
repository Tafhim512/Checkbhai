"""
CheckBhai Backend - Main FastAPI application
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os

from app.database import init_db, create_admin_user, get_db
from app.ai_engine import get_ai_engine
from app.routers import auth, check, history, payment, admin, entities, reports, claims

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting CheckBhai Backend...")
    
    # Initialize database
    try:
        print("Initializing database...")
        await init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        # In production, we might want to continue or exit depending on strategy
        # For now, let's log it clearly
    
    # Create default admin user
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@checkbhai.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        await create_admin_user(admin_email, admin_password)
    except Exception as e:
        print(f"Admin user creation failed: {e}")
    
    # Initialize AI service (Check providers)
    try:
        from app.services.ai_service import get_ai_service
        print(f"DEBUG: GROK_API_KEY loaded: {bool(os.getenv('GROK_API_KEY'))}")
        
        ai_service = get_ai_service()
        provider_name = ai_service.provider.name if ai_service.provider else "None (Rules Only)"
        print(f"AI Service ready. Active provider: {provider_name}")
    except Exception as e:
        print(f"AI Service initialization failed: {e}")
    
    print("CheckBhai Backend ready!")
    
    yield
    
    # Shutdown
    print("Shutting down CheckBhai Backend...")

# Create FastAPI application
app = FastAPI(
    title="CheckBhai API",
    description="AI-powered scam detection platform for Bangladesh",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be False if using ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allow all hosts (required for Railway healthchecks)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]
)

# Register routers
app.include_router(auth.router)
app.include_router(check.router)
app.include_router(history.router)
app.include_router(payment.router)
app.include_router(admin.router)
app.include_router(entities.router)
app.include_router(reports.router)
app.include_router(claims.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CheckBhai API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "check": "/check",
            "history": "/history",
            "payment": "/payment",
            "admin": "/admin",
            "entities": "/entities",
            "reports": "/reports",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "CheckBhai API"}

@app.get("/seed-db")
async def seed_db(db = Depends(get_db)):
    """Temporary endpoint to seed production database"""
    # Import locally to avoid cluttering main file
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.database import User, Entity, Report, Message
    from app.auth import hash_password
    from sqlalchemy import select
    import random
    from datetime import datetime, timedelta
    import os
    
    # Type check hack
    if not isinstance(db, AsyncSession):
        pass # Should theoretically be AsyncSession

    print("🌱 Starting Production Data Seed via API...")
    
    # 1. Ensure Admin User
    admin_email = os.getenv("ADMIN_EMAIL", "admin@checkbhai.com")
    result = await db.execute(select(User).filter(User.email == admin_email))
    admin = result.scalars().first()
    
    if not admin:
        print(f"Creating admin user: {admin_email}")
        admin = User(
            email=admin_email,
            password_hash=hash_password(os.getenv("ADMIN_PASSWORD", "admin123")),
            is_admin=True,
            reputation_score=100
        )
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
    
    # 2. Seed Entities
    # High Risk Scammer
    result = await db.execute(select(Entity).filter(Entity.identifier == "01812345678"))
    scammer = result.scalars().first()
    if not scammer:
        scammer = Entity(
            type="agent",
            identifier="01812345678",
            risk_status="High Risk",
            confidence_level="High",
            total_reports=15,
            scam_reports=14,
            verified_reports=10,
            last_checked=datetime.utcnow()
        )
        db.add(scammer)
    
    # Fake Shop
    result = await db.execute(select(Entity).filter(Entity.identifier == "facebook.com/fake-shop-bd"))
    fake_shop = result.scalars().first()
    if not fake_shop:
        fake_shop = Entity(
            type="fb_page",
            identifier="facebook.com/fake-shop-bd",
            risk_status="Medium Risk",
            confidence_level="Medium",
            total_reports=5,
            scam_reports=5,
            verified_reports=2,
            last_checked=datetime.utcnow()
        )
        db.add(fake_shop)

    # Safe Number
    result = await db.execute(select(Entity).filter(Entity.identifier == "01700000000"))
    safe_guy = result.scalars().first()
    if not safe_guy:
        safe_guy = Entity(
            type="phone",
            identifier="01700000000",
            risk_status="Safe",
            confidence_level="High",
            total_reports=0,
            scam_reports=0,
            verified_reports=0,
            last_checked=datetime.utcnow()
        )
        db.add(safe_guy)
        
    await db.commit()
    
    # Refresh to ensure IDs are available
    await db.refresh(scammer)
    await db.refresh(fake_shop)
    
    # 3. Seed Reports
    descriptions = [
        "He asked for advance payment via bKash and then blocked me.",
        "Fake agent, said my account was locked. Stole 5000tk.",
        "Total fraud, do not trust this number."
    ]
    
    for desc in descriptions:
        exists = await db.execute(select(Report).filter(Report.entity_id == scammer.id, Report.description == desc))
        if not exists.scalars().first():
            report = Report(
                entity_id=scammer.id,
                platform="agent",
                scam_type="advance_taken",
                amount_lost=random.randint(500, 5000),
                currency="BDT",
                description=desc,
                status="verified",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(report)

    exists = await db.execute(select(Report).filter(Report.entity_id == fake_shop.id))
    if not exists.scalars().first():
        report = Report(
            entity_id=fake_shop.id,
            platform="facebook",
            scam_type="fake_product",
            amount_lost=1200,
            currency="BDT",
            description="Ordered a watch, received a potato. Page blocked me.",
            status="pending",
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        db.add(report)
    
    await db.commit()
    
    # 4. Seed History (for Admin)
    msgs = [
        "You won a lottery! Call 01812345678 to claim.",
        "Is 01700000000 a safe number?",
        "Urgent: Send money to 01812345678 immediately."
    ]
    
    for txt in msgs:
        exists = await db.execute(select(Message).filter(Message.user_id == admin.id, Message.message_text == txt))
        if not exists.scalars().first():
            msg = Message(
                user_id=admin.id,
                message_text=txt,
                risk_level="High" if "01812345678" in txt else "Low",
                confidence=0.9 if "01812345678" in txt else 0.95,
                red_flags=["suspicious_number"] if "01812345678" in txt else [],
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            db.add(msg)
            
    await db.commit()

    return {"status": "success", "message": "Database seeded successfully with test data!"}

@app.get("/debug-ai")
async def debug_ai():
    """Diagnose AI Service Connectivity"""
    import os
    import httpx
    
    api_key = os.getenv("GROK_API_KEY")
    api_url = os.getenv("GROK_API_URL", "https://api.grok.openai.com/v1")
    
    status = {
        "env_check": {
            "GROK_API_KEY_PRESENT": bool(api_key),
            "GROK_API_KEY_LENGTH": len(api_key) if api_key else 0,
            "GROK_API_URL": api_url
        },
        "connectivity_check": "Pending"
    }
    
    if not api_key:
        status["connectivity_check"] = "Failed: No API Key found in environment variables."
        return status
        
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [{"role": "user", "content": "Hello"}], # Correct format for OpenAI-compatible query
             "model": "grok-beta", # Try specifying model or generic
             "max_tokens": 5
        }
        # Note: Grok official API might use different payload structure depending on exact endpoint
        # Using the one from ai_service.py which was updated to {"message": ...} for the specific user request?
        # Re-checking ai_service.py: It uses json={"message": prompt}.
        # Let's match ai_service.py exactly to test THAT path.
        
        payload_test = {"message": "Test connection"}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                api_url,
                json=payload_test,
                headers=headers
            )
            
            status["http_status"] = response.status_code
            status["response_text"] = response.text
            
            if response.status_code == 200:
                status["connectivity_check"] = "SUCCESS: Connected to Grok API."
            else:
                status["connectivity_check"] = f"FAILED: API returned {response.status_code}"
                
    except Exception as e:
        status["connectivity_check"] = f"ERROR: {str(e)}"
        
    return status

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
