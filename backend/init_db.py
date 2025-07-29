#!/usr/bin/env python3
"""
Database initialization script for RedditHarbor UI.
Creates all necessary tables in PostgreSQL.
"""

import os
from dotenv import load_dotenv
from database import engine, Base
from models import User, SearchJob, Submission, Comment

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database by creating all tables."""
    print("🗄️  Initializing database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'search_jobs', 'submissions', 'comments']
        created_tables = [table for table in expected_tables if table in tables]
        
        print(f"📋 Created tables: {', '.join(created_tables)}")
        
        if len(created_tables) == len(expected_tables):
            print("✅ All expected tables were created!")
        else:
            missing = set(expected_tables) - set(created_tables)
            print(f"⚠️  Missing tables: {', '.join(missing)}")
            
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_database() 