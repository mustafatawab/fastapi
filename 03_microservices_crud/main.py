from fastapi import FastAPI, HTTPException
from router import cars

app = FastAPI(title="Car Management API")

app.include_router(cars.router)