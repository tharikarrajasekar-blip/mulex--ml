from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from typing import List, Optional
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─── USER OPERATIONS ───
def get_user(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user(db, username)
    if not user:
        return None
    hashed_pwd = user.hashed_password  # type: ignore
    if not pwd_context.verify(password, hashed_pwd):  # type: ignore
        return None
    return user


# ─── ACCOUNT OPERATIONS ───
def create_account(db: Session, account: schemas.AccountCreate, user_id: int) -> models.Account:
    db_account = models.Account(account_id=account.account_id, user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_account(db: Session, account_id: str) -> Optional[models.Account]:
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()


def update_trust_score(db: Session, account_id: str, score: float) -> Optional[models.Account]:
    account = get_account(db, account_id)
    if account:
        account.trust_score = score  # type: ignore
        account.last_activity = datetime.utcnow()  # type: ignore
        db.commit()
        db.refresh(account)
    return account


# ─── TRANSACTION OPERATIONS ───
def create_transaction(db: Session, txn: schemas.TransactionBase) -> models.Transaction:
    db_txn = models.Transaction(**txn.dict())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn


def get_transactions(db: Session, account_id: str, limit: int = 50) -> List[models.Transaction]:
    return db.query(models.Transaction).filter(
        models.Transaction.account_id == account_id
    ).order_by(models.Transaction.timestamp.desc()).limit(limit).all()


# ─── ALERT OPERATIONS ───
def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Alert]:
    return db.query(models.Alert).order_by(models.Alert.timestamp.desc()).offset(skip).limit(limit).all()


def create_alert(db: Session, alert: schemas.AlertCreate) -> models.Alert:
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_account_alerts(db: Session, account_id: str, limit: int = 20) -> List[models.Alert]:
    return db.query(models.Alert).filter(
        models.Alert.account_id == account_id
    ).order_by(models.Alert.timestamp.desc()).limit(limit).all()


# ─── KYC OPERATIONS ───
def create_kyc_record(db: Session, account_id: str, doc_type: str) -> models.KYCRecord:
    # Remove existing KYC if it exists
    db.query(models.KYCRecord).filter(models.KYCRecord.account_id == account_id).delete()
    db.commit()
    
    kyc = models.KYCRecord(
        account_id=account_id,
        document_type=doc_type,
        overall_score=0.0,
        verdict="PENDING"
    )
    db.add(kyc)
    db.commit()
    db.refresh(kyc)
    return kyc


def get_kyc_record(db: Session, account_id: str) -> Optional[models.KYCRecord]:
    return db.query(models.KYCRecord).filter(models.KYCRecord.account_id == account_id).first()


def update_kyc_record(db: Session, account_id: str, updates: dict):
    kyc = get_kyc_record(db, account_id)
    if kyc:
        for key, value in updates.items():
            setattr(kyc, key, value)
        db.commit()
        db.refresh(kyc)
    return kyc


# ─── AML OPERATIONS ───
def create_aml_scan(db: Session, account_id: str) -> models.AMLScan:
    aml = models.AMLScan(account_id=account_id)
    db.add(aml)
    db.commit()
    db.refresh(aml)
    return aml


def get_aml_scan(db: Session, account_id: str) -> Optional[models.AMLScan]:
    return db.query(models.AMLScan).filter(
        models.AMLScan.account_id == account_id
    ).order_by(models.AMLScan.timestamp.desc()).first()


def update_aml_scan(db: Session, account_id: str, updates: dict):
    aml = get_aml_scan(db, account_id)
    if aml:
        for key, value in updates.items():
            setattr(aml, key, value)
        db.commit()
        db.refresh(aml)
    return aml


# ─── BIOMETRIC OPERATIONS ───
def create_biometric_profile(db: Session, account_id: str) -> models.BiometricProfile:
    profile = models.BiometricProfile(account_id=account_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_biometric_profile(db: Session, account_id: str) -> Optional[models.BiometricProfile]:
    return db.query(models.BiometricProfile).filter(
        models.BiometricProfile.account_id == account_id
    ).first()


# ─── AUTHENTICATION OPERATIONS ───
def create_auth_attempt(db: Session, account_id: str) -> models.AuthenticationAttempt:
    attempt = models.AuthenticationAttempt(account_id=account_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def update_auth_attempt(db: Session, attempt_id: int, updates: dict) -> Optional[models.AuthenticationAttempt]:
    attempt = db.query(models.AuthenticationAttempt).filter(
        models.AuthenticationAttempt.id == attempt_id
    ).first()
    if attempt:
        for key, value in updates.items():
            setattr(attempt, key, value)
        db.commit()
        db.refresh(attempt)
    return attempt


# ─── METRICS ───
def get_metrics(db: Session) -> schemas.Metrics:
    total = db.query(models.Transaction).count()
    high_risk = db.query(models.Alert).filter(models.Alert.risk_score >= 75).count()
    active = db.query(models.Alert).filter(models.Alert.status.in_(["OPEN", "UNDER_REVIEW"])).count()
    
    accounts = db.query(models.Account).all()
    if accounts:
        trust_scores = [float(a.trust_score) for a in accounts]  # type: ignore
        avg_trust = sum(trust_scores) / len(trust_scores)
    else:
        avg_trust = 0.0
    
    return schemas.Metrics(
        total_transactions=total,
        high_risk_accounts=high_risk,
        active_alerts=active,
        avg_trust_score=float(round(avg_trust, 2)),
    )
