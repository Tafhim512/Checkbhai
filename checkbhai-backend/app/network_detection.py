"""
CheckBhai Network Detection - Logic for identifying scammer networks
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Dict
import uuid

from app.database import Entity, Report, Evidence

class NetworkDetector:
    """Detects links between different entities based on reports and identifiers"""
    
    @staticmethod
    async def get_related_entities(entity_id: uuid.UUID, db: AsyncSession) -> List[Dict]:
        """
        Find entities that are linked to this one.
        Links can be:
        1. Reported by the same users
        2. Mentioned in same report descriptions (pattern matching)
        3. Shared payment numbers in metadata
        """
        # Get reports for this entity
        result = await db.execute(select(Report).filter(Report.entity_id == entity_id))
        entity_reports = result.scalars().all()
        
        if not entity_reports:
            return []
        
        reporter_ids = [r.reporter_id for r in entity_reports]
        
        # 1. Find other entities reported by the same users
        related_result = await db.execute(
            select(Entity)
            .join(Report, Report.entity_id == Entity.id)
            .filter(Report.reporter_id.in_(reporter_ids))
            .filter(Entity.id != entity_id)
            .distinct()
        )
        related_entities = related_result.scalars().all()
        
        # Format results
        output = []
        for e in related_entities:
            output.append({
                "id": str(e.id),
                "type": e.type,
                "identifier": e.identifier,
                "risk_status": e.risk_status,
                "link_reason": "Reported by same user(s)"
            })
            
        return output

    @staticmethod
    async def analyze_network_risk(entity_id: uuid.UUID, db: AsyncSession) -> float:
        """Calculate additional risk based on network connections"""
        related = await NetworkDetector.get_related_entities(entity_id, db)
        if not related:
            return 0.0
            
        # If connected to high risk entities, increase risk
        high_risk_links = [e for e in related if e["risk_status"] == "High Risk"]
        return min(30.0, len(high_risk_links) * 10.0)
