"""
CheckBhai Entity Router - Community-Powered Trust Scoring
WITH EXPLICIT LOGGING TO PROVE DATA FLOW IS REAL
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import uuid
import logging
from datetime import datetime, timedelta

from app.database import Entity, Report, get_db
from app.models import EntityCheck, EntityResponse, ReportResponse
from app.auth import get_current_user_optional

# Setup logging
logger = logging.getLogger("checkbhai.entities")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/entities", tags=["entities"])


def calculate_trust_score(scam_reports: int, verified_reports: int, total_reports: int, recent_reports_count: int) -> tuple[str, str, int]:
    """
    Calculate risk status and confidence level from RAW DATA.
    Returns (risk_status, confidence_level, base_score)
    """
    # Calculate base score from ACTUAL numbers
    base_score = (scam_reports * 3) + (verified_reports * 5) + (recent_reports_count * 2)
    
    # Determine risk status
    if base_score == 0:
        risk_status = "Insufficient Data"
    elif base_score <= 4:
        risk_status = "Low Risk"
    elif base_score <= 9:
        risk_status = "Medium Risk"
    else:
        risk_status = "High Risk"
    
    # Determine confidence level
    if total_reports <= 2:
        confidence_level = "Low"
    elif total_reports <= 7:
        confidence_level = "Medium"
    else:
        confidence_level = "High"
    
    return risk_status, confidence_level, base_score


@router.get("/check", response_model=EntityResponse)
async def check_entity(
    type: str = Query(..., pattern="^(phone|fb_page|fb_profile|whatsapp|shop|agent|bkash|nagad|rocket)$"),
    identifier: str = Query(..., min_length=3),
    db: AsyncSession = Depends(get_db)
):
    """
    Check an entity's risk level and community report history.
    ALWAYS QUERIES DATABASE. NO HARDCODED VALUES.
    """
    # Clean identifier
    identifier = identifier.strip().lower()
    
    logger.info(f"[TRUTH LOOP] Searching entity: type={type}, identifier={identifier}")
    
    # STEP 1: Query database for existing entity
    result = await db.execute(
        select(Entity).filter(Entity.type == type, Entity.identifier == identifier)
    )
    entity = result.scalar_one_or_none()
    
    if not entity:
        # STEP 2A: Create new entity with REAL defaults (no reports = insufficient data)
        logger.info(f"[TRUTH LOOP] Entity NOT FOUND - creating with Insufficient Data status")
        entity = Entity(
            type=type,
            identifier=identifier,
            total_reports=0,
            scam_reports=0,
            verified_reports=0,
            last_reported_date=None,
            risk_status="Insufficient Data",
            confidence_level="Low",
            extra_metadata={}
        )
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        
        logger.info(f"[TRUTH LOOP] NEW Entity created: id={entity.id}, risk_status={entity.risk_status}")
    else:
        # STEP 2B: Entity exists - QUERY ACTUAL REPORT COUNTS
        logger.info(f"[TRUTH LOOP] Entity FOUND: id={entity.id}")
        
        # Count recent reports (last 7 days) from ACTUAL database
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_result = await db.execute(
            select(func.count(Report.id)).filter(
                Report.entity_id == entity.id,
                Report.created_at >= seven_days_ago,
                Report.status != "spam"  # Exclude spam reports
            )
        )
        recent_reports_count = recent_result.scalar() or 0
        
        # STEP 3: Calculate risk from REAL DATABASE VALUES
        risk_status, confidence_level, base_score = calculate_trust_score(
            scam_reports=entity.scam_reports or 0,
            verified_reports=entity.verified_reports or 0,
            total_reports=entity.total_reports or 0,
            recent_reports_count=recent_reports_count
        )
        
        # Log the ACTUAL calculation
        logger.info(f"[TRUTH LOOP] CALCULATION: scam_reports={entity.scam_reports}, verified_reports={entity.verified_reports}, total_reports={entity.total_reports}, recent_reports={recent_reports_count}")
        logger.info(f"[TRUTH LOOP] RESULT: base_score={base_score}, risk_status={risk_status}, confidence_level={confidence_level}")
        
        # Update entity with calculated values
        entity.risk_status = risk_status
        entity.confidence_level = confidence_level
    
    # Update last checked timestamp
    entity.last_checked = datetime.utcnow()
    await db.commit()
    await db.refresh(entity)
    
    # STEP 4: Return ACTUAL values to frontend
    logger.info(f"[TRUTH LOOP] RETURNING: risk_status={entity.risk_status}, total_reports={entity.total_reports}, scam_reports={entity.scam_reports}")
    
    return entity


@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity_details(
    entity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific entity"""
    result = await db.execute(select(Entity).filter(Entity.id == entity_id))
    entity = result.scalar_one_or_none()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return entity


@router.get("/{entity_id}/reports", response_model=List[ReportResponse])
async def get_entity_reports(
    entity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get all community reports linked to an entity"""
    result = await db.execute(
        select(Report).filter(Report.entity_id == entity_id).order_by(Report.created_at.desc())
    )
    reports = result.scalars().all()
    return reports
