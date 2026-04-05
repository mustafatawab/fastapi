from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.user_router import router
from db.session import create_db_tables




@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield



app = FastAPI(lifespan=lifespan, title="Car API", version="1.0.0")

app.include_router(router) 