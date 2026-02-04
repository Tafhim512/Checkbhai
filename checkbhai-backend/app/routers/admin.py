"""
Admin routes - statistics, message review, AI retraining
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List

from app.database import Message, User, Payment, TrainingData, get_db
from app.models import AdminStats, RetrainRequest, MessageHistory
from app.auth import get_current_admin
from app.ai_engine import get_ai_engine

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get platform statistics"""
    
    # Total users
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar() or 0
    
    # Total message checks
    total_checks_result = await db.execute(select(func.count(Message.id)))
    total_checks = total_checks_result.scalar() or 0
    
    # Total scams detected (High risk)
    total_scams_result = await db.execute(
        select(func.count(Message.id)).filter(Message.risk_level == "High")
    )
    total_scams = total_scams_result.scalar() or 0
    
    # Total payments
    total_payments_result = await db.execute(select(func.count(Payment.id)))
    total_payments = total_payments_result.scalar() or 0
    
    # Calculate scam percentage
    scam_percentage = (total_scams / total_checks * 100) if total_checks > 0 else 0
    
    return AdminStats(
        total_users=total_users,
        total_checks=total_checks,
        total_scams_detected=total_scams,
        total_payments=total_payments,
        scam_percentage=round(scam_percentage, 2)
    )

@router.get("/messages", response_model=List[MessageHistory])
async def get_all_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    risk_filter: str = Query(None, pattern="^(Low|Medium|High)$"),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get all message checks with filters"""
    
    query = select(Message)
    
    if risk_filter:
        query = query.filter(Message.risk_level == risk_filter)
    
    query = query.order_by(desc(Message.created_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return messages

@router.post("/retrain")
async def retrain_model(
    retrain_data: RetrainRequest,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrain AI model with new data (human-in-the-loop)
    """
    
    # Save new training data to database
    for item in retrain_data.training_data:
        training_record = TrainingData(
            text=item.text,
            label=item.label,
            category=item.category,
            verified_by_admin=True,
            admin_id=current_admin.id
        )
        db.add(training_record)
    
    await db.commit()
    
    # Prepare data for retraining
    new_texts = [item.text for item in retrain_data.training_data]
    new_labels = [1 if item.label == 'Scam' else 0 for item in retrain_data.training_data]
    
    # Retrain AI model
    ai_engine = get_ai_engine()
    ai_engine.retrain_with_feedback(new_texts, new_labels)
    
    return {
        "status": "success",
        "message": f"Model retrained with {len(new_texts)} new examples",
        "total_examples": len(new_texts)
    }

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get recent platform activity"""
    
    # Recent messages
    messages_result = await db.execute(
        select(Message).order_by(desc(Message.created_at)).limit(limit)
    )
    recent_messages = messages_result.scalars().all()
    
    # Recent payments
    payments_result = await db.execute(
        select(Payment).order_by(desc(Payment.created_at)).limit(limit)
    )
    recent_payments = payments_result.scalars().all()
    
    return {
        "recent_checks": [
            {
                "id": str(msg.id),
                "risk_level": msg.risk_level,
                "created_at": msg.created_at.isoformat()
            } for msg in recent_messages
        ],
        "recent_payments": [
            {
                "id": str(pay.id),
                "amount": pay.amount,
                "method": pay.method,
                "created_at": pay.created_at.isoformat()
            } for pay in recent_payments
        ]
    }
