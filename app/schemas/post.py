from pydantic import BaseModel

class PostCreate(BaseModel):
    text: str
