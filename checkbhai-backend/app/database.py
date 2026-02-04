"""
Database configuration and models for CheckBhai
Using SQLAlchemy with async support
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import os

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL:
    # Auto-correct scheme for asyncpg
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # Ensure SSL for Supabase/Production
    if "supabase.co" in DATABASE_URL or "pooler.supabase.com" in DATABASE_URL:
        if "sslmode=" not in DATABASE_URL:
            connector = "&" if "?" in DATABASE_URL else "?"
            DATABASE_URL += f"{connector}sslmode=require"
    
    # Log connection attempt (redacting password)
    try:
        parts = DATABASE_URL.split("@")
        if len(parts) > 1:
            print(f"Connecting to DB at: {parts[1].split('/')[0]}")
    except:
        pass

# Create async engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
    pool_pre_ping=True,
    connect_args={
        "command_timeout": 10,
        "server_settings": {
            "application_name": "CheckBhai-Backend"
        }
    }
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Database Models

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    reputation_score = Column(Integer, default=100)
    vote_weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Entity(Base):
    """Entities being checked (Phone, URL, FB Page, etc.)"""
    __tablename__ = "entities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(50), nullable=False, index=True)  # phone, fb_page, website, etc.
    identifier = Column(String(255), nullable=False, index=True)
    risk_score = Column(Integer, default=0)
    trust_level = Column(String(20), default="Low") # Low, Medium, High
    scam_probability = Column(Float, default=0.0)
    total_reports = Column(Integer, default=0)
    extra_metadata = Column(JSON, nullable=True)
    last_checked = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    """Message check history"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    message_text = Column(Text, nullable=False)
    risk_level = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    red_flags = Column(JSON, nullable=True)
    explanation = Column(Text, nullable=True)
    ai_prediction = Column(String(20), nullable=True)
    rules_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Report(Base):
    """Evidence-based reports"""
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    scam_type = Column(String(100), nullable=False)
    amount_lost = Column(Float, default=0.0)
    currency = Column(String(10), default="BDT")
    description = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, verified, rejected, appealed
    ai_validation_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Evidence(Base):
    """Supporting evidence for reports (screenshots, documents)"""
    __tablename__ = "evidence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False)
    file_url = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)  # image, pdf
    ai_validation_status = Column(String(20), default="pending")
    extra_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Vote(Base):
    """Community verification votes"""
    __tablename__ = "votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False)
    vote_type = Column(String(20), nullable=False)  # confirm_scam, confirm_safe, flag_false
    weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    """Payment records for premium features"""
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    transaction_id = Column(String(255), nullable=True)
    payment_details = Column(JSON, nullable=True)
    tier = Column(String(20), default="premium_one_month")
    created_at = Column(DateTime, default=datetime.utcnow)

class ActivityLog(Base):
    """Audit log for major actions"""
    __tablename__ = "activity_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    extra_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrainingData(Base):
    """Verified training data for AI model"""
    __tablename__ = "training_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    label = Column(String(20), nullable=False)
    category = Column(String(50), nullable=True)
    verified_by_admin = Column(Boolean, default=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get database session
async def get_db():
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database tables with connection verification"""
    print(f"DEBUG: Attempting to connect to DB...")
    async with engine.begin() as conn:
        print("DEBUG: Connection established, creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully")

async def create_admin_user(email: str, password: str):
    """Create an admin user"""
    from app.auth import hash_password
    
    async with AsyncSessionLocal() as session:
        # Check if admin already exists
        from sqlalchemy import select
        result = await session.execute(select(User).filter(User.email == email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"Admin user {email} already exists")
            return
        
        # Create admin user
        admin = User(
            email=email,
            password_hash=hash_password(password),
            is_admin=True,
            reputation_score=1000, # Admins start with max reputation
            vote_weight=10.0
        )
        session.add(admin)
        await session.commit()
        print(f"Admin user created: {email}")
