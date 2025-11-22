from services.car_service import CarService


_default_car_service = CarService()

def get_car_service() -> CarService:
    return _default_car_service