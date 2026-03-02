"""
MULEX AI Backend - Simplified Launch Script (Works without PostgreSQL)
Starts the API server directly
"""

import subprocess
import sys
import os

def main():
    print("\n" + "🚀" * 35)
    print("MULEX AI BACKEND - STARTING SERVER")
    print("🚀" * 35)
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    print("\n" + "=" * 70)
    print("📊 SERVER CONFIGURATION")
    print("=" * 70)
    print(f"   • Directory: {backend_dir}")
    print(f"   • Host: 0.0.0.0")
    print(f"   • Port: 8000")
    print(f"   • Mode: Development (--reload)")
    print(f"\n🎯 ACCESS POINTS:")
    print(f"   • API Base: http://localhost:8000")
    print(f"   • API Docs (Swagger): http://localhost:8000/docs")
    print(f"   • ReDoc: http://localhost:8000/redoc")
    print(f"   • OpenAPI JSON: http://localhost:8000/openapi.json")
    print(f"\n💾 DATABASE:")
    print(f"   Note: PostgreSQL is not currently running.")
    print(f"   API server will start, but database operations will fail.")
    print(f"   To enable database features:")
    print(f"   1. Install PostgreSQL from https://www.postgresql.org/")
    print(f"   2. Create database: CREATE DATABASE mulex;")
    print(f"   3. Update .env with correct DATABASE_URL")
    print(f"   4. Re-run this script")
    print(f"\n🔧 QUICK SETUP (If you have PostgreSQL):")
    print(f"   1. Start PostgreSQL service")
    print(f"   2. Create database: psql -U postgres -c 'CREATE DATABASE mulex;'")
    print(f"   3. Run: python init_db.py")
    print(f"   4. Run: python seed_db.py")
    print(f"   5. Run: python test_models.py")
    print(f"\n" + "=" * 70)
    print(f"\n▶️  Starting FastAPI server...\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
