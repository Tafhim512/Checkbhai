"""
CheckBhai Reports Router - Handling report submission and evidence
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
import uuid
from datetime import datetime

from app.database import Report, Evidence, Entity, User, Vote, ActivityLog, get_db
from app.models import ReportCreate, ReportResponse, VoteCreate
from app.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a new scam report with evidence
    """
    # Verify entity exists
    entity_result = await db.execute(select(Entity).filter(Entity.id == report_data.entity_id))
    entity = entity_result.scalar_one_or_none()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Create report
    report = Report(
        reporter_id=current_user.id,
        entity_id=report_data.entity_id,
        scam_type=report_data.scam_type,
        amount_lost=report_data.amount_lost,
        currency=report_data.currency,
        description=report_data.description,
        status="pending"
    )
    db.add(report)
    await db.flush() # Get report ID
    
    # Add evidence
    for ev in report_data.evidence:
        evidence = Evidence(
            report_id=report.id,
            file_url=ev.file_url,
            file_type=ev.file_type,
            ai_validation_status="pending"
        )
        db.add(evidence)
    
    # Update entity stats
    entity.total_reports += 1
    # Simple risk score increase for now
    entity.risk_score = min(100, entity.risk_score + 10)
    if entity.risk_score > 60:
        entity.trust_level = "Low"
    elif entity.risk_score > 30:
        entity.trust_level = "Medium"
    
    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action="submit_report",
        entity_id=report.id,
        extra_metadata={"entity_id": str(entity.id)}
    )
    db.add(log)
    
    await db.commit()
    await db.refresh(report)
    
    return report

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

@router.post("/{report_id}/vote")
async def vote_on_report(
    report_id: uuid.UUID,
    vote_data: VoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cast a community vote on a report
    Updates reputation and entity risk
    """
    # Check if user already voted
    existing_vote_result = await db.execute(
        select(Vote).filter(Vote.report_id == report_id, Vote.user_id == current_user.id)
    )
    if existing_vote_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You have already voted on this report")
    
    # Get report and entity
    report_result = await db.execute(select(Report).filter(Report.id == report_id))
    report = report_result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    entity_result = await db.execute(select(Entity).filter(Entity.id == report.entity_id))
    entity = entity_result.scalar_one_or_none()
    
    # Create vote
    vote = Vote(
        user_id=current_user.id,
        report_id=report_id,
        vote_type=vote_data.vote_type,
        weight=current_user.vote_weight
    )
    db.add(vote)
    
    # Update reputation logic (simplified)
    # Confirming a scam gives reputation, flagging false report costs if wrong, etc.
    if vote_data.vote_type == "confirm_scam":
        current_user.reputation_score += 5
        entity.risk_score = min(100, entity.risk_score + 2)
    elif vote_data.vote_type == "confirm_safe":
        entity.risk_score = max(0, entity.risk_score - 5)
    
    # Threshold for status change
    # If a report gets enough 'confirm_scam' weight, it becomes 'verified'
    vote_sum_result = await db.execute(
        select(func.sum(Vote.weight)).filter(Vote.report_id == report_id, Vote.vote_type == "confirm_scam")
    )
    confirm_weight = vote_sum_result.scalar() or 0.0
    
    if confirm_weight >= 10.0 and report.status == "pending":
        report.status = "verified"
        # Update entity trust level
        entity.trust_level = "High Risk" if entity.risk_score > 80 else "Low"
    
    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action="cast_vote",
        entity_id=report_id,
        extra_metadata={"vote_type": vote_data.vote_type, "new_status": report.status}
    )
    db.add(log)
    
    await db.commit()
    return {"message": "Vote recorded successfully", "report_status": report.status}

@router.post("/{report_id}/appeal")
async def appeal_report(
    report_id: uuid.UUID,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allow an entity owner or interested party to appeal a report
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if report.status == "appealed":
        raise HTTPException(status_code=400, detail="This report is already under appeal")
        
    report.status = "appealed"
    
    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action="submit_appeal",
        entity_id=report_id,
        extra_metadata={"reason": reason}
    )
    db.add(log)
    
    await db.commit()
    return {"message": "Appeal submitted and report is now under review"}
