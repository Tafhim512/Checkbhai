"""
Claims Router - Handle Business Profile Claims
Compliant with Core Principle #5: Business Claim & Response System
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
import logging

from app.database import get_db, Entity, EntityClaim
from app.models import EntityClaimCreate, EntityClaimResponse

# Setup logging
logger = logging.getLogger("checkbhai.claims")

router = APIRouter(prefix="/claims", tags=["claims"])

@router.post("/", response_model=EntityClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_data: EntityClaimCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a request to claim a business profile/entity.
    This does NOT remove reports. It starts a transparency process.
    """
    # 1. Verify Entity Exists
    result = await db.execute(select(Entity).filter(Entity.id == claim_data.entity_id))
    entity = result.scalar_one_or_none()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    # 2. Check for existing pending claims for this entity to prevent spam
    result = await db.execute(
        select(EntityClaim).filter(
            EntityClaim.entity_id == claim_data.entity_id,
            EntityClaim.status == "pending"
        )
    )
    existing_claim = result.scalars().first()
    if existing_claim:
        raise HTTPException(
            status_code=400, 
            detail="A claim request is already pending for this entity."
        )

    # 3. Create Claim
    new_claim = EntityClaim(
        entity_id=claim_data.entity_id,
        contact_email=claim_data.contact_email,
        business_name=claim_data.business_name,
        verification_doc_url=claim_data.verification_doc_url,
        message=claim_data.message
    )
    
    db.add(new_claim)
    await db.commit()
    await db.refresh(new_claim)
    
    logger.info(f"New Claim Submitted: {new_claim.id} for Entity {entity.identifier}")
    
    return new_claim

@router.get("/{claim_id}", response_model=EntityClaimResponse)
async def get_claim_status(
    claim_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Check the status of a claim request"""
    result = await db.execute(select(EntityClaim).filter(EntityClaim.id == claim_id))
    claim = result.scalar_one_or_none()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
        
    return claim
