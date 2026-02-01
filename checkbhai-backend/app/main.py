"""
CheckBhai Backend - Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.database import init_db, create_admin_user
from app.ai_engine import get_ai_engine
from app.routers import auth, check, history, payment, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting CheckBhai Backend...")
    
    # Initialize database
    await init_db()
    
    # Create default admin user
    admin_email = os.getenv("ADMIN_EMAIL", "admin@checkbhai.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    await create_admin_user(admin_email, admin_password)
    
    # Initialize AI engine (train model if needed)
    ai_engine = get_ai_engine()
    print(f"✅ AI Engine ready (trained: {ai_engine.is_trained})")
    
    print("✅ CheckBhai Backend ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down CheckBhai Backend...")

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
    allow_origins=["*"],  # In production, specify exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(check.router)
app.include_router(history.router)
app.include_router(payment.router)
app.include_router(admin.router)

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
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CheckBhai API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
