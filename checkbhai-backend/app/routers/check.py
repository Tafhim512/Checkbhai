"""
Message checking routes - core scam detection functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import Message, User, get_db
from app.models import MessageCheck, ScamCheckResult
from app.ai_engine import get_ai_engine
from app.rules_engine import RulesEngine
from app.auth import get_current_user_optional

router = APIRouter(prefix="/check", tags=["scam-detection"])

@router.post("/message", response_model=ScamCheckResult)
async def check_message(
    message_data: MessageCheck,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Check if a message is a scam
    Combines AI model with rules engine for comprehensive detection
    """
    
    message_text = message_data.message
    
    # Get AI prediction
    ai_engine = get_ai_engine()
    ai_analysis = ai_engine.analyze(message_text)
    
    # Get rules-based analysis
    rules_engine = RulesEngine()
    red_flags, rules_score = rules_engine.check_message(message_text)
    
    # Combine AI and rules for final decision
    # AI provides base confidence, rules add/modify risk level
    ai_confidence = ai_analysis['confidence']
    
    # Calculate combined score (weighted average)
    # AI weight: 60%, Rules weight: 40%
    combined_score = (ai_confidence * 60) + (rules_score * 0.4)
    
    # Determine final risk level
    if combined_score >= 60:
        risk_level = "High"
    elif combined_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Override: If AI is very confident AND rules also flag it, it's definitely high risk
    if ai_analysis['is_scam'] and ai_confidence > 0.8 and rules_score > 50:
        risk_level = "High"
    
    # Generate explanation
    explanation = rules_engine.generate_explanation(
        message_text,
        risk_level,
        red_flags,
        ai_confidence
    )
    
    # Save to database
    message_record = Message(
        user_id=current_user.id if current_user else None,
        message_text=message_text,
        risk_level=risk_level,
        confidence=combined_score / 100.0,
        red_flags=red_flags,
        explanation=explanation,
        ai_prediction=ai_analysis['prediction'],
        rules_score=rules_score
    )
    
    db.add(message_record)
    await db.commit()
    await db.refresh(message_record)
    
    return ScamCheckResult(
        risk_level=risk_level,
        confidence=combined_score / 100.0,
        red_flags=red_flags,
        explanation=explanation,
        ai_prediction=ai_analysis['prediction'],
        ai_confidence=ai_confidence,
        rules_score=rules_score,
        message_id=str(message_record.id)
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CheckBhai Scam Detection"}
