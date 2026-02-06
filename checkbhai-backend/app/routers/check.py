"""
Message checking routes - core scam detection functionality
 STRICT COMPLIANCE: 
 - Risk Level from Rules Engine ONLY (Deterministic)
 - AI used ONLY for explanation/summary
 - No fake probabilities
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import Message, User, get_db
from app.models import MessageCheck, RiskCheckResult
from app.services.ai_service import get_ai_service
from app.rules_engine import RulesEngine
from app.auth import get_current_user_optional
from app.utils import get_fingerprint

router = APIRouter(prefix="/check", tags=["scam-detection"])

@router.post("/message", response_model=RiskCheckResult)
async def check_message(
    message_data: MessageCheck,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Check if a message is a scam.
    RISK SOURCE: Rules Engine (Deterministic Patterns)
    EXPLANATION SOURCE: AI (Language Model)
    """
    
    message_text = message_data.message
    fingerprint = get_fingerprint(request)
    
    # STEP 1: Rule-Based Analysis (Source of Truth for Risk)
    rules_engine = RulesEngine()
    red_flags, rules_score = rules_engine.check_message(message_text)
    risk_level = rules_engine.get_risk_level(rules_score)
    
    # STEP 2: AI Analysis (Explanation Only)
    ai_service = get_ai_service()
    # We ignore AI's scam_probability/prediction for risk assignment
    ai_result = await ai_service.analyze_message(message_text)
    
    # Combine red flags (AI might find semantic ones)
    all_red_flags = list(set(ai_result.get("red_flags", []) + red_flags))
    
    # Use AI explanation if available, otherwise fallback to template
    explanation = ai_result.get("explanation_en", 
        rules_engine.generate_explanation(message_text, risk_level, all_red_flags)
    )
    explanation_bn = ai_result.get("explanation_bn",
        rules_engine.generate_explanation_bn(message_text, risk_level, all_red_flags)
    )
    
    # Try to save to database (non-blocking)
    message_id = None
    try:
        message_record = Message(
            user_id=current_user.id if current_user else None,
            message_text=message_text,
            risk_level=risk_level,
            confidence=1.0, # Rules are deterministic, so confidence is 100% in the rule match
            red_flags=all_red_flags,
            explanation=explanation,
            ai_prediction="N/A", # Explicitly not using AI prediction
            rules_score=rules_score,
            fingerprint=fingerprint
        )
        
        db.add(message_record)
        await db.commit()
        await db.refresh(message_record)
        message_id = str(message_record.id)
    except Exception as e:
        print(f"Database write failed (non-critical): {e}")
        await db.rollback()
    
    return RiskCheckResult(
        risk_level=risk_level,
        confidence=1.0, # Deterministic match
        red_flags=all_red_flags,
        explanation=explanation,
        explanation_bn=explanation_bn,
        ai_prediction="N/A",
        ai_confidence=0.0, # AI probability hidden/unused
        rules_score=rules_score,
        message_id=message_id
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CheckBhai Scam Detection"}
