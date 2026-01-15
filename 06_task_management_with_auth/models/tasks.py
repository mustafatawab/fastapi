from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime


class Tasks(SQLModel, table=True):
    id : int | None = Field(default=None , primary_key=True)
    title : str = Field(min_length=1 , max_length=200)
    created_at : datetime = Field(default=datetime.utcnow())
    completed : bool = Field(default=False)
    userId: int | None = Field(default=None, foreign_key="user.id")



class TaskCreate(BaseModel):
    title : str

class TaskUpdate(BaseModel):
    title : str | None = None
    completed : bool | None = None

class TaskReponse(BaseModel):
    id : int
    title : str
    created_at : str | None = None
    completed : bool

