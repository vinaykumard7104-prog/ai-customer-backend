from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, Float, String, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
from pydantic import BaseModel
import os, random, hashlib

load_dotenv()

app = FastAPI(title="AI Customer Analyzer API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Database ──
_DB_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_DB_DIR}/analytics.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Tables ──
class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    google_id     = Column(String, unique=True, index=True, nullable=True)
    email         = Column(String, unique=True, index=True, nullable=False)
    name          = Column(String, nullable=True)
    picture       = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    auth_type     = Column(String, default="google")

class Analytics(Base):
    __tablename__ = "analytics"
    id         = Column(Integer, primary_key=True, index=True)
    engagement = Column(Float)
    churn      = Column(Float)
    conversion = Column(Float)
    time_spent = Column(Float, nullable=True)
    clicks     = Column(Integer, nullable=True)
    pages      = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)

# ── Google Client IDs ──
GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_ID_WEB = "80897882374-ors5b56g4908qug128la3pot40ea6v86.apps.googleusercontent.com"
GOOGLE_CLIENT_ID_AND = "80897882374-4habl4ihsjj5c7qr6q427ebo66hrcgi5.apps.googleusercontent.com"
ACCEPTED_CLIENT_IDS  = [GOOGLE_CLIENT_ID_WEB, GOOGLE_CLIENT_ID_AND, GOOGLE_CLIENT_ID]

# ── DB Dependency ──
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Request Schemas ──
class GoogleTokenRequest(BaseModel):
    id_token: str

class EmailLoginRequest(BaseModel):
    email: str
    password: str

class PredictRequest(BaseModel):
    time_spent: float
    clicks: int
    pages: int

# ── Health ──
@app.get("/")
def root():
    return {"status": "AI Customer Analyzer API is running", "version": "2.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}

# ── Google Login ──
@app.post("/auth/google")
def google_login(request: GoogleTokenRequest, db: Session = Depends(get_db)):
    try:
        user_info = None
        last_error = None
        for client_id in ACCEPTED_CLIENT_IDS:
            if not client_id:
                continue
            try:
                user_info = id_token.verify_oauth2_token(
                    request.id_token,
                    google_requests.Request(),
                    client_id
                )
                break
            except ValueError as e:
                last_error = e
                continue
        if user_info is None:
            raise ValueError(str(last_error))

        google_id = user_info["sub"]
        email     = user_info["email"]
        name      = user_info.get("name", "")
        picture   = user_info.get("picture", "")

        user = db.query(User).filter(User.google_id == google_id).first()
        is_new = False
        if not user:
            user = User(google_id=google_id, email=email, name=name,
                        picture=picture, auth_type="google")
            db.add(user)
            db.commit()
            db.refresh(user)
            is_new = True

        return {"status": "success", "user_id": user.id, "email": user.email,
                "name": user.name, "picture": user.picture, "is_new_user": is_new}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Google token: {str(e)}")

# ── Email Login ──
@app.post("/auth/email")
def email_login(request: EmailLoginRequest, db: Session = Depends(get_db)):
    email = request.email.lower().strip()
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
    if user.auth_type != "email":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="This email is registered with Google. Please use Google Sign-In.")
    if user.password_hash != password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
    return {"status": "success", "user_id": user.id, "email": user.email,
            "name": user.name, "picture": user.picture or "", "is_new_user": False}

# ── Predict GET ──
@app.get("/predict")
def predict():
    return {
        "engagement_probability": round(random.uniform(0.5, 0.9), 2),
        "churn_risk":             round(random.uniform(0.1, 0.4), 2),
        "conversion_chance":      round(random.uniform(0.4, 0.8), 2)
    }

# ── Predict POST ──
@app.post("/predict")
def predict_with_data(data: PredictRequest, db: Session = Depends(get_db)):
    score      = data.time_spent * 0.1 + data.clicks * 0.05 + data.pages * 0.1
    churn      = round(max(0.05, min(0.95, 1 - score / 20)), 2)
    engagement = round(min(0.95, data.clicks * 0.02 + data.pages * 0.05), 2)
    conversion = round(max(0.05, engagement - churn * 0.3), 2)
    db.add(Analytics(engagement=engagement, churn=churn, conversion=conversion,
                     time_spent=data.time_spent, clicks=data.clicks, pages=data.pages))
    db.commit()
    return {"engagement_probability": engagement, "churn_risk": churn,
            "conversion_chance": conversion, "model_used": "rule-based-engine"}

# ── Analytics ──
@app.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    engagement = round(random.uniform(0.5, 0.9), 2)
    churn      = round(random.uniform(0.1, 0.4), 2)
    conversion = round(random.uniform(0.4, 0.8), 2)
    db.add(Analytics(engagement=engagement, churn=churn, conversion=conversion))
    db.commit()
    return {"engagement": engagement, "churn": churn, "conversion": conversion}

@app.get("/analytics/history")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    records = db.query(Analytics).order_by(Analytics.id.desc()).limit(limit).all()
    return [{"id": r.id, "engagement": r.engagement, "churn": r.churn,
             "conversion": r.conversion, "time_spent": r.time_spent,
             "clicks": r.clicks, "pages": r.pages} for r in records]

@app.get("/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    result = db.query(
        func.avg(Analytics.engagement).label("avg_engagement"),
        func.avg(Analytics.churn).label("avg_churn"),
        func.avg(Analytics.conversion).label("avg_conversion"),
        func.count(Analytics.id).label("total")
    ).first()
    return {"avg_engagement": round(result.avg_engagement or 0, 3),
            "avg_churn":      round(result.avg_churn or 0, 3),
            "avg_conversion": round(result.avg_conversion or 0, 3),
            "total_records":  result.total}
