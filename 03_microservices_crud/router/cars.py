from fastapi import APIRouter, Depends, HTTPException
from typing import List


from shemas import CarCreate, CarRead, CarUpdate
from deps import get_car_service
from services.car_service import CarService


router = APIRouter(prefix="/cars", tags=["cars"])

@router.post("/" , response_model=CarRead)
def create_car(car: CarCreate , car_service: CarService = Depends(get_car_service)):
    return car_service.create(car)


@router.get("/" , response_model=List[CarRead])
def read_cars(car_service: CarService = Depends(get_car_service)):
    return car_service.list_all()

@router.get("/{car_id}" , response_model=CarRead)
def read_car(car_id: int, car_service: CarService = Depends(get_car_service)):
    car = car_service.get(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.put("/{car_id}" , response_model=CarRead)
def update_car(car_id: int, car: CarUpdate, car_service: CarService = Depends(get_car_service)):
    updated = car_service.update(car_id, car)
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated

@router.delete("/{car_id}")
def delete_car(car_id: int, car_service: CarService = Depends(get_car_service)):
    deleted = car_service.delete(car_id=car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}