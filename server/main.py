from fastapi import FastAPI
from routers.auth import router as auth_router
import models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
