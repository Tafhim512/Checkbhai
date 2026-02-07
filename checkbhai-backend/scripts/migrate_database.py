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
        print("Checking for missing columns...")
        
        # Migration 1: Add scam_reports column if missing
        try:
            await conn.execute(text("SELECT scam_reports FROM entities LIMIT 1"))
            print("✅ Column 'scam_reports' already exists")
        except Exception as e:
            if "scam_reports" in str(e):
                print("➕ Adding 'scam_reports' column...")
                await conn.execute(text("""
                    ALTER TABLE entities 
                    ADD COLUMN scam_reports INTEGER DEFAULT 0 NOT NULL
                """))
                print("✅ Added 'scam_reports' column")
            else:
                raise
        
        # Migration 2: Add verified_reports column if missing
        try:
            await conn.execute(text("SELECT verified_reports FROM entities LIMIT 1"))
            print("✅ Column 'verified_reports' already exists")
        except Exception as e:
            if "verified_reports" in str(e):
                print("➕ Adding 'verified_reports' column...")
                await conn.execute(text("""
                    ALTER TABLE entities 
                    ADD COLUMN verified_reports INTEGER DEFAULT 0 NOT NULL
                """))
                print("✅ Added 'verified_reports' column")
            else:
                raise
        
        # Migration 3: Add report_trend column if missing (optional, has default)
        try:
            await conn.execute(text("SELECT report_trend FROM entities LIMIT 1"))
            print("✅ Column 'report_trend' already exists")
        except Exception as e:
            if "report_trend" in str(e):
                print("➕ Adding 'report_trend' column...")
                await conn.execute(text("""
                    ALTER TABLE entities 
                    ADD COLUMN report_trend VARCHAR(20) DEFAULT 'Stable'
                """))
                print("✅ Added 'report_trend' column")
            else:
                raise
        
        # Migration 4: Add confidence_level column if missing
        try:
            await conn.execute(text("SELECT confidence_level FROM entities LIMIT 1"))
            print("✅ Column 'confidence_level' already exists")
        except Exception as e:
            if "confidence_level" in str(e):
                print("➕ Adding 'confidence_level' column...")
                await conn.execute(text("""
                    ALTER TABLE entities 
                    ADD COLUMN confidence_level VARCHAR(20) DEFAULT 'Low'
                """))
                print("✅ Added 'confidence_level' column")
            else:
                raise
        
        # Update existing rows to have default values
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
