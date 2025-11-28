from ..schemas.car import CarCreate, CarRead
from ..models.cars import Car as CarModel
from sqlmodel import Session, select
from ..repositories.car_repository import CarRepository
from sqlmodel.ext.asyncio.session import AsyncSession

class CarService:

    @staticmethod
    async def list_cars(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        color: str | None = None,
        manufacturer: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ):
        cars , total = await CarRepository.list_cars(
            session=session,
            skip=skip,
            limit=limit,
            color=color,
            manufacturer=manufacturer,
            sort_by=sort_by,
            sort_order=sort_order
        )

        return {
            "data" : cars,
            "meta" : {
                "total" : total,
                "skip" : skip,
                "limit" : limit
            }
        }




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