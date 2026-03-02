from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas, routes
from .database import SessionLocal, engine
from .config import DATABASE_URL, PORT, DEBUG, SECRET_KEY
from datetime import timedelta
import uvicorn
import os

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MuleX AI Backend")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# simple in-memory token store for demo
fake_tokens = {}

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fake_hash_token(token: str):
    return token + "_hashed"


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token = fake_hash_token(user.username)  # type: ignore
    fake_tokens[token] = user.username  # type: ignore
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = fake_tokens.get(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")
    user = crud.get_user(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    return user


@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/dashboard/metrics", response_model=schemas.Metrics)
def read_metrics(db: Session = Depends(get_db)):
    return crud.get_metrics(db)


@app.get("/dashboard/alerts", response_model=list[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_alerts(db, skip=skip, limit=limit)


@app.post("/alerts", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_alert(db, alert)


@app.post("/transactions", response_model=schemas.Transaction)
def create_transaction(txn: schemas.TransactionBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_transaction(db, txn)


# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/feed")
async def websocket_feed(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # echo back for now
            await manager.send_personal_message(f"received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# startup task to simulate feed messages
@app.on_event("startup")
async def start_feed_simulation():
    import asyncio
    import random

    async def producer():
        messages = [
            "TXN ₹1,200 · ACC-1103 · Mumbai → APPROVED",
            "TXN ₹95,000 · ACC-9087 · Delhi → FLAGGED HIGH VELOCITY",
            "LOGIN ATTEMPT · ACC-3312 · IP 192.168.4.20 → DEEPFAKE DETECTED",
            "TXN ₹500 · ACC-2201 · Chennai → APPROVED",
            "KYC UPLOAD · ACC-7741 · Document Tampering → BLOCKED",
            "TXN ₹48,000 · ACC-5503 · Pune → STEP-UP AUTH REQUIRED",
            "AML ALERT · ACC-8800 · Layering Pattern → STR GENERATED",
            "TXN ₹220 · ACC-0042 · Bengaluru → APPROVED"
        ]
        while True:
            await asyncio.sleep(2.5)
            msg = random.choice(messages)
            await manager.broadcast(msg)

    asyncio.create_task(producer())


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MuleX AI Backend - Starting Server")
    print("=" * 60)
    print(f"📊 Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print(f"🔌 Port: {PORT}")
    print(f"🐛 Debug: {DEBUG}")
    print("=" * 60)
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=DEBUG)
