from fastapi import FastAPI
from app.routes import auth_routes, post_routes
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Modular FastAPI MVC App")
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(post_routes.router, prefix="/posts", tags=["Posts"])
