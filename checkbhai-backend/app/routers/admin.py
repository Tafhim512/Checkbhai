"""
Admin routes - Minimal, Strong Admin Panel
- View all reports
- Mark report as Verified
- Remove spam reports
NO AI training, NO analytics bloat
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List
import uuid
from datetime import datetime, timedelta

from app.database import Report, User, Entity, ActivityLog, get_db
from app.models import ReportResponse
from app.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get platform statistics (minimal, essential only)"""
    
    # Total users
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar() or 0
    
    # Total reports
    total_reports_result = await db.execute(select(func.count(Report.id)))
    total_reports = total_reports_result.scalar() or 0
    
    # Verified reports
    verified_reports_result = await db.execute(
        select(func.count(Report.id)).filter(Report.status == "verified")
    )
    verified_reports = verified_reports_result.scalar() or 0
    
    # Pending reports
    pending_reports_result = await db.execute(
        select(func.count(Report.id)).filter(Report.status == "pending")
    )
    pending_reports = pending_reports_result.scalar() or 0
    
    # Total entities tracked
    total_entities_result = await db.execute(select(func.count(Entity.id)))
    total_entities = total_entities_result.scalar() or 0
    
    # High risk entities
    high_risk_result = await db.execute(
        select(func.count(Entity.id)).filter(Entity.risk_status == "High Risk")
    )
    high_risk_entities = high_risk_result.scalar() or 0
    
    return {
        "total_users": total_users,
        "total_reports": total_reports,
        "verified_reports": verified_reports,
        "pending_reports": pending_reports,
        "total_entities": total_entities,
        "high_risk_entities": high_risk_entities
    }


@router.get("/reports", response_model=List[ReportResponse])
async def get_all_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status_filter: str = Query(None, pattern="^(pending|verified|rejected|spam)$"),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get all reports with optional status filter"""
    
    query = select(Report)
    
    if status_filter:
        query = query.filter(Report.status == status_filter)
    
    query = query.order_by(desc(Report.created_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.put("/reports/{report_id}/verify")
async def verify_report(
    report_id: uuid.UUID,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a report as verified.
    Verified reports have higher weight in trust scoring.
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if report.status == "verified":
        raise HTTPException(status_code=400, detail="Report is already verified")
    
    # Update report status
    report.status = "verified"
    
    # Update entity's verified_reports count
    entity_result = await db.execute(select(Entity).filter(Entity.id == report.entity_id))
    entity = entity_result.scalar_one_or_none()
    
    if entity:
        entity.verified_reports = (entity.verified_reports or 0) + 1
        
        # Recalculate trust score
        scam_reports = entity.scam_reports or 0
        verified_reports = entity.verified_reports or 0
        total_reports = entity.total_reports or 0
        
        # Get recent reports count
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_result = await db.execute(
            select(func.count(Report.id)).filter(
                Report.entity_id == entity.id,
                Report.created_at >= seven_days_ago
            )
        )
        recent_count = recent_result.scalar() or 0
        
        base_score = (scam_reports * 3) + (verified_reports * 5) + (recent_count * 2)
        
        if base_score == 0:
            entity.risk_status = "Insufficient Data"
        elif base_score <= 4:
            entity.risk_status = "Low Risk"
        elif base_score <= 9:
            entity.risk_status = "Medium Risk"
        else:
            entity.risk_status = "High Risk"
        
        if total_reports <= 2:
            entity.confidence_level = "Low"
        elif total_reports <= 7:
            entity.confidence_level = "Medium"
        else:
            entity.confidence_level = "High"
    
    # Log activity
    log = ActivityLog(
        user_id=current_admin.id,
        action="verify_report",
        entity_id=report_id,
        extra_metadata={"entity_id": str(report.entity_id)}
    )
    db.add(log)
    
    await db.commit()
    
    return {"message": "Report verified successfully", "report_id": str(report_id)}


@router.delete("/reports/{report_id}")
async def delete_spam_report(
    report_id: uuid.UUID,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a report as spam (soft delete).
    This reduces the entity's scam_reports count.
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if report.status == "spam":
        raise HTTPException(status_code=400, detail="Report is already marked as spam")
    
    # Update report status
    old_status = report.status
    report.status = "spam"
    
    # Update entity stats
    entity_result = await db.execute(select(Entity).filter(Entity.id == report.entity_id))
    entity = entity_result.scalar_one_or_none()
    
    if entity:
        entity.total_reports = max(0, (entity.total_reports or 1) - 1)
        entity.scam_reports = max(0, (entity.scam_reports or 1) - 1)
        if old_status == "verified":
            entity.verified_reports = max(0, (entity.verified_reports or 1) - 1)
        
        # Recalculate trust score
        scam_reports = entity.scam_reports or 0
        verified_reports = entity.verified_reports or 0
        total_reports = entity.total_reports or 0
        
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_result = await db.execute(
            select(func.count(Report.id)).filter(
                Report.entity_id == entity.id,
                Report.created_at >= seven_days_ago,
                Report.status != "spam"
            )
        )
        recent_count = recent_result.scalar() or 0
        
        base_score = (scam_reports * 3) + (verified_reports * 5) + (recent_count * 2)
        
        if base_score == 0:
            entity.risk_status = "Insufficient Data"
        elif base_score <= 4:
            entity.risk_status = "Low Risk"
        elif base_score <= 9:
            entity.risk_status = "Medium Risk"
        else:
            entity.risk_status = "High Risk"
        
        if total_reports <= 2:
            entity.confidence_level = "Low"
        elif total_reports <= 7:
            entity.confidence_level = "Medium"
        else:
            entity.confidence_level = "High"
    
    # Log activity
    log = ActivityLog(
        user_id=current_admin.id,
        action="mark_report_spam",
        entity_id=report_id,
        extra_metadata={"entity_id": str(report.entity_id)}
    )
    db.add(log)
    
    await db.commit()
    
    return {"message": "Report marked as spam", "report_id": str(report_id)}
