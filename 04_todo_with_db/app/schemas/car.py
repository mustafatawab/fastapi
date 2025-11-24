from pydantic import BaseModel
from typing import Optional

class CarCreate(BaseModel):
    brand: str
    model: str
    year: int


class CarRead(BaseModel):
    id: int
    brand: str
    model: str
    year: int

    model_config = {
        "from_attributes": True  # <-- enables ORM-style conversion
    }

class CarUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None