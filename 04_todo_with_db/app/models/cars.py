from sqlmodel import SQLModel, Field
from typing import Optional

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    model: str
    year: int

