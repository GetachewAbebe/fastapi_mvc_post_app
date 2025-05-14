from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User
from app.cache.post_cache import post_cache

def add_post(text: str, user_email: str, db: Session):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    post = Post(text=text, owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    post_cache.pop(user_email, None)  # Clear cached posts
    return post.id

def get_user_posts(user_email: str, db: Session):
    if user_email in post_cache:
        return post_cache[user_email]
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    post_cache[user_email] = posts
    return posts

def delete_post(post_id: int, user_email: str, db: Session):
    user = db.query(User).filter(User.email == user_email).first()
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    post_cache.pop(user_email, None)
