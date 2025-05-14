from sqlalchemy import Column, Integer, Text, ForeignKey
from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)  # ✅ FIX: use Text for large content
    owner_id = Column(Integer, ForeignKey("users.id"))
