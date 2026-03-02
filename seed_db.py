"""
Database seeding script - Creates sample data for testing
Run this after init_db.py to populate the database with test data
"""

from app.database import SessionLocal, engine
from app import models, crud, schemas
from datetime import datetime, timedelta
import random

def create_sample_users(db):
    """Create sample user accounts"""
    users = [
        schemas.UserCreate(username="admin@mulex.ai", password="secured", role="ADMIN"),
        schemas.UserCreate(username="investigator@mulex.ai", password="secured", role="INVESTIGATOR"),
        schemas.UserCreate(username="user1@email.com", password="password123", role="USER"),
        schemas.UserCreate(username="user2@email.com", password="password123", role="USER"),
    ]
    
    created_users = []
    for user in users:
        existing = crud.get_user(db, user.username)
        if not existing:
            new_user = crud.create_user(db, user)
            created_users.append(new_user)
            print(f"✅ Created user: {user.username}")
        else:
            created_users.append(existing)
            print(f"⏭️ User already exists: {user.username}")
    
    return created_users


def create_sample_accounts(db, users):
    """Create sample trading accounts"""
    accounts_data = [
        ("ACC-1001-XK", users[2].id),
        ("ACC-2002-BB", users[2].id),
        ("ACC-3003-ZQ", users[3].id),
        ("ACC-5005-PQ", users[3].id),
        ("ACC-7007-MM", users[2].id),
    ]
    
    created_accounts = []
    for acc_id, user_id in accounts_data:
        existing = crud.get_account(db, acc_id)
        if not existing:
            acc = crud.create_account(
                db,
                schemas.AccountCreate(account_id=acc_id),
                user_id
            )
            created_accounts.append(acc)
            print(f"✅ Created account: {acc_id}")
        else:
            created_accounts.append(existing)
            print(f"⏭️ Account already exists: {acc_id}")
    
    return created_accounts


def create_sample_transactions(db, accounts):
    """Create sample transactions"""
    transaction_types = [
        (1000, "APPROVED"),
        (5000, "APPROVED"),
        (25000, "APPROVED"),
        (95000, "FLAGGED"),
        (150000, "UNDER_REVIEW"),
        (500, "APPROVED"),
        (48000, "STEP_UP_AUTH"),
    ]
    
    for account in accounts:
        for i in range(random.randint(5, 10)):
            amount, status = random.choice(transaction_types)
            txn = crud.create_transaction(
                db,
                schemas.TransactionBase(
                    account_id=account.account_id,
                    amount=amount + random.randint(-1000, 1000),
                    currency="INR",
                    status=status
                )
            )
            print(f"✅ Created transaction: {account.account_id} - ₹{txn.amount}")
    
    return True


def create_sample_alerts(db, accounts):
    """Create sample risk alerts"""
    alert_types = ["FRAUD", "AML_LAYERING", "VELOCITY_SPIKE", "KYC_INCOMPLETE", "DEEPFAKE_DETECTED"]
    statuses = ["OPEN", "UNDER_REVIEW", "RESOLVED"]
    
    for account in accounts[1:3]:  # Create alerts for some accounts
        for _ in range(random.randint(2, 4)):
            alert = crud.create_alert(
                db,
                schemas.AlertCreate(
                    account_id=account.account_id,
                    risk_score=random.randint(50, 95),
                    type=random.choice(alert_types),
                    status=random.choice(statuses),
                    description="Sample alert for testing",
                    severity="MEDIUM" if random.random() > 0.5 else "HIGH"
                )
            )
            print(f"✅ Created alert: {account.account_id} - {alert.type} (Score: {alert.risk_score})")
    
    return True


def create_sample_kyc_records(db, accounts):
    """Create sample KYC verification records"""
    doc_types = ["AADHAR", "PAN", "PASSPORT", "DL"]
    
    for account in accounts:
        kyc = crud.create_kyc_record(db, account.account_id, random.choice(doc_types))
        
        if kyc:
            # Update with verification details
            updates = {
                "ocr_extracted": True,
                "tamper_detected": False,
                "synthetic_identity": False,
                "consent_validated": True,
                "overall_score": round(random.uniform(70, 98), 2),
                "verdict": "APPROVED" if random.random() > 0.3 else "PENDING"
            }
            
            kyc = crud.update_kyc_record(db, account.account_id, updates)
            if kyc:
                print(f"✅ Created KYC: {account.account_id} - {kyc.verdict}")
            else:
                print(f"⚠️ Failed to update KYC: {account.account_id}")
        else:
            print(f"⚠️ Failed to create KYC: {account.account_id}")
    
    return True


def create_sample_aml_scans(db, accounts):
    """Create sample AML detection records"""
    for account in accounts[::2]:  # Every other account
        aml = crud.create_aml_scan(db, account.account_id)
        
        updates = {
            "layering_detected": random.random() > 0.7,
            "structuring_detected": random.random() > 0.8,
            "smurfing_detected": random.random() > 0.6,
            "dispersion_detected": random.random() > 0.75,
            "circular_detected": random.random() > 0.9,
            "str_generated": random.random() > 0.8
        }
        
        crud.update_aml_scan(db, account.account_id, updates)
        print(f"✅ Created AML scan: {account.account_id}")
    
    return True


def create_sample_biometric_profiles(db, accounts):
    """Create sample behavioral biometric profiles"""
    for account in accounts:
        profile = crud.create_biometric_profile(db, account.account_id)
        profile.typing_velocity_avg = random.uniform(40, 120)  # type: ignore
        profile.mouse_velocity_avg = random.uniform(100, 2000)  # type: ignore
        profile.anomaly_score = random.uniform(0, 50)  # type: ignore
        db.commit()
        print(f"✅ Created biometric profile: {account.account_id}")
    
    return True


def create_sample_auth_attempts(db, accounts):
    """Create sample authentication attempts"""
    for account in accounts:
        for _ in range(random.randint(1, 3)):
            attempt = crud.create_auth_attempt(db, account.account_id)
            
            success = random.random() > 0.15
            updates = {
                "face_verified": success or random.random() > 0.3,
                "liveness_confirmed": success or random.random() > 0.2,
                "voice_verified": success or random.random() > 0.3,
                "deepfake_detected": not success and random.random() > 0.7,
                "overall_success": success
            }
            
            attempt_id = int(attempt.id)  # type: ignore
            crud.update_auth_attempt(db, attempt_id, updates)
            print(f"✅ Created auth attempt: {account.account_id} - {'SUCCESS' if success else 'FAILED'}")
    
    return True


def seed_database():
    """Main seeding function"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("🌱 MULEX AI - DATABASE SEEDING")
        print("=" * 60)
        
        print("\n📝 Creating users...")
        users = create_sample_users(db)
        
        print("\n📊 Creating accounts...")
        accounts = create_sample_accounts(db, users)
        
        print("\n💳 Creating transactions...")
        create_sample_transactions(db, accounts)
        
        print("\n⚠️ Creating alerts...")
        create_sample_alerts(db, accounts)
        
        print("\n📋 Creating KYC records...")
        create_sample_kyc_records(db, accounts)
        
        print("\n🔍 Creating AML scans...")
        create_sample_aml_scans(db, accounts)
        
        print("\n👤 Creating biometric profiles...")
        create_sample_biometric_profiles(db, accounts)
        
        print("\n🔐 Creating authentication attempts...")
        create_sample_auth_attempts(db, accounts)
        
        print("\n" + "=" * 60)
        print("✅ DATABASE SEEDING COMPLETE!")
        print("=" * 60)
        print(f"\nCreated:")
        print(f"  • {len(users)} users")
        print(f"  • {len(accounts)} accounts")
        print(f"  • Multiple transactions, alerts, KYC, AML, biometric records")
        print(f"\nYou can now start the API server:")
        print(f"  python -m uvicorn app.main:app --reload")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
