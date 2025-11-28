from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from sqlmodel import select
from sqlalchemy import func
from ..models.cars import Car


class CarRepository:

    @staticmethod
    async def list_cars(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        color: Optional[str] = None,
        manufacturer: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ):
        """
        Returns (cars list, total_count)
        """

        # ----------------------------------
        # BASE QUERY (filters only)
        # ----------------------------------
        base_query = select(Car)

        if color:
            base_query = base_query.where(Car.color == color)

        if manufacturer:
            base_query = base_query.where(Car.manufacturer == manufacturer)

        # ----------------------------------
        # SORTING
        # ----------------------------------
        if sort_by and hasattr(Car, sort_by):
            column = getattr(Car, sort_by)

            if sort_order == "asc":
                base_query = base_query.order_by(column.asc())
            else:
                base_query = base_query.order_by(column.desc())
        else:
            base_query = base_query.order_by(Car.created_at.desc())

        # ----------------------------------
        # COUNT QUERY (filters repeated)
        # ----------------------------------
        count_query = select(func.count()).select_from(Car)

        if color:
            count_query = count_query.where(Car.color == color)

        if manufacturer:
            count_query = count_query.where(Car.manufacturer == manufacturer)

        count_result = await session.exec(count_query)
        total_count = count_result.one()

        # ----------------------------------
        # PAGINATION
        # ----------------------------------
        paginated_query = base_query.offset(skip).limit(limit)

        result = await session.exec(paginated_query)
        cars = result.all()

        return cars, total_count
