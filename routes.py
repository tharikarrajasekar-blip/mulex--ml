"""
Additional API route handlers for AI/ML endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal
from .ml_models import fraud_detector, trust_engine, aml_detector
from datetime import datetime

router = APIRouter(prefix="/api", tags=["AI/ML Endpoints"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str | None = None, db: Session = Depends(get_db)):
    """Placeholder for token validation"""
    return {"username": "demo_user"}


# ─── FRAUD DETECTION ───
@router.post("/fraud/predict", response_model=schemas.FraudPredictionResponse)
def predict_fraud(
    request: schemas.FraudPredictionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Predict fraud probability for a transaction"""
    result = fraud_detector.predict(
        request.amount,
        request.velocity_score,
        request.location_risk,
        request.device_risk,
        request.time_anomaly,
        request.network_risk
    )
    
    explanation = fraud_detector.get_shap_explanation(
        request.amount,
        request.velocity_score,
        request.location_risk,
        request.device_risk,
        request.time_anomaly,
        request.network_risk
    )
    
    return schemas.FraudPredictionResponse(
        fraud_probability=result["fraud_probability"],
        decision=result["decision"],
        confidence=result["confidence"],
        explanation=explanation
    )


# ─── TRUST SCORING ───
@router.post("/trust/score", response_model=schemas.TrustScoreResponse)
def calculate_trust_score(
    request: schemas.TrustScoreRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Calculate composite trust score"""
    result = trust_engine.calculate_score(
        request.identity_risk,
        request.auth_risk,
        request.transaction_risk,
        request.network_risk,
        request.behavior_risk
    )
    
    return schemas.TrustScoreResponse(
        trust_score=result["trust_score"],
        decision=result["decision"],
        components=result["components"]
    )


@router.post("/trust/explain")
def explain_trust_score(
    request: schemas.TrustScoreRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get detailed explanation of trust score calculation"""
    return trust_engine.get_explanation(
        request.identity_risk,
        request.auth_risk,
        request.transaction_risk,
        request.network_risk,
        request.behavior_risk
    )


# ─── AML DETECTION ───
@router.post("/aml/detect", response_model=schemas.AMLDetectionResponse)
def detect_aml_patterns(
    request: schemas.AMLDetectionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Detect AML patterns in transaction history"""
    result = aml_detector.detect_patterns(request.transaction_history)
    
    # Store in database
    aml_scan = crud.create_aml_scan(db, request.account_id)
    
    updates = {
        "layering_detected": result["layering_score"] > 50,
        "structuring_detected": result["structuring_score"] > 50,
        "smurfing_detected": result["smurfing_score"] > 50,
        "dispersion_detected": result["dispersion_score"] > 50,
        "circular_detected": result["circular_score"] > 50,
        "str_generated": result["overall_risk"] in ["HIGH", "CRITICAL"]
    }
    
    crud.update_aml_scan(db, request.account_id, updates)
    
    # Create alert if high risk
    if result["overall_risk"] in ["HIGH", "CRITICAL"]:
        sev = "HIGH" if result["overall_risk"] == "HIGH" else "CRITICAL"
        alert = crud.create_alert(
            db,
            schemas.AlertCreate(
                account_id=request.account_id,
                risk_score=75 if result["overall_risk"] == "HIGH" else 95,
                type="AML_DETECTION",
                status="OPEN",
                description=f"AML pattern detected: {result['overall_risk']}",
                severity=sev
            )
        )
    
    return schemas.AMLDetectionResponse(
        **result,
        str_generated=updates["str_generated"]
    )


# ─── KYC VERIFICATION ───
@router.post("/kyc/verify")
def verify_kyc(
    account_id: str,
    document_type: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Initiate KYC verification process"""
    kyc = crud.create_kyc_record(db, account_id, document_type)
    
    # Simulate ML verification (in real scenario, integrate actual ML model)
    updates = {
        "ocr_extracted": True,
        "tamper_detected": False,
        "synthetic_identity": False,
        "consent_validated": True,
        "overall_score": 92.0,
        "verdict": "APPROVED"
    }
    
    kyc = crud.update_kyc_record(db, account_id, updates)
    
    # Update account KYC status
    account = crud.get_account(db, account_id)
    if account:
        account.kyc_verified = True  # type: ignore
        db.commit()
    
    if not kyc:
        raise HTTPException(status_code=500, detail="Failed to update KYC record")
    
    return {
        "status": "success",
        "kyc_id": kyc.id,
        "verdict": kyc.verdict,
        "score": kyc.overall_score
    }


# ─── AUTHENTICATION ───
@router.post("/auth/attempt")
def create_auth_attempt(
    account_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create authentication attempt record"""
    attempt = crud.create_auth_attempt(db, account_id)
    return {
        "attempt_id": attempt.id,
        "account_id": attempt.account_id,
        "timestamp": attempt.timestamp
    }


@router.put("/auth/attempt/{attempt_id}")
def update_auth_attempt(
    attempt_id: int,
    face_verified: bool = False,
    liveness_confirmed: bool = False,
    voice_verified: bool = False,
    deepfake_detected: bool = False,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update authentication attempt with verification results"""
    overall_success = face_verified and liveness_confirmed and voice_verified and not deepfake_detected
    
    attempt = crud.update_auth_attempt(
        db,
        attempt_id,
        {
            "face_verified": face_verified,
            "liveness_confirmed": liveness_confirmed,
            "voice_verified": voice_verified,
            "deepfake_detected": deepfake_detected,
            "overall_success": overall_success
        }
    )
    
    if attempt and deepfake_detected:
        # Create alert for deepfake detection
        acct_id = str(attempt.account_id) if attempt.account_id else ""  # type: ignore
        crud.create_alert(
            db,
            schemas.AlertCreate(
                account_id=acct_id,
                risk_score=95,
                type="DEEPFAKE_DETECTED",
                status="OPEN",
                severity="CRITICAL"
            )
        )
    
    return {
        "attempt_id": attempt.id if attempt else None,
        "overall_success": overall_success,
        "deepfake_detected": deepfake_detected
    }


# ─── BIOMETRICS ───
@router.post("/biometrics/analyze")
def analyze_biometrics(
    account_id: str,
    typing_velocity: float,
    mouse_velocity: float,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Analyze behavioral biometrics"""
    profile = crud.get_biometric_profile(db, account_id)
    if not profile:
        profile = crud.create_biometric_profile(db, account_id)
    
    # Simple anomaly detection
    anomaly_score = 0
    if typing_velocity > 120:  # Extremely fast
        anomaly_score += 30
    if mouse_velocity > 1500:  # Extremely fast mouse
        anomaly_score += 30
    
    # Update profile
    profile.typing_velocity_avg = typing_velocity  # type: ignore
    profile.mouse_velocity_avg = mouse_velocity  # type: ignore
    profile.anomaly_score = min(anomaly_score, 100)  # type: ignore
    db.commit()
    
    return {
        "account_id": account_id,
        "typing_velocity": typing_velocity,
        "mouse_velocity": mouse_velocity,
        "anomaly_score": profile.anomaly_score,
        "anomaly_detected": anomaly_score > 50
    }


# ─── EXPLAINABLE AI (SHAP) ───
@router.get("/explain/{alert_id}")
def get_shap_explanation(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get SHAP explanation for an alert/decision"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Return generic explanation (in production, compute real SHAP values)
    return {
        "alert_id": alert_id,
        "type": alert.type,
        "risk_score": alert.risk_score,
        "explanation": {
            "top_factors": [
                {"factor": "Transaction Amount", "impact": 0.35},
                {"factor": "Transaction Velocity", "impact": 0.28},
                {"factor": "Location Risk", "impact": 0.18},
                {"factor": "Device Risk", "impact": 0.12},
                {"factor": "Network Anomaly", "impact": 0.07}
            ],
            "model": "XGBoost v4.2",
            "confidence": 0.95
        }
    }
