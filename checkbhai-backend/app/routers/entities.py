"""
CheckBhai Entity Router - Logic for checking and fetching entity risk
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import uuid
from datetime import datetime

from app.database import Entity, Message, Report, get_db
from app.models import EntityCheck, EntityResponse
from app.auth import get_current_user_optional

router = APIRouter(prefix="/entities", tags=["entities"])

@router.get("/check", response_model=EntityResponse)
async def check_entity(
    type: str = Query(..., pattern="^(phone|fb_page|fb_profile|website|bkash|nagad|rocket)$"),
    identifier: str = Query(..., min_length=3),
    db: AsyncSession = Depends(get_db)
):
    """
    Check an entity's risk level and history
    If entity doesn't exist, create a baseline record
    """
    # Clean identifier (remove spaces, etc.)
    identifier = identifier.strip().lower()
    
    # Check if entity exists
    result = await db.execute(
        select(Entity).filter(Entity.type == type, Entity.identifier == identifier)
    )
    entity = result.scalar_one_or_none()
    
    if not entity:
        # Create new entity record
        entity = Entity(
            type=type,
            identifier=identifier,
            risk_score=0,
            trust_level="Low", # New entities start as Unverified/Low trust
            scam_probability=0.0,
            extra_metadata={}
        )
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
    
    # Update last checked
    entity.last_checked = datetime.utcnow()
    await db.commit()
    
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

@router.get("/{entity_id}/reports")
async def get_entity_reports(
    entity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get all reports linked to an entity"""
    result = await db.execute(
        select(Report).filter(Report.entity_id == entity_id).order_by(Report.created_at.desc())
    )
    reports = result.scalars().all()
    return reports
