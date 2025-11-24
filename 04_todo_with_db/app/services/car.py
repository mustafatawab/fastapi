from ..schemas.car import CarCreate, CarRead
from ..models.cars import Car as CarModel
from sqlmodel import Session, select


class CarService:
    def create(self, session: Session, payload : CarCreate) -> CarRead:
        db_obj = CarModel(**payload.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return CarRead.model_validate(db_obj)
    
    def list_all(self, session: Session) -> list[CarRead]:
        statement = select(CarModel)
        result = session.exec(statement).all()
        return [CarRead.model_validate(car) for car in result]


    def get(self, session: Session, car_id: int) -> CarRead | None:
        obj = session.get(CarModel, car_id)
        if obj:
            return CarRead.model_validate(obj)
        return None

    def update(self, session: Session, car_id: int, payload: CarCreate) -> CarRead | None:
        db_obj = session.get(CarModel, car_id)
        if not db_obj:
            return None
        obj_data = payload.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return CarRead.model_validate(db_obj)

    def delete(self, session: Session, car_id: int) -> bool:
        db_obj = session.get(CarModel, car_id)
        if not db_obj:
            return False
        session.delete(db_obj)
        session.commit()
        return True