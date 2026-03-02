"""
Quick Start Guide for MULEX AI Backend
Complete instructions for database setup, seeding, testing, and deployment
"""

# ════════════════════════════════════════════════════════════════════════════════
# MULEX AI BACKEND - QUICK START GUIDE
# ════════════════════════════════════════════════════════════════════════════════

## 📋 PREREQUISITES

Before starting, ensure you have:
- Python 3.8+ installed
- PostgreSQL running and accessible
- All Python packages installed (pip install -r requirements.txt)
- .env file configured with database credentials

## 🚀 QUICK START (3 Steps)

### OPTION 1: ONE-COMMAND SETUP & RUN (Recommended)

cd c:\Users\thari\Downloads\MULEX.ML\backend
python run_all.py

This single command will:
✅ Initialize database (create tables)
✅ Seed with sample data (5 users, 5 accounts, 50+ records)
✅ Run model tests (fraud, trust, aml detection)
✅ Start the API server (http://localhost:8000)

### OPTION 2: STEP-BY-STEP SETUP

Step 1️⃣ - Initialize Database
python init_db.py
Expected output: "✅ Database setup complete!"

Step 2️⃣ - Seed Sample Data
python seed_db.py
Expected output: "✅ DATABASE SEEDING COMPLETE!"

Step 3️⃣ - Test Models
python test_models.py
Expected output: "✅ ALL MODEL TESTS COMPLETED SUCCESSFULLY!"

Step 4️⃣ - Run Server
python -m uvicorn app.main:app --reload
Server will start at: http://localhost:8000

## 📊 SAMPLE DATA CREATED

The seeding script creates:

Users:
  • admin@mulex.ai (ADMIN role)
  • investigator@mulex.ai (INVESTIGATOR role)
  • user1@email.com (USER role)
  • user2@email.com (USER role)

Accounts:
  • ACC-1001-XK through ACC-7007-MM (5 accounts)

For Each Account:
  • 5-10 transactions (various amounts)
  • 2-4 risk alerts
  • KYC verification records
  • AML detection scans
  • Biometric profiles
  • Authentication attempts

## 🤖 AI/ML MODELS TESTED

✅ Fraud Detection Model
   - Predicts fraud probability (0-100%)
   - Uses 6 features: amount, velocity, location, device, time, network
   - Provides SHAP explanations for decisions
   - XGBoost-style classification

✅ Trust Scoring Engine
   - Composite trust score (0-100)
   - 5 components: identity, auth, transaction, network, behavior
   - Weighted formula: 0.2·I + 0.2·A + 0.25·T + 0.2·N + 0.15·B
   - Decision: APPROVE / STEP-UP AUTH / BLOCK

✅ AML Pattern Detection
   - Detects 5 money laundering patterns
   - Layering (multiple short-time transactions)
   - Structuring (amounts below thresholds)
   - Smurfing (many small transactions)
   - Dispersion (multiple recipients)
   - Circular (circular transactions)
   - Auto-generates STR (Suspicious Transaction Report)

## 🔌 API ENDPOINTS

### Authentication
POST /token
  Login and get access token
  
### Dashboard
GET /dashboard/metrics
  Get KPI metrics (transactions, alerts, trust score)
  
GET /dashboard/alerts
  Get list of recent alerts

### AI/ML Predictions
POST /api/fraud/predict
  Predict fraud probability

POST /api/trust/score
  Calculate trust score

POST /api/aml/detect
  Detect AML patterns

POST /api/kyc/verify
  KYC verification

POST /api/auth/attempt
  Create authentication attempt

POST /api/biometrics/analyze
  Analyze behavioral biometrics

GET /api/explain/{alert_id}
  Get SHAP explanations

### WebSocket
WS /ws/feed
  Live transaction stream

## 🔍 TESTING THE API

### Test Login
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@mulex.ai&password=secured"

### Get Metrics
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/dashboard/metrics

### Test Fraud Prediction
curl -X POST "http://localhost:8000/api/fraud/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 150000,
    "velocity_score": 85,
    "location_risk": 70,
    "device_risk": 60,
    "time_anomaly": 75,
    "network_risk": 65
  }'

### Interactive API Documentation
Visit: http://localhost:8000/docs
(Swagger UI - Try Out All APIs Here!)

## 📁 PROJECT STRUCTURE

backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI server with routes
│   ├── database.py       # PostgreSQL connection
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── crud.py           # Database CRUD operations
│   ├── ml_models.py      # AI/ML models (Fraud, Trust, AML)
│   ├── routes.py         # API route handlers
│   ├── config.py         # Environment configuration
│   └── trained_models/   # Saved ML models
├── init_db.py            # Database initialization
├── seed_db.py            # Sample data seeding
├── test_models.py        # Model testing script
├── run_all.py            # Complete setup & launch
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── DATABASE_SETUP.md     # Database configuration guide

## 🐛 TROUBLESHOOTING

### "Connection refused" error
Problem: Cannot connect to PostgreSQL
Solution:
  1. Ensure PostgreSQL is running
  2. Check DATABASE_URL in .env
  3. Verify username/password
  4. Ensure database exists

### "Address already in use" error
Problem: Port 8000 is already in use
Solution:
  python -m uvicorn app.main:app --port 8001

### "Import errors"
Problem: Missing Python packages
Solution:
  pip install -r requirements.txt

### "Authentication failed"
Problem: Token/credentials issue
Solution:
  Use credentials from seed_db.py:
    username: admin@mulex.ai
    password: secured

## 📈 NEXT STEPS

1. ✅ Run the setup: python run_all.py
2. ✅ Access the API docs: http://localhost:8000/docs
3. ✅ Try out the endpoints with sample data
4. ✅ Connect the frontend to the backend
5. ✅ Integrate real ML models as needed
6. ✅ Deploy to production

## 🔗 FRONTEND INTEGRATION

Frontend should connect to:
- API Base: http://localhost:8000
- Login: POST /token
- Metrics: GET /dashboard/metrics
- Predictions: POST /api/{fraud|trust|aml|kyc}/...
- WebSocket: ws://localhost:8000/ws/feed

## 📞 SUPPORT

For issues or questions:
1. Check logs in the terminal
2. Review DATABASE_SETUP.md
3. Check .env configuration
4. Verify PostgreSQL is running

## 📝 DATABASE SCHEMA

Tables Created:
- users (authentication & profiles)
- accounts (trading/business accounts)
- transactions (payment records)
- alerts (risk alerts & notifications)
- kyc_records (identity verification)
- aml_scans (money laundering detection)
- biometric_profiles (behavioral analysis)
- authentication_attempts (login security)
- ml_models (trained models registry)

## ✨ KEY FEATURES

✅ Real-time risk detection
✅ Multi-factor authentication
✅ Explainable AI (SHAP)
✅ AML/KYC compliance
✅ Behavioral biometrics
✅ WebSocket live feeds
✅ PostgreSQL persistence
✅ RESTful API with FastAPI
✅ Pydantic validation
✅ SQLAlchemy ORM
✅ JWT authentication
✅ CORS enabled

═══════════════════════════════════════════════════════════════════════════════
Ready to go! Run: python run_all.py
═══════════════════════════════════════════════════════════════════════════════
