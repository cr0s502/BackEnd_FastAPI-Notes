from fastapi import FastAPI
from .routers.user import userRouter
from .routers.note import noteRouter
from .models import user, note
from .database.database import Base, engine
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Note API",
    description="",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Joan Cruz - CrossDev",
        "url": "http://contact/",
        "email": "joancruz0502@hotmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"])

Base.metadata.create_all(bind=engine)

app.include_router(userRouter)
app.include_router(noteRouter)
