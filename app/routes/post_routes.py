from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.token_service import decode_token
from app.controllers.post_controller import add_post, get_user_posts, delete_post

router = APIRouter()

def get_current_user_email(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token_data = decode_token(token.split()[1])
    if not token_data or "sub" not in token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data["sub"]

@router.post("/add")
async def create_post(request: Request, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    body = await request.body()
    if len(body) > 1024 * 1024:
        raise HTTPException(status_code=413, detail="Payload too large")
    text = (await request.json())["text"]
    post_id = add_post(text, user_email, db)
    return {"post_id": post_id}

@router.get("/all")
def read_user_posts(db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    posts = get_user_posts(user_email, db)
    return posts

@router.delete("/delete/{post_id}")
def delete_user_post(post_id: int, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    delete_post(post_id, user_email, db)
    return {"detail": "Post deleted"}
