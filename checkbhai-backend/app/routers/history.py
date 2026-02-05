"""
User history routes - retrieve message check history
"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_
from typing import List, Optional

from app.database import Message, User, get_db
from app.models import MessageHistory
from app.auth import get_current_user, get_current_user_optional
from app.utils import get_fingerprint

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=List[MessageHistory])
async def get_user_history(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    risk_filter: str = Query(None, pattern="^(Low|Medium|High)$"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    Get message check history.
    If logged in: Get by user_id.
    If anonymous: Get by device fingerprint (IP+UA).
    """
    
    fingerprint = get_fingerprint(request)
    
    # Build query
    if current_user:
        # Logged in users see their account history
        query = select(Message).filter(Message.user_id == current_user.id)
    else:
        # Anonymous users see history for their current device
        query = select(Message).filter(Message.fingerprint == fingerprint, Message.user_id == None)
    
    # Apply risk filter if provided
    if risk_filter:
        query = query.filter(Message.risk_level == risk_filter)
    
    # Order by most recent first
    query = query.order_by(desc(Message.created_at))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return messages

@router.get("/stats")
async def get_user_stats(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """Get message check statistics"""
    
    from sqlalchemy import func
    
    fingerprint = get_fingerprint(request)
    
    # Build base filter
    if current_user:
        base_filter = Message.user_id == current_user.id
    else:
        base_filter = (Message.fingerprint == fingerprint) & (Message.user_id == None)
    
    # Total checks
    total_result = await db.execute(
        select(func.count(Message.id)).filter(base_filter)
    )
    total_checks = total_result.scalar() or 0
    
    # High risk count
    high_risk_result = await db.execute(
        select(func.count(Message.id)).filter(
            base_filter,
            Message.risk_level == "High"
        )
    )
    high_risk_count = high_risk_result.scalar() or 0
    
    # Medium risk count
    medium_risk_result = await db.execute(
        select(func.count(Message.id)).filter(
            base_filter,
            Message.risk_level == "Medium"
        )
    )
    medium_risk_count = medium_risk_result.scalar() or 0
    
    return {
        "total_checks": total_checks,
        "high_risk_count": high_risk_count,
        "medium_risk_count": medium_risk_count,
        "low_risk_count": total_checks - high_risk_count - medium_risk_count,
        "scam_percentage": (high_risk_count / total_checks * 100) if total_checks > 0 else 0
    }
