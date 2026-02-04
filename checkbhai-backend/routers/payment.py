"""
Payment processing routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from database import Payment, User, get_db
from models import PaymentCreate, PaymentResponse
from auth import get_current_user

router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Process a payment (Simulated)
    """
    
    # Generate transaction ID
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    # Store payment details based on method
    payment_details = {
        "mobile_number": payment_data.mobile_number,
        "account_number": payment_data.account_number,
        "bank_name": payment_data.bank_name
    }
    
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=payment_data.amount,
        method=payment_data.method,
        status="completed", # Simulated success
        transaction_id=transaction_id,
        payment_details=payment_details,
        tier=payment_data.tier
    )
    
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    
    return payment

@router.get("/history", response_model=list[PaymentResponse])
async def get_payment_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's payment history"""
    
    from sqlalchemy import select, desc
    
    result = await db.execute(
        select(Payment)
        .filter(Payment.user_id == current_user.id)
        .order_by(desc(Payment.created_at))
        .limit(50)
    )
    payments = result.scalars().all()
    
    return payments
