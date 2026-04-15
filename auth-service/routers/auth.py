from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models.user import User
from schemas.user import UserRegister, UserLogin, TokenResponse
from auth.jwt import create_access_token

router = APIRouter(tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    user = User(
        email=data.email,
        hashed_password=pwd_context.hash(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registrasi berhasil", "user_id": user.id}

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}