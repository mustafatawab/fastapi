from pydantic import BaseModel
from typing import Optional

class CarCreate(BaseModel):
    name: str
    brand: str
    model: str
    color: str
    manufacturer: str

class CarRead(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    color: str
    manufacturer: str

    model_config = {
        "from_attributes": True  # <-- enables ORM-style conversion
    }

class CarUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    model: str | None = None
    color: str | None = None
    manufacturer: str | None = None


class Meta(BaseModel):
    total: int
    skip: int
    limit: int

class CarReadListResponse(BaseModel):
    data : list[CarRead]
    meta : Meta