from pydantic import BaseModel
from typing import Optional


class CarRead(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    year: int


class CarCreate(BaseModel):
    name: str
    brand: str
    model: str
    year: int


class CarUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None