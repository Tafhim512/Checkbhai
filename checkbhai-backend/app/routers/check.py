"""
Message checking routes - core scam detection functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import Message, User, get_db
from app.models import MessageCheck, ScamCheckResult
from app.services.ai_service import get_ai_service
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
    Combines AI model, LLM reasoning, and rules engine
    """
    
    message_text = message_data.message
    
    # NEW: Use Unified AI service with Fallback
    ai_service = get_ai_service()
    ai_result = await ai_service.analyze_message(message_text)
    
    # Get local rules-based analysis
    rules_engine = RulesEngine()
    red_flags_rules, rules_score = rules_engine.check_message(message_text)
    
    # Combine results
    # Use AI probability if available
    scam_prob = ai_result.get("scam_probability", 0.0)
    is_scam_ai = ai_result.get("is_scam", False)
    
    # Calculate combined score
    combined_score = (scam_prob * 70) + (rules_score * 0.3)
    
    # Determine final risk level
    if combined_score >= 60 or is_scam_ai:
        risk_level = "High"
    elif combined_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Collect all red flags
    all_red_flags = list(set(ai_result.get("red_flags", []) + red_flags_rules))
    
    # Generate explanation (Prefer AI explanation)
    explanation = ai_result.get("explanation_en", 
        rules_engine.generate_explanation(message_text, risk_level, all_red_flags, scam_prob)
    )
    explanation_bn = ai_result.get("explanation_bn",
        rules_engine.generate_explanation_bn(message_text, risk_level, all_red_flags)
    )
    
    # Try to save to database (non-blocking - don't fail if DB errors)
    message_id = None
    try:
        message_record = Message(
            user_id=current_user.id if current_user else None,
            message_text=message_text,
            risk_level=risk_level,
            confidence=combined_score / 100.0 if combined_score <= 100 else 1.0,
            red_flags=all_red_flags,
            explanation=explanation,
            ai_prediction="Scam" if is_scam_ai else "Legit",
            rules_score=rules_score
        )
        
        db.add(message_record)
        await db.commit()
        await db.refresh(message_record)
        message_id = str(message_record.id)
    except Exception as e:
        # Log error but don't fail the request
        print(f"Database write failed (non-critical): {e}")
        await db.rollback()
    
    return ScamCheckResult(
        risk_level=risk_level,
        confidence=combined_score / 100.0 if combined_score <= 100 else 1.0,
        red_flags=all_red_flags,
        explanation=explanation,
        explanation_bn=explanation_bn,
        ai_prediction="Scam" if is_scam_ai else "Legit",
        ai_confidence=scam_prob,
        rules_score=rules_score,
        message_id=message_id
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CheckBhai Scam Detection"}
