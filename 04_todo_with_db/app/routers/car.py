from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated, List
from ..schemas.car import CarCreate, CarRead, CarUpdate
from ..db.session import get_session
from ..models.cars import Car
from ..services.car import CarService

car_router = APIRouter(prefix="/cars", tags=["cars"])

service = CarService()


@car_router.get("/", response_model=dict)
def root():
    return {"message": "Welcome to the Car API"}


@car_router.post("/", response_model=CarRead)
def crate_car(car: CarCreate , session : Annotated[Session, Depends(get_session)]):
    car_added = service.create(session, car)
    return car_added


@car_router.get("/", response_model=List[CarRead])
def list_cars(session : Annotated[Session, Depends(get_session)]):
    cars = service.list_all(session)
    return cars

@car_router.get("/{car_id}", response_model=CarRead)
def get_car(car_id: int, session : Annotated[Session, Depends(get_session)]):
    car = service.get(session, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@car_router.put("/{car_id}", response_model=CarRead)
def update_car(car_id: int, payload: CarUpdate, session : Annotated[Session, Depends(get_session)]):
    updated_car = service.update(session, car_id, payload)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated_car



@car_router.delete("/{car_id}", response_model=dict)
def delete_car(car_id: int, session : Annotated[Session, Depends(get_session)]):
    deleted = service.delete(session, car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}

