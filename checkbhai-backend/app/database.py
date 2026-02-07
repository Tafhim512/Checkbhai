"""
Database configuration and models for CheckBhai
Using SQLAlchemy with async support
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship  # CRITICAL: Required for Entity and EntityClaim models
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import os

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL:
    # 1. Ensure the dialect is postgresql+asyncpg
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # 2. Strip ALL ssl/sslmode parameters and clean up separators
    import re
    DATABASE_URL = re.sub(r'[?&]sslmode=[^&]*', '', DATABASE_URL)
    DATABASE_URL = re.sub(r'[?&]ssl=[^&]*', '', DATABASE_URL)
    DATABASE_URL = DATABASE_URL.rstrip('?&')
    
    # 3. Log connection attempt (redacted)
    try:
        parts = DATABASE_URL.split("@")
        if len(parts) > 1:
            print(f"Connecting to DB at: {parts[1].split('/')[0]}")
    except:
        pass
else:
    print("WARNING: DATABASE_URL not set. Using SQLite fallback for local development.")
    DATABASE_URL = "sqlite+aiosqlite:///./checkbhai_dev.db"

# Create async engine with appropriate settings
import ssl

if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL with SSL for production
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    engine = create_async_engine(
        DATABASE_URL, 
        echo=False, 
        future=True,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={
            "ssl": ctx,
            "statement_cache_size": 0,
            "command_timeout": 60,
            "server_settings": {
                "application_name": "CheckBhai-Backend"
            }
        }
    )
else:
    # SQLite for local development
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True
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
    """Entities being checked (Phone, FB Page, WhatsApp, Shop, Agent, Payment ID, etc.)"""
    __tablename__ = "entities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(50), nullable=False, index=True)  # phone, fb_page, fb_profile, whatsapp, shop, agent, bkash, nagad, rocket
    identifier = Column(String(255), nullable=False, index=True)
    # Community-powered trust scoring fields
    total_reports = Column(Integer, default=0)
    scam_reports = Column(Integer, default=0)  # Reports claiming scam
    verified_reports = Column(Integer, default=0)  # Admin-verified reports
    last_reported_date = Column(DateTime, nullable=True)  # Last report submission date
    # Computed risk status: Insufficient Data, Low Risk, Medium Risk, High Risk
    risk_status = Column(String(30), default="Insufficient Data")
    confidence_level = Column(String(20), default="Low")  # Low, Medium, High
    extra_metadata = Column(JSON, nullable=True)
    last_checked = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    claims = relationship("EntityClaim", back_populates="entity")

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
    fingerprint = Column(String(64), nullable=True, index=True)  # SHA256 of IP + UA for anon history
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Report(Base):
    """Evidence-based community reports - append-only"""
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # nullable for anonymous
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    # Platform where scam occurred
    platform = Column(String(50), default="other")  # facebook, whatsapp, shop, agent, other
    # Scam type: no_delivery, fake_product, advance_taken, blocked_after_payment, impersonation, other
    scam_type = Column(String(100), nullable=False)
    amount_lost = Column(Float, default=0.0)
    currency = Column(String(10), default="BDT")
    description = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, verified, rejected, spam
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Evidence(Base):
    """Supporting evidence for reports (screenshots, documents)"""
    __tablename__ = "evidence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False)
    file_url = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)  # image, pdf
    ai_validation_status = Column(String(20), default="pending")
class EntityClaim(Base):
    __tablename__ = "entity_claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    contact_email = Column(String, nullable=False)
    business_name = Column(String, nullable=False)
    verification_doc_url = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, default="pending") # pending, approved, rejected
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    entity = relationship("Entity", back_populates="claims")


# Add back-populate to Entity
# Entity.claims = relationship("EntityClaim", back_populates="entity")

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
    """Initialize database tables and run migrations for existing tables"""
    print(f"DEBUG: Attempting to connect to DB for initialization...")
    async with engine.begin() as conn:
        # 1. Create tables if they don't exist
        print("DEBUG: Connection established, ensuring tables exist...")
        await conn.run_sync(Base.metadata.create_all)
        
        # 2. Safe migrations for existing tables (Production Fix)
        print("DEBUG: Running safe migrations (ALTER TABLE ... ADD COLUMN IF NOT EXISTS)...")
        from sqlalchemy import text
        
        # entities table columns
        columns = [
            ("scam_reports", "INTEGER DEFAULT 0 NOT NULL"),
            ("verified_reports", "INTEGER DEFAULT 0 NOT NULL"),
            ("report_trend", "VARCHAR(20) DEFAULT 'Stable'"),
            ("confidence_level", "VARCHAR(20) DEFAULT 'Low'"),
            ("risk_status", "VARCHAR(30) DEFAULT 'Insufficient Data'"),
            ("last_reported_date", "TIMESTAMP WITHOUT TIME ZONE")
        ]
        
        for col_name, col_type in columns:
            try:
                await conn.execute(text(f"ALTER TABLE entities ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                print(f"✅ Column 'entities.{col_name}' ready")
            except Exception as e:
                print(f"⚠️ Note: entities.{col_name} migration info: {e}")
        
        # Ensure default values for existing rows
        try:
            await conn.execute(text("UPDATE entities SET scam_reports = 0 WHERE scam_reports IS NULL"))
            await conn.execute(text("UPDATE entities SET verified_reports = 0 WHERE verified_reports IS NULL"))
        except:
            pass
            
    print("Database initialization and migration completed")

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
