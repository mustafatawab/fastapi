from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    brand: str
    model: str
    color: str
    manufacturer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
