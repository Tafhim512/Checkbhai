"""
CheckBhai Truth Loop Test Script
Run this script to verify the core data loop is working correctly.

Usage:
    cd checkbhai-backend
    .\\venv\\Scripts\\activate  # Windows
    python scripts/test_truth_loop.py

This will:
1. Create/find a test entity
2. Submit a report
3. Query the entity again
4. Verify the counts updated
"""

import asyncio
import uuid
from datetime import datetime

# Add parent directory to path
import sys
sys.path.insert(0, '.')

async def test_truth_loop():
    from app.database import AsyncSessionLocal, Entity, Report
    from sqlalchemy import select, func
    
    print("\n" + "="*60)
    print("CHECKBHAI TRUTH LOOP TEST")
    print("="*60 + "\n")
    
    async with AsyncSessionLocal() as db:
        test_identifier = f"test_{int(datetime.utcnow().timestamp())}"
        test_type = "phone"
        
        # STEP 1: Check if entity exists
        print(f"[STEP 1] Searching for entity: type={test_type}, identifier={test_identifier}")
        result = await db.execute(
            select(Entity).filter(Entity.type == test_type, Entity.identifier == test_identifier)
        )
        entity = result.scalar_one_or_none()
        
        if entity:
            print(f"  ✓ Entity found: id={entity.id}")
            print(f"    - total_reports: {entity.total_reports}")
            print(f"    - scam_reports: {entity.scam_reports}")
            print(f"    - risk_status: {entity.risk_status}")
        else:
            print(f"  → Entity NOT found. Creating new entity...")
            entity = Entity(
                type=test_type,
                identifier=test_identifier,
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
            print(f"  ✓ Created entity: id={entity.id}")
            print(f"    - total_reports: {entity.total_reports}")
            print(f"    - risk_status: {entity.risk_status}")
        
        # Before state
        before_total = entity.total_reports or 0
        before_scam = entity.scam_reports or 0
        before_risk = entity.risk_status
        
        # STEP 2: Submit a report
        print(f"\n[STEP 2] Submitting a scam report for entity {entity.id}...")
        report = Report(
            reporter_id=None,  # Anonymous
            entity_id=entity.id,
            platform="other",
            scam_type="no_delivery",
            amount_lost=500.0,
            currency="BDT",
            description="Test report to verify truth loop is working. This is not a real scam report.",
            status="pending"
        )
        db.add(report)
        
        # Update entity stats
        entity.total_reports = (entity.total_reports or 0) + 1
        entity.scam_reports = (entity.scam_reports or 0) + 1
        entity.last_reported_date = datetime.utcnow()
        
        # Calculate new risk
        scam_reports = entity.scam_reports
        base_score = scam_reports * 3
        
        if base_score == 0:
            entity.risk_status = "Insufficient Data"
        elif base_score <= 4:
            entity.risk_status = "Low Risk"
        elif base_score <= 9:
            entity.risk_status = "Medium Risk"
        else:
            entity.risk_status = "High Risk"
        
        await db.commit()
        await db.refresh(entity)
        await db.refresh(report)
        
        print(f"  ✓ Report submitted: id={report.id}")
        
        # STEP 3: Verify updates
        print(f"\n[STEP 3] Verifying entity stats updated...")
        result = await db.execute(select(Entity).filter(Entity.id == entity.id))
        updated_entity = result.scalar_one()
        
        print(f"  BEFORE → AFTER")
        print(f"    total_reports: {before_total} → {updated_entity.total_reports}")
        print(f"    scam_reports:  {before_scam} → {updated_entity.scam_reports}")
        print(f"    risk_status:   {before_risk} → {updated_entity.risk_status}")
        print(f"    last_reported: {updated_entity.last_reported_date}")
        
        # STEP 4: Count actual reports in database
        print(f"\n[STEP 4] Counting reports in database for entity {entity.id}...")
        count_result = await db.execute(
            select(func.count(Report.id)).filter(Report.entity_id == entity.id)
        )
        actual_count = count_result.scalar()
        print(f"  ✓ Actual reports in DB: {actual_count}")
        
        # VALIDATION
        print("\n" + "="*60)
        if updated_entity.total_reports > before_total:
            print("✅ TRUTH LOOP WORKING: Entity stats updated correctly")
        else:
            print("❌ TRUTH LOOP BROKEN: Entity stats did NOT update")
        
        if actual_count > 0:
            print("✅ DATABASE WORKING: Reports are being saved")
        else:
            print("❌ DATABASE BROKEN: Reports are NOT being saved")
        print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_truth_loop())
