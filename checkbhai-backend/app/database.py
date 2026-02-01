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
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/checkbhai"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

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
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Message(Base):
    """Message check history"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Optional for anonymous checks
    message_text = Column(Text, nullable=False)
    risk_level = Column(String(20), nullable=False)  # Low, Medium, High
    confidence = Column(Float, nullable=False)
    red_flags = Column(JSON, nullable=True)  # List of red flags
    explanation = Column(Text, nullable=True)
    ai_prediction = Column(String(20), nullable=True)
    rules_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Payment(Base):
    """Payment records"""
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(50), nullable=False)  # bkash, rocket, bank
    status = Column(String(20), nullable=False, default="pending")  # pending, completed, failed
    transaction_id = Column(String(255), nullable=True)
    payment_details = Column(JSON, nullable=True)  # Store method-specific details
    created_at = Column(DateTime, default=datetime.utcnow)

class TrainingData(Base):
    """AI training data with human verification"""
    __tablename__ = "training_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    label = Column(String(20), nullable=False)  # Scam or Legit
    category = Column(String(50), nullable=True)
    language = Column(String(20), nullable=True)
    verified_by_admin = Column(Boolean, default=False)
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
    """Initialize database tables"""
    async with engine.begin() as conn:
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
            is_admin=True
        )
        session.add(admin)
        await session.commit()
        print(f"Admin user created: {email}")
