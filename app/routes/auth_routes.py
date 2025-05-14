from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.controllers.user_controller import signup, login
from app.core.database import get_db

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    return {"token": signup(user, db)}

@router.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    return {"token": login(user, db)}
