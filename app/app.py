from fastapi import FastAPI
from .routers.user import userRouter
from .models import user, note
from .database.database import Base, engine
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(userRouter)