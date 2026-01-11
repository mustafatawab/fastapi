from fastapi import FastAPI
from app.routers.car import car_router
from sqlmodel import SQLModel
from app.db.engine import engine
from contextlib import asynccontextmanager


def create_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield



app = FastAPI(lifespan=lifespan, title="Car API", version="1.0.0")

app.include_router(car_router) 

