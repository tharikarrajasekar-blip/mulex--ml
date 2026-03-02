"""
Database initialization and connection test script
Run this before starting the server to create all tables
"""

from app.database import engine, Base
from app import models
from sqlalchemy import text
import sys

def init_db():
    """Create all database tables"""
    try:
        print("🔄 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.fetchone():
                print("✅ Database connection successful!")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure PostgreSQL is running and credentials are correct in .env file")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("MuleX AI Backend - Database Setup")
    print("=" * 50)
    
    if not test_connection():
        print("\n⚠️ Connection test failed. Check your database credentials in .env")
        sys.exit(1)
    
    if not init_db():
        print("\n⚠️ Failed to initialize database tables")
        sys.exit(1)
    
    print("\n✅ Database setup complete! Ready to start the server.")
    print("   Run: uvicorn app.main:app --reload")
