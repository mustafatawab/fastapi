from fastapi import FastAPI
from routers.auth_router import router as auth_router
from contextlib import asynccontextmanager
from db.session import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


