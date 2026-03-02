from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="ADMIN")
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trust_score = Column(Float, default=50.0)
    kyc_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"), index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    status = Column(String, default="PENDING")
    fraud_probability = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    source_ip = Column(String, nullable=True)
    device_id = Column(String, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"), index=True)
    risk_score = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # FRAUD, AML, DEEPFAKE, KYC, etc
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    status = Column(String, default="OPEN")  # OPEN, UNDER_REVIEW, RESOLVED, BLOCKED
    severity = Column(String)  # LOW, MEDIUM, HIGH, CRITICAL


class KYCRecord(Base):
    __tablename__ = "kyc_records"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"), unique=True)
    document_type = Column(String)  # AADHAR, PAN, PASSPORT, DL
    document_path = Column(String, nullable=True)
    ocr_extracted = Column(Boolean, default=False)
    tamper_detected = Column(Boolean, default=False)
    synthetic_identity = Column(Boolean, default=False)
    consent_validated = Column(Boolean, default=False)
    overall_score = Column(Float)  # 0-100
    verdict = Column(String)  # APPROVED, REJECTED, PENDING
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class AMLScan(Base):
    __tablename__ = "aml_scans"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"), index=True)
    layering_detected = Column(Boolean, default=False)
    structuring_detected = Column(Boolean, default=False)
    smurfing_detected = Column(Boolean, default=False)
    dispersion_detected = Column(Boolean, default=False)
    circular_detected = Column(Boolean, default=False)
    str_generated = Column(Boolean, default=False)
    str_path = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class BiometricProfile(Base):
    __tablename__ = "biometric_profiles"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"), unique=True)
    typing_velocity_avg = Column(Float)  # WPM
    mouse_velocity_avg = Column(Float)  # px/s
    click_pressure_pattern = Column(String, nullable=True)
    keystroke_timing = Column(JSON, nullable=True)
    anomaly_score = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class AuthenticationAttempt(Base):
    __tablename__ = "authentication_attempts"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"), index=True)
    face_verified = Column(Boolean, default=False)
    liveness_confirmed = Column(Boolean, default=False)
    voice_verified = Column(Boolean, default=False)
    deepfake_detected = Column(Boolean, default=False)
    overall_success = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    ip_address = Column(String, nullable=True)


class MLModel(Base):
    __tablename__ = "ml_models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # fraud_detector, trust_engine, etc
    model_type = Column(String)
    version = Column(String)
    path = Column(String)  # Path to saved model file
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    last_trained = Column(DateTime)
    is_active = Column(Boolean, default=True)
