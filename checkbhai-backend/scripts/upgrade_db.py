"""
CheckBhai Database Upgrade Script
SAFE MIGRATION: adds new columns if they are missing.
"""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, '.')

from app.database import engine
from sqlalchemy import text

async def upgrade_db():
    print("CheckBhai Schema Upgrade (Safe Mode)")
    print("-----------------------------------")
    
    async with engine.begin() as conn:
        print("Checking tables...")
        
        # 1. Upgrade entities table
        print("-> Checking 'entities' table...")
        
        # Add risk_status
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS risk_status VARCHAR(30) DEFAULT 'Insufficient Data'"))
            print("   ✓ risk_status column ready")
        except Exception as e:
            print(f"   ! Error checking risk_status: {e}")

        # Add confidence_level
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS confidence_level VARCHAR(20) DEFAULT 'Low'"))
            print("   ✓ confidence_level column ready")
        except Exception as e:
            print(f"   ! Error checking confidence_level: {e}")

        # Add scam_reports
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS scam_reports INTEGER DEFAULT 0"))
            print("   ✓ scam_reports column ready")
        except Exception as e:
            print(f"   ! Error checking scam_reports: {e}")

        # Add verified_reports
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS verified_reports INTEGER DEFAULT 0"))
            print("   ✓ verified_reports column ready")
        except Exception as e:
            print(f"   ! Error checking verified_reports: {e}")

        # Add last_reported_date
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS last_reported_date TIMESTAMP WITHOUT TIME ZONE"))
            print("   ✓ last_reported_date column ready")
        except Exception as e:
            print(f"   ! Error checking last_reported_date: {e}")

        # 2. Upgrade reports table
        print("-> Checking 'reports' table...")
        try:
            await conn.execute(text("ALTER TABLE reports ADD COLUMN IF NOT EXISTS platform VARCHAR(50) DEFAULT 'other'"))
            print("   ✓ platform column ready")
        except Exception as e:
            print(f"   ! Error checking platform: {e}")

        # 3. Upgrade messages table
        print("-> Checking 'messages' table...")
        try:
            await conn.execute(text("ALTER TABLE messages ADD COLUMN IF NOT EXISTS fingerprint VARCHAR(64)"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_messages_fingerprint ON messages (fingerprint)"))
            print("   ✓ fingerprint column and index ready")
        except Exception as e:
            print(f"   ! Error checking fingerprint: {e}")
            
    print("\nDatabase upgrade complete! Ready for launch.")

if __name__ == "__main__":
    asyncio.run(upgrade_db())
