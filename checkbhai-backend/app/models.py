"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid

# Auth schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    is_admin: bool

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Message check schemas
class MessageCheck(BaseModel):
    message: str = Field(..., min_length=10, max_length=5000)
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class RedFlag(BaseModel):
    flag: str
    severity: str = "medium"

class ScamCheckResult(BaseModel):
    risk_level: str  # Low, Medium, High
    confidence: float
    red_flags: List[str]
    explanation: str
    ai_prediction: Optional[str] = None
    ai_confidence: Optional[float] = None
    rules_score: Optional[int] = None
    message_id: Optional[str] = None

# History schemas
class MessageHistory(BaseModel):
    id: uuid.UUID
    message_text: str
    risk_level: str
    confidence: float
    red_flags: Optional[List[str]] = []
    explanation: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Payment schemas
class PaymentCreate(BaseModel):
    amount: float = Field(..., gt=0)
    method: str = Field(..., pattern="^(bkash|rocket|bank)$")
    mobile_number: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    
    @validator('mobile_number')
    def validate_mobile(cls, v, values):
        if values.get('method') in ['bkash', 'rocket'] and not v:
            raise ValueError('Mobile number required for mobile banking')
        if v and not v.startswith('01') and not len(v) == 11:
            raise ValueError('Invalid Bangladesh mobile number')
        return v
    
    @validator('account_number')
    def validate_account(cls, v, values):
        if values.get('method') == 'bank' and not v:
            raise ValueError('Account number required for bank transfer')
        return v

class PaymentResponse(BaseModel):
    id: uuid.UUID
    amount: float
    method: str
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Admin schemas
class AdminStats(BaseModel):
    total_users: int
    total_checks: int
    total_scams_detected: int
    total_payments: int
    scam_percentage: float

class TrainingDataCreate(BaseModel):
    text: str
    label: str = Field(..., pattern="^(Scam|Legit)$")
    category: Optional[str] = None

class RetrainRequest(BaseModel):
    training_data: List[TrainingDataCreate]
