from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from models import SessionLocal, Base, engine, User

def reset_db():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 
    print("Database has been reset!")

reset_db()

app = FastAPI()

origins = [
    "*" 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    username: str
    password: str

class LoginReq(BaseModel):
    username: str
    password: str

class ScoreReq(BaseModel):
    username: Optional[str] = None 
    score: int

class LeaderboardItem(BaseModel):
    username: str
    highscore: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    user = User(username=payload.username, password=payload.password, highscore=0)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "highscore": user.highscore}

@app.post("/login")
def login(payload: LoginReq, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"id": user.id, "username": user.username, "highscore": user.highscore}

@app.post("/score")
def post_score(payload: ScoreReq, db: Session = Depends(get_db)):
    if not payload.username:
        return {"ok": True, "stored": False}
    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if payload.score > (user.highscore or 0):
        user.highscore = payload.score
        db.add(user)
        db.commit()
        return {"ok": True, "stored": True, "new_highscore": user.highscore}
    return {"ok": True, "stored": False, "highscore": user.highscore}

@app.get("/leaderboard", response_model=List[LeaderboardItem])
def leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    rows = db.query(User).order_by(User.highscore.desc()).limit(limit).all()
    return [{"username": r.username, "highscore": r.highscore or 0} for r in rows]
