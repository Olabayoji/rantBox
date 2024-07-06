from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.posts import post_router
from routers.users import user_router
import models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
app.include_router(post_router, prefix="/post")
app.include_router(user_router, prefix="/users")
