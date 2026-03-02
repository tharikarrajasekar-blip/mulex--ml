"""
ML/AI Models and Prediction Services for MuleX AI
Includes: Fraud Detection, Trust Scoring, Explainable AI (SHAP)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

# Optional SHAP import with fallback
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("Warning: SHAP not available, explanations will be limited")

# Model file paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'trained_models')
os.makedirs(MODELS_DIR, exist_ok=True)

FRAUD_MODEL_PATH = os.path.join(MODELS_DIR, 'fraud_detector.joblib')
TRUST_MODEL_PATH = os.path.join(MODELS_DIR, 'trust_engine.joblib')


class FraudDetector:
    """XGBoost-style Fraud Detection Model"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['amount', 'velocity_score', 'location_risk', 
                             'device_risk', 'time_anomaly', 'network_risk']
        self.load_or_train()
    
    def load_or_train(self):
        """Load existing model or create a new one"""
        if os.path.exists(FRAUD_MODEL_PATH):
            self.model = joblib.load(FRAUD_MODEL_PATH)
        else:
            self.train_default_model()
    
    def train_default_model(self):
        """Train a default fraud detector on synthetic data"""
        # Generate synthetic training data
        n_samples = 500
        X = np.random.rand(n_samples, 6) * 100
        y = (X[:, 0] > 50) | (X[:, 1] > 70) | (X[:, 4] > 80)  # Simple rules
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = GradientBoostingClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Save model
        joblib.dump(self.model, FRAUD_MODEL_PATH)
    
    def predict(self, amount: float, velocity_score: float, location_risk: float,
                device_risk: float, time_anomaly: float, network_risk: float) -> dict:
        """Predict fraud probability (0-100)"""
        if self.model is None:
            return {
                "fraud_probability": 50,
                "decision": "STEP-UP AUTH",
                "confidence": 0.5
            }
        
        features = np.array([[amount, velocity_score, location_risk, 
                             device_risk, time_anomaly, network_risk]])
        probability = self.model.predict_proba(features)[0][1]
        fraud_score = int(probability * 100)
        
        decision = "BLOCKED" if fraud_score > 75 else "STEP-UP AUTH" if fraud_score > 50 else "APPROVED"
        
        return {
            "fraud_probability": fraud_score,
            "decision": decision,
            "confidence": float(probability)
        }
    
    def get_shap_explanation(self, amount: float, velocity_score: float, 
                            location_risk: float, device_risk: float, 
                            time_anomaly: float, network_risk: float) -> dict:
        """Get SHAP explanation for prediction"""
        features = np.array([[amount, velocity_score, location_risk, 
                             device_risk, time_anomaly, network_risk]])
        
        if not SHAP_AVAILABLE:
            # Fallback explanation without SHAP
            return {
                "amount": float(amount),
                "velocity_score": float(velocity_score),
                "location_risk": float(location_risk),
                "device_risk": float(device_risk),
                "time_anomaly": float(time_anomaly),
                "network_risk": float(network_risk),
                "note": "Full SHAP explanations require shap package"
            }
        
        try:
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(features)
            
            # For binary classification, get the positive class explanation
            if isinstance(shap_values, list):
                shap_vals = shap_values[1][0]
            else:
                shap_vals = shap_values[0]
            
            explanation = {
                feature: float(val) 
                for feature, val in zip(self.feature_names, shap_vals)
            }
            return explanation
        except Exception as e:
            return {"error": str(e)}


class TrustEngine:
    """Weighted Trust Score Calculator"""
    
    def __init__(self):
        self.weights = {
            'identity': 0.2,
            'auth': 0.2,
            'transaction': 0.25,
            'network': 0.2,
            'behavior': 0.15
        }
    
    def calculate_score(self, identity_risk: float, auth_risk: float, 
                       txn_risk: float, network_risk: float, 
                       behavior_risk: float) -> dict:
        """
        Calculate composite trust score (0-100)
        Risks are inverted to trust (100 - risk)
        """
        identity_trust = max(0, 100 - identity_risk)
        auth_trust = max(0, 100 - auth_risk)
        txn_trust = max(0, 100 - txn_risk)
        network_trust = max(0, 100 - network_risk)
        behavior_trust = max(0, 100 - behavior_risk)
        
        composite = (
            identity_trust * self.weights['identity'] +
            auth_trust * self.weights['auth'] +
            txn_trust * self.weights['transaction'] +
            network_trust * self.weights['network'] +
            behavior_trust * self.weights['behavior']
        )
        
        decision = "APPROVE" if composite > 75 else "STEP-UP AUTH" if composite > 50 else "BLOCK"
        
        return {
            "trust_score": round(composite, 2),
            "decision": decision,
            "components": {
                "identity": round(identity_trust * self.weights['identity'], 2),
                "auth": round(auth_trust * self.weights['auth'], 2),
                "transaction": round(txn_trust * self.weights['transaction'], 2),
                "network": round(network_trust * self.weights['network'], 2),
                "behavior": round(behavior_trust * self.weights['behavior'], 2),
            }
        }
    
    def get_explanation(self, identity_risk: float, auth_risk: float,
                       txn_risk: float, network_risk: float,
                       behavior_risk: float) -> dict:
        """Get detailed explanation of trust score"""
        result = self.calculate_score(
            identity_risk, auth_risk, txn_risk, network_risk, behavior_risk
        )
        
        explanation = {
            "formula": "0.2·I + 0.2·A + 0.25·T + 0.2·N + 0.15·B",
            "where": {
                "I": "Identity Risk",
                "A": "Auth Risk",
                "T": "Transaction Risk",
                "N": "Network Risk",
                "B": "Behavioral Risk"
            },
            "risk_inputs": {
                "identity_risk": identity_risk,
                "auth_risk": auth_risk,
                "transaction_risk": txn_risk,
                "network_risk": network_risk,
                "behavioral_risk": behavior_risk
            },
            "result": result
        }
        
        return explanation


class AMLDetector:
    """AML Pattern Detection"""
    
    @staticmethod
    def detect_patterns(transaction_history: list[dict]) -> dict:
        """
        Detect AML patterns from transaction history
        Patterns: Layering, Structuring, Smurfing, Dispersion, Circular
        """
        if not transaction_history:
            return {
                "layering_score": 0,
                "structuring_score": 0,
                "smurfing_score": 0,
                "dispersion_score": 0,
                "circular_score": 0,
                "overall_risk": "LOW"
            }
        
        df = pd.DataFrame(transaction_history)
        
        # Layering: Multiple transactions in short time with varying amounts
        if len(df) > 3:
            layering_score = min(100, len(df) * 10)
        else:
            layering_score = 0
        
        # Structuring: Amounts just below thresholds (e.g., <100k repeated)
        high_amt = df['amount'].max()
        if (df['amount'] < high_amt * 0.9).sum() > 5:
            structuring_score = 40
        else:
            structuring_score = 0
        
        # Smurfing: Many small transactions
        if (df['amount'] < 10000).sum() > 10:
            smurfing_score = 50
        else:
            smurfing_score = 20
        
        # Dispersion: Transactions to many different entities
        if 'recipient_count' in df:
            dispersion_score = min(100, df['recipient_count'].sum() * 5)
        else:
            dispersion_score = 0
        
        if 'is_circular' in df and (df['is_circular'] == True).any():
            circular_score = 30
        else:
            circular_score = 0
        
        # Calculate overall risk
        max_score = max([layering_score, structuring_score, smurfing_score])
        if max_score > 70:
            overall_risk = "CRITICAL"
        elif max_score > 50:
            overall_risk = "HIGH"
        elif max_score > 30:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"
        
        return {
            "layering_score": int(layering_score),
            "structuring_score": int(structuring_score),
            "smurfing_score": int(smurfing_score),
            "dispersion_score": int(dispersion_score),
            "circular_score": int(circular_score),
            "overall_risk": overall_risk
        }


# Global instances
fraud_detector = FraudDetector()
trust_engine = TrustEngine()
aml_detector = AMLDetector()
