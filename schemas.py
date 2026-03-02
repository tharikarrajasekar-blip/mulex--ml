from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    full_name: Optional[str]
    email: Optional[str]
    disabled: Optional[bool]

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    account_id: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    trust_score: float
    kyc_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    account_id: str
    amount: float
    currency: Optional[str] = "INR"
    status: Optional[str] = "PENDING"


class Transaction(TransactionBase):
    id: int
    fraud_probability: float
    timestamp: datetime

    class Config:
        orm_mode = True


class AlertBase(BaseModel):
    account_id: str
    risk_score: int
    type: str
    status: str


class AlertCreate(AlertBase):
    description: Optional[str] = None
    severity: Optional[str] = None


class Alert(AlertBase):
    id: int
    timestamp: datetime
    severity: Optional[str]

    class Config:
        orm_mode = True


class KYCBase(BaseModel):
    account_id: str
    document_type: str


class KYCCreate(KYCBase):
    pass


class KYCRecord(KYCBase):
    id: int
    ocr_extracted: bool
    tamper_detected: bool
    synthetic_identity: bool
    consent_validated: bool
    overall_score: float
    verdict: str
    timestamp: datetime

    class Config:
        orm_mode = True


class AMLBase(BaseModel):
    account_id: str


class AMLCreate(AMLBase):
    pass


class AMLScan(AMLBase):
    id: int
    layering_detected: bool
    structuring_detected: bool
    smurfing_detected: bool
    dispersion_detected: bool
    circular_detected: bool
    str_generated: bool
    timestamp: datetime

    class Config:
        orm_mode = True


class BiometricProfileBase(BaseModel):
    account_id: str


class BiometricProfile(BiometricProfileBase):
    id: int
    typing_velocity_avg: float
    mouse_velocity_avg: float
    anomaly_score: float
    timestamp: datetime

    class Config:
        orm_mode = True


class AuthAttemptBase(BaseModel):
    account_id: str


class AuthAttempt(AuthAttemptBase):
    id: int
    face_verified: bool
    liveness_confirmed: bool
    voice_verified: bool
    deepfake_detected: bool
    overall_success: bool
    timestamp: datetime

    class Config:
        orm_mode = True


class Metrics(BaseModel):
    total_transactions: int
    high_risk_accounts: int
    active_alerts: int
    avg_trust_score: float


class FraudPredictionRequest(BaseModel):
    amount: float = Field(..., gt=0)
    velocity_score: float = Field(..., ge=0, le=100)
    location_risk: float = Field(..., ge=0, le=100)
    device_risk: float = Field(..., ge=0, le=100)
    time_anomaly: float = Field(..., ge=0, le=100)
    network_risk: float = Field(..., ge=0, le=100)


class FraudPredictionResponse(BaseModel):
    fraud_probability: int = Field(..., ge=0, le=100)
    decision: str
    confidence: float
    explanation: Optional[Dict[str, float]] = None


class TrustScoreRequest(BaseModel):
    identity_risk: float = Field(..., ge=0, le=100)
    auth_risk: float = Field(..., ge=0, le=100)
    transaction_risk: float = Field(..., ge=0, le=100)
    network_risk: float = Field(..., ge=0, le=100)
    behavior_risk: float = Field(..., ge=0, le=100)


class TrustScoreResponse(BaseModel):
    trust_score: float
    decision: str
    components: Dict[str, float]


class AMLDetectionRequest(BaseModel):
    account_id: str
    transaction_history: List[Dict]


class AMLDetectionResponse(BaseModel):
    layering_score: int
    structuring_score: int
    smurfing_score: int
    dispersion_score: int
    circular_score: int
    overall_risk: str
    str_generated: bool = False
