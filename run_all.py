"""
Complete Backend Setup & Launch Script
Handles database initialization, seeding, model testing, and server startup
"""

import subprocess
import sys
import time
import os

def print_section(title):
    """Print formatted section"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n▶️  {description}...")
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🎯" * 35)
    print("MULEX AI BACKEND - COMPLETE SETUP & RUN")
    print("🎯" * 35)
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Step 1: Initialize Database
    print_section("STEP 1: DATABASE INITIALIZATION")
    print("Creating PostgreSQL tables and schema...")
    if not run_command([sys.executable, "init_db.py"], "Database initialization"):
        print("⚠️  Database initialization may have issues. Continuing anyway...")
    
    time.sleep(2)
    
    # Step 2: Seed Database
    print_section("STEP 2: DATABASE SEEDING")
    print("Populating database with sample data for testing...")
    if not run_command([sys.executable, "seed_db.py"], "Database seeding"):
        print("⚠️  Seeding failed. Database may be empty.")
    
    time.sleep(2)
    
    # Step 3: Test Models
    print_section("STEP 3: MODEL TESTING")
    print("Running AI/ML models with sample and real database data...")
    if not run_command([sys.executable, "test_models.py"], "Model testing"):
        print("⚠️  Model tests failed. Check configurations.")
    
    time.sleep(2)
    
    # Step 4: Start Server
    print_section("STEP 4: STARTING FASTAPI SERVER")
    print("Launching uvicorn server...")
    print("\n📊 Server Configuration:")
    print("   • Host: 0.0.0.0")
    print("   • Port: 8000")
    print("   • Mode: Development (--reload)")
    print("\n🎯 Access Points:")
    print("   • API Base: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print("   • WebSocket: ws://localhost:8000/ws/feed")
    print("\n💡 Tips:")
    print("   • Press Ctrl+C to stop the server")
    print("   • The server auto-reloads on code changes")
    print("   • Check logs above for any connection issues")
    print("\n" + "=" * 70 + "\n")
    
    # Start the server
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
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
