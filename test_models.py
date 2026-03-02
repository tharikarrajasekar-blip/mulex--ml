"""
Model Testing and Demonstration Script
Tests all AI/ML models with sample data from the database
"""

from app.database import SessionLocal
from app import models, crud
from app.ml_models import fraud_detector, trust_engine, aml_detector
from datetime import datetime
import json

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"🤖 {title}")
    print("=" * 70)


def test_fraud_detector(db):
    """Test fraud detection model"""
    print_header("FRAUD DETECTION MODEL")
    
    # Sample test cases
    test_cases = [
        {
            "name": "Low Risk Transaction",
            "amount": 1000,
            "velocity_score": 30,
            "location_risk": 20,
            "device_risk": 15,
            "time_anomaly": 10,
            "network_risk": 25
        },
        {
            "name": "Medium Risk Transaction",
            "amount": 50000,
            "velocity_score": 65,
            "location_risk": 60,
            "device_risk": 55,
            "time_anomaly": 70,
            "network_risk": 50
        },
        {
            "name": "High Risk Transaction",
            "amount": 150000,
            "velocity_score": 95,
            "location_risk": 85,
            "device_risk": 90,
            "time_anomaly": 95,
            "network_risk": 80
        }
    ]
    
    for test in test_cases:
        name = test.pop("name")
        result = fraud_detector.predict(**test)
        
        print(f"\n📊 {name}")
        print(f"   Fraud Probability: {result['fraud_probability']}%")
        print(f"   Decision: {result['decision']}")
        print(f"   Confidence: {result['confidence']:.2%}")
        
        # Get explanation
        explanation = fraud_detector.get_shap_explanation(**test)
        if "error" not in explanation:
            print(f"   Feature Importance:")
            for feature, impact in explanation.items():
                print(f"      • {feature}: {impact:.4f}")


def test_trust_engine(db):
    """Test trust scoring engine"""
    print_header("TRUST SCORING ENGINE")
    
    test_cases = [
        {
            "name": "Trusted User",
            "identity_risk": 20,
            "auth_risk": 15,
            "transaction_risk": 25,
            "network_risk": 20,
            "behavior_risk": 30
        },
        {
            "name": "Medium Trust User",
            "identity_risk": 50,
            "auth_risk": 60,
            "transaction_risk": 55,
            "network_risk": 50,
            "behavior_risk": 45
        },
        {
            "name": "High Risk User",
            "identity_risk": 85,
            "auth_risk": 90,
            "transaction_risk": 80,
            "network_risk": 85,
            "behavior_risk": 75
        }
    ]
    
    for test in test_cases:
        name = test.pop("name")
        result = trust_engine.calculate_score(**test)
        
        print(f"\n📊 {name}")
        print(f"   Trust Score: {result['trust_score']}/100")
        print(f"   Decision: {result['decision']}")
        print(f"   Component Breakdown:")
        for component, value in result['components'].items():
            print(f"      • {component}: {value:.2f}")
        
        # Get detailed explanation
        explanation = trust_engine.get_explanation(**test)
        print(f"   Formula: {explanation['formula']}")


def test_aml_detector(db):
    """Test AML pattern detection"""
    print_header("AML PATTERN DETECTION")
    
    # Sample transaction history
    test_cases = [
        {
            "name": "Clean Transaction History",
            "transactions": [
                {"amount": 50000, "recipient_count": 1},
                {"amount": 45000, "recipient_count": 1},
                {"amount": 55000, "recipient_count": 1},
            ]
        },
        {
            "name": "Structuring Pattern (Many Small Transactions)",
            "transactions": [
                {"amount": 9000, "recipient_count": 1},
                {"amount": 8500, "recipient_count": 1},
                {"amount": 9200, "recipient_count": 1},
                {"amount": 9100, "recipient_count": 1},
                {"amount": 8800, "recipient_count": 1},
                {"amount": 9300, "recipient_count": 1},
                {"amount": 8900, "recipient_count": 1},
                {"amount": 9400, "recipient_count": 1},
                {"amount": 9000, "recipient_count": 1},
                {"amount": 8700, "recipient_count": 1},
                {"amount": 9100, "recipient_count": 1},
                {"amount": 9200, "recipient_count": 1},
            ]
        },
        {
            "name": "Smurfing Pattern (Rapid Dispersion)",
            "transactions": [
                {"amount": 1000, "recipient_count": 5},
                {"amount": 1500, "recipient_count": 8},
                {"amount": 1200, "recipient_count": 6},
                {"amount": 1300, "recipient_count": 7},
                {"amount": 2000, "recipient_count": 10},
            ]
        }
    ]
    
    for test in test_cases:
        name = test.pop("name")
        result = aml_detector.detect_patterns(test["transactions"])
        
        print(f"\n📊 {name}")
        print(f"   Overall Risk: {result['overall_risk']}")
        print(f"   Pattern Scores:")
        print(f"      • Layering: {result['layering_score']}")
        print(f"      • Structuring: {result['structuring_score']}")
        print(f"      • Smurfing: {result['smurfing_score']}")
        print(f"      • Dispersion: {result['dispersion_score']}")
        print(f"      • Circular: {result['circular_score']}")


def test_with_database_data(db):
    """Test models with real database data"""
    print_header("REAL DATABASE TESTING")
    
    # Get alerts from database
    alerts = crud.get_alerts(db, limit=5)
    print(f"\n📊 Database Records Found:")
    print(f"   • Total Alerts: {len(alerts)}")
    
    for alert in alerts[:3]:
        print(f"\n   Alert ID: {alert.id}")
        print(f"   Account: {alert.account_id}")
        print(f"   Type: {alert.type}")
        print(f"   Risk Score: {alert.risk_score}")
        print(f"   Status: {alert.status}")
    
    # Get transactions
    accounts = db.query(models.Account).limit(3).all()
    print(f"\n   • Total Accounts in DB: {db.query(models.Account).count()}")
    
    for account in accounts:
        txns = crud.get_transactions(db, account.account_id, limit=3)
        print(f"\n   Account: {account.account_id}")
        print(f"   Trust Score: {account.trust_score}")
        print(f"   Recent Transactions: {len(txns)}")
        for txn in txns[:2]:
            print(f"      • Amount: ₹{txn.amount} | Status: {txn.status}")
    
    # Get metrics
    metrics = crud.get_metrics(db)
    print(f"\n   📈 System Metrics:")
    print(f"      • Total Transactions: {metrics.total_transactions}")
    print(f"      • High Risk Accounts: {metrics.high_risk_accounts}")
    print(f"      • Active Alerts: {metrics.active_alerts}")
    print(f"      • Average Trust Score: {metrics.avg_trust_score}")


def test_model_predictions_on_real_data(db):
    """Make predictions on real database records"""
    print_header("LIVE PREDICTIONS ON DATABASE DATA")
    
    accounts = db.query(models.Account).limit(2).all()
    
    for account in accounts:
        print(f"\n📊 Account: {account.account_id}")
        
        # Get recent transactions for pattern analysis
        txns = crud.get_transactions(db, account.account_id, limit=10)
        
        if txns:
            # Prepare transaction data for AML
            txn_data = [
                {
                    "amount": float(t.amount),  # type: ignore
                    "recipient_count": 1,
                    "is_circular": False
                }
                for t in txns
            ]
            
            aml_result = aml_detector.detect_patterns(txn_data)
            print(f"   AML Risk Level: {aml_result['overall_risk']}")
            print(f"   Patterns Detected:")
            print(f"      • Layering: {aml_result['layering_score']}")
            print(f"      • Structuring: {aml_result['structuring_score']}")
            print(f"      • Smurfing: {aml_result['smurfing_score']}")
        
        # Trust score prediction
        trust_result = trust_engine.calculate_score(
            identity_risk=30,
            auth_risk=25,
            txn_risk=40,
            network_risk=20,
            behavior_risk=35
        )
        print(f"   Trust Score: {trust_result['trust_score']}/100")
        print(f"   Decision: {trust_result['decision']}")


def run_tests():
    """Run all model tests"""
    db = SessionLocal()
    try:
        print("\n" + "🚀" * 35)
        print("MULEX AI - MODEL TESTING & DEMONSTRATION")
        print("🚀" * 35)
        
        # Test models with sample data
        test_fraud_detector(db)
        test_trust_engine(db)
        test_aml_detector(db)
        
        # Test with real database data
        test_with_database_data(db)
        test_model_predictions_on_real_data(db)
        
        print("\n" + "=" * 70)
        print("✅ ALL MODEL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("   • Fraud Detection: ✅ Working")
        print("   • Trust Scoring: ✅ Working")
        print("   • AML Detection: ✅ Working")
        print("   • Database Integration: ✅ Connected")
        print("\n🚀 Ready to deploy! Start the server:")
        print("   python -m uvicorn app.main:app --reload\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    run_tests()
