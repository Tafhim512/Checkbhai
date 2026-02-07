#!/usr/bin/env python3
"""
Database Migration Script for CheckBhai
Adds missing columns to the entities table
"""

import asyncio
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
import re


async def run_migration():
    """Run database migrations to add missing columns"""
    
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not set!")
        return False
    
    # Ensure the dialect is postgresql+asyncpg
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # Strip SSL parameters
    DATABASE_URL = re.sub(r'[?&]sslmode=[^&]*', '', DATABASE_URL)
    DATABASE_URL = re.sub(r'[?&]ssl=[^&]*', '', DATABASE_URL)
    DATABASE_URL = DATABASE_URL.rstrip('?&')
    
    print(f"Connecting to database...")
    
    # Create engine without SSL context for migration
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        pool_pre_ping=True,
        connect_args={
            "statement_cache_size": 0,
            "command_timeout": 60,
        }
    )
    
    async with engine.begin() as conn:
        print("Checking/Updating entities table...")
        
        # Migration 1: scam_reports
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS scam_reports INTEGER DEFAULT 0 NOT NULL"))
            print("✅ Column 'scam_reports' ready")
        except Exception as e:
            print(f"⚠️ Error with 'scam_reports': {e}")
        
        # Migration 2: verified_reports
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS verified_reports INTEGER DEFAULT 0 NOT NULL"))
            print("✅ Column 'verified_reports' ready")
        except Exception as e:
            print(f"⚠️ Error with 'verified_reports': {e}")
        
        # Migration 3: report_trend
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS report_trend VARCHAR(20) DEFAULT 'Stable'"))
            print("✅ Column 'report_trend' ready")
        except Exception as e:
            print(f"⚠️ Error with 'report_trend': {e}")
        
        # Migration 4: confidence_level
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS confidence_level VARCHAR(20) DEFAULT 'Low'"))
            print("✅ Column 'confidence_level' ready")
        except Exception as e:
            print(f"⚠️ Error with 'confidence_level': {e}")

        # Migration 5: risk_status
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS risk_status VARCHAR(30) DEFAULT 'Insufficient Data'"))
            print("✅ Column 'risk_status' ready")
        except Exception as e:
            print(f"⚠️ Error with 'risk_status': {e}")

        # Migration 6: last_reported_date
        try:
            await conn.execute(text("ALTER TABLE entities ADD COLUMN IF NOT EXISTS last_reported_date TIMESTAMP WITHOUT TIME ZONE"))
            print("✅ Column 'last_reported_date' ready")
        except Exception as e:
            print(f"⚠️ Error with 'last_reported_date': {e}")
            
        # Update existing rows to have default values (Safe updates)
        print("\nUpdating existing records...")
        await conn.execute(text("""
            UPDATE entities 
            SET scam_reports = 0 
            WHERE scam_reports IS NULL
        """))
        await conn.execute(text("""
            UPDATE entities 
            SET verified_reports = 0 
            WHERE verified_reports IS NULL
        """))
        
        print("\n✅ Migration completed successfully!")
    
    await engine.dispose()
    return True


if __name__ == "__main__":
    success = asyncio.run(run_migration())
    sys.exit(0 if success else 1)
