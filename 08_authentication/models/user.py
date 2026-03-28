from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime


class User(SQLModel):
    id: UUID = Field(default_factory=uuid4 , primary_key=True)
    name: str = Field(description="User's full name")
    email: str = Field(unique=True)
    hashed_password: str
    created_at: datetime = Field(default=datetime.today())
    updated_at: datetime = Field(default=datetime.today())