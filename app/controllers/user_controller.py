from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.token_service import get_password_hash, verify_password, create_access_token
from app.core.database import get_db

def signup(user_data: UserCreate, db: Session):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=user_data.email, hashed_password=get_password_hash(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return create_access_token({"sub": user.email})

def login(user_data: UserCreate, db: Session):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_access_token({"sub": user.email})
