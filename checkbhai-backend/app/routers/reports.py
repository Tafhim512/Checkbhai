"""
CheckBhai Reports Router - Community Report Submission (Append-Only)
WITH EXPLICIT LOGGING TO PROVE DATA FLOW IS REAL
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import uuid
import logging
from datetime import datetime, timedelta

from app.database import Report, Evidence, Entity, User, ActivityLog, get_db
from app.models import ReportCreate, ReportResponse
from app.auth import get_current_user, get_current_user_optional

# Setup logging
logger = logging.getLogger("checkbhai.reports")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/reports", tags=["reports"])


def recalculate_entity_trust(scam_reports: int, verified_reports: int, total_reports: int, recent_reports_count: int) -> tuple[str, str, int]:
    """Recalculate entity trust score from ACTUAL values"""
    base_score = (scam_reports * 3) + (verified_reports * 5) + (recent_reports_count * 2)
    
    if base_score == 0:
        risk_status = "Insufficient Data"
    elif base_score <= 4:
        risk_status = "Low Risk"
    elif base_score <= 9:
        risk_status = "Medium Risk"
    else:
        risk_status = "High Risk"
    
    if total_reports <= 2:
        confidence_level = "Low"
    elif total_reports <= 7:
        confidence_level = "Medium"
    else:
        confidence_level = "High"
    
    return risk_status, confidence_level, base_score


@router.post("/", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Submit a new scam report.
    THIS UPDATES THE DATABASE - NOT A MOCK.
    """
    logger.info(f"[TRUTH LOOP] Report submission started for entity_id={report_data.entity_id}")
    
    # Verify entity exists
    entity_result = await db.execute(select(Entity).filter(Entity.id == report_data.entity_id))
    entity = entity_result.scalar_one_or_none()
    
    if not entity:
        logger.error(f"[TRUTH LOOP] Entity NOT FOUND: {report_data.entity_id}")
        raise HTTPException(status_code=404, detail="Entity not found. Please search for the entity first.")
    
    logger.info(f"[TRUTH LOOP] Entity found: identifier={entity.identifier}, current_reports={entity.total_reports}")
    
    # STEP 1: Create report in database
    report = Report(
        reporter_id=current_user.id if current_user else None,
        entity_id=report_data.entity_id,
        platform=report_data.platform,
        scam_type=report_data.scam_type,
        amount_lost=report_data.amount_lost,
        currency=report_data.currency,
        description=report_data.description,
        status="pending"
    )
    db.add(report)
    await db.flush()
    
    logger.info(f"[TRUTH LOOP] Report created with id={report.id}")
    
    # Add evidence if provided
    for ev in report_data.evidence:
        evidence = Evidence(
            report_id=report.id,
            file_url=ev.file_url,
            file_type=ev.file_type,
            ai_validation_status="pending"
        )
        db.add(evidence)
    
    # STEP 2: UPDATE ENTITY COUNTS IN DATABASE
    old_total = entity.total_reports or 0
    old_scam = entity.scam_reports or 0
    
    entity.total_reports = old_total + 1
    entity.scam_reports = old_scam + 1
    entity.last_reported_date = datetime.utcnow()
    
    logger.info(f"[TRUTH LOOP] Entity stats UPDATED: total_reports {old_total} -> {entity.total_reports}, scam_reports {old_scam} -> {entity.scam_reports}")
    
    # STEP 3: Recalculate risk score
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_result = await db.execute(
        select(func.count(Report.id)).filter(
            Report.entity_id == entity.id,
            Report.created_at >= seven_days_ago
        )
    )
    recent_count = (recent_result.scalar() or 0) + 1  # +1 for current report
    
    risk_status, confidence_level, base_score = recalculate_entity_trust(
        scam_reports=entity.scam_reports,
        verified_reports=entity.verified_reports or 0,
        total_reports=entity.total_reports,
        recent_reports_count=recent_count
    )
    
    entity.risk_status = risk_status
    entity.confidence_level = confidence_level
    
    logger.info(f"[TRUTH LOOP] NEW RISK: base_score={base_score}, risk_status={risk_status}, confidence={confidence_level}")
    
    # Log activity
    log = ActivityLog(
        user_id=current_user.id if current_user else None,
        action="submit_report",
        entity_id=report.id,
        extra_metadata={
            "entity_id": str(entity.id),
            "scam_type": report_data.scam_type,
            "platform": report_data.platform,
            "new_total_reports": entity.total_reports,
            "new_risk_status": entity.risk_status
        }
    )
    db.add(log)
    
    # STEP 4: Commit to database
    await db.commit()
    await db.refresh(report)
    
    logger.info(f"[TRUTH LOOP] Report COMMITTED. Entity {entity.identifier} now has {entity.total_reports} reports, risk={entity.risk_status}")
    
    return report


@router.get("/", response_model=List[ReportResponse])
async def get_all_reports(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get all reports"""
    result = await db.execute(
        select(Report).order_by(Report.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_details(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed report information"""
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report
