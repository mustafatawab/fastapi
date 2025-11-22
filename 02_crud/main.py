from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Car(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    year: int

class CarCreate(BaseModel):
    name: str
    brand: str
    model: str
    year: int

class CarUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


cars_db: list = []  

@app.post("/cars/", response_model=Car)
def create_car(car: CarCreate):
    new_car = Car(id=len(cars_db) + 1, **car.dict())
    cars_db.append(new_car)
    return new_car

@app.get("/cars/{car_id}", response_model=Car)
def read_car(car_id: int):
    for car in cars_db:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")

@app.get("/cars/", response_model=list[Car])
def read_cars():
    return cars_db


@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, car: CarUpdate):
    for index, existing_car in enumerate(cars_db):
        if existing_car.id == car_id:
            update_car = Car(id=car_id, **car.dict())
            cars_db[index] = update_car
            return update_car
    raise HTTPException(status_code=404, detail="Car not found")

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    for index, existing_car in enumerate(cars_db):
        if existing_car.id == car_id:
            del cars_db[index]
            return {"message": "Car deleted"}
    return {"error": "Car not found"}