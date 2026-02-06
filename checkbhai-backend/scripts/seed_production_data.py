
import asyncio
import sys
import os
import uuid
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, '.')

from app.database import engine, Base, User, Entity, Report, Message
from app.auth import hash_password
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

# Database session
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def seed_data():
    print("🌱 Starting Production Data Seed...")
    
    async with AsyncSessionLocal() as db:
        # 1. Ensure Admin User
        print("-> Checking Admin User...")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@checkbhai.com")
        result = await db.execute(select(User).filter(User.email == admin_email))
        admin = result.scalars().first()
        
        if not admin:
            print(f"Creating admin user: {admin_email}")
            admin = User(
                email=admin_email,
                password_hash=hash_password(os.getenv("ADMIN_PASSWORD", "admin123")),
                is_admin=True,
                reputation_score=100
            )
            db.add(admin)
            await db.commit()
            await db.refresh(admin)
        else:
            print("Admin user exists.")

        # 2. Seed Entities (Scammers & Safe)
        print("-> Seeding Entities...")
        
        # High Risk Scammer (Bkash Agent)
        result = await db.execute(select(Entity).filter(Entity.identifier == "01812345678"))
        scammer = result.scalars().first()
        if not scammer:
            scammer = Entity(
                type="agent",
                identifier="01812345678",
                risk_status="High Risk",
                confidence_level="High",
                total_reports=15,
                scam_reports=14,
                verified_reports=10,
                last_checked=datetime.utcnow()
            )
            db.add(scammer)
        
        # Fake Shop (Facebook)
        result = await db.execute(select(Entity).filter(Entity.identifier == "facebook.com/fake-shop-bd"))
        fake_shop = result.scalars().first()
        if not fake_shop:
            fake_shop = Entity(
                type="fb_page",
                identifier="facebook.com/fake-shop-bd",
                risk_status="Medium Risk",
                confidence_level="Medium",
                total_reports=5,
                scam_reports=5,
                verified_reports=2,
                last_checked=datetime.utcnow()
            )
            db.add(fake_shop)

        # Safe Number
        result = await db.execute(select(Entity).filter(Entity.identifier == "01700000000"))
        safe_guy = result.scalars().first()
        if not safe_guy:
            safe_guy = Entity(
                type="phone",
                identifier="01700000000",
                risk_status="Safe",
                confidence_level="High",
                total_reports=0,
                scam_reports=0,
                verified_reports=0,
                last_checked=datetime.utcnow()
            )
            db.add(safe_guy)
            
        await db.commit()

        # 3. Seed Reports (For the Scammer)
        print("-> Seeding Reports...")
        # Need to re-fetch to get IDs if just added
        await db.refresh(scammer)
        await db.refresh(fake_shop)

        # Add 3 reports for the scammer
        descriptions = [
            "He asked for advance payment via bKash and then blocked me.",
            "Fake agent, said my account was locked. Stole 5000tk.",
            "Total fraud, do not trust this number."
        ]
        
        for desc in descriptions:
            # Check if similar report exists to avoid duplicates on re-run
            # Simplified check
            exists = await db.execute(select(Report).filter(Report.entity_id == scammer.id, Report.description == desc))
            if not exists.scalars().first():
                report = Report(
                    entity_id=scammer.id,
                    platform="agent",
                    scam_type="advance_taken",
                    amount_lost=random.randint(500, 5000),
                    currency="BDT",
                    description=desc,
                    status="verified",
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(report)

        # Add 1 report for fake shop
        exists = await db.execute(select(Report).filter(Report.entity_id == fake_shop.id))
        if not exists.scalars().first():
            report = Report(
                entity_id=fake_shop.id,
                platform="facebook",
                scam_type="fake_product",
                amount_lost=1200,
                currency="BDT",
                description="Ordered a watch, received a potato. Page blocked me.",
                status="pending",
                created_at=datetime.utcnow() - timedelta(days=2)
            )
            db.add(report)

        await db.commit()
        
        # 4. Seed History (For Admin User)
        print("-> Seeding History (for Admin)...")
        # Add some messages checked by admin
        msgs = [
            "You won a lottery! Call 01812345678 to claim.",
            "Is 01700000000 a safe number?",
            "Urgent: Send money to 01812345678 immediately."
        ]
        
        for txt in msgs:
            exists = await db.execute(select(Message).filter(Message.user_id == admin.id, Message.message_text == txt))
            if not exists.scalars().first():
                msg = Message(
                    user_id=admin.id,
                    message_text=txt,
                    risk_level="High" if "01812345678" in txt else "Low",
                    confidence=0.9 if "01812345678" in txt else 0.95,
                    red_flags=["suspicious_number"] if "01812345678" in txt else [],
                    created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                )
                db.add(msg)
        
        await db.commit()

    print("✅ Seed Complete! You can now verify the dashboard.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_data())
