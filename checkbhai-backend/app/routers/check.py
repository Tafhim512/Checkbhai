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
    Combines AI model, LLM reasoning, and rules engine
    """
    
    message_text = message_data.message
    
    # Get Enhanced AI analysis (Async)
    ai_engine = get_ai_engine()
    ai_analysis = await ai_engine.analyze_text(message_text)
    
    # Get rules-based analysis
    rules_engine = RulesEngine()
    red_flags_rules, rules_score = rules_engine.check_message(message_text)
    
    # Combine results
    # Use LLM probability if available, otherwise local model
    scam_prob = ai_analysis.get("scam_probability", ai_analysis["confidence"])
    
    # Calculate combined score
    combined_score = (scam_prob * 70) + (rules_score * 0.3)
    
    # Determine final risk level
    if combined_score >= 60 or ai_analysis["is_scam"]:
        risk_level = "High"
    elif combined_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Collect all red flags
    all_red_flags = list(set(ai_analysis.get("red_flags", []) + red_flags_rules))
    
    # Generate explanation (Prefer LLM explanation)
    explanation = ai_analysis.get("explanation_en", 
        rules_engine.generate_explanation(message_text, risk_level, all_red_flags, scam_prob)
    )
    
    # Save to database
    message_record = Message(
        user_id=current_user.id if current_user else None,
        message_text=message_text,
        risk_level=risk_level,
        confidence=combined_score / 100.0 if combined_score <= 100 else 1.0,
        red_flags=all_red_flags,
        explanation=explanation,
        ai_prediction=ai_analysis["prediction"],
        rules_score=rules_score
    )
    
    db.add(message_record)
    await db.commit()
    await db.refresh(message_record)
    
    return ScamCheckResult(
        risk_level=risk_level,
        confidence=message_record.confidence,
        red_flags=all_red_flags,
        explanation=explanation,
        ai_prediction=ai_analysis["prediction"],
        ai_confidence=scam_prob,
        rules_score=rules_score,
        message_id=str(message_record.id)
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CheckBhai Scam Detection"}
