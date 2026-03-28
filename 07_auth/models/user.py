from sqlmodel import SQLModel , Field
from uuid import uuid4 , UUID


class User(SQLModel , table=True):
    id: UUID = Field(default_factory=uuid4 , primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    hash_password: str  = Field(index=True)

