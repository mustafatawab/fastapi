from threading import Lock
from shemas import CarCreate, CarUpdate, CarRead

class CarService:
    def __init__(self):
        self._cars: list[CarRead] = []
        self._next_id: int = 1
        self._lock = Lock()
    

    def create(self, data: CarCreate) -> CarRead:
        with self._lock:
            car = CarRead(id=self._next_id, **data.model_dump())
            self._cars.append(car)
            self._next_id += 1
            return car
    
    def list_all(self) -> list[CarRead]:
        return list(self._cars)
    
    def get(self, car_id: int) -> CarRead | None:
        for car in self._cars:
            if car.id == car_id:
                return car
        return None

    def update(self, car_id: int, data: CarUpdate) -> CarRead | None:
        with self._lock:
            for i , c in enumerate(self._cars):
                if c.id == car_id:
                    updated_data = c.model_dump()
                    updated_fields = data.model_dump(exclude_unset=True)
                    updated_data.update(updated_fields)
                    updated_car = CarRead(**updated_data)
                    self._cars[i] = updated_car
                    return updated_car
        return None

    def delete(self, car_id: int) -> bool:
        with self._lock:
            for i, c in enumerate(self._cars):
                if c.id == car_id:
                    del self._cars[i]
                    return True
        return False