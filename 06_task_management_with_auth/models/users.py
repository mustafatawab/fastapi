from sqlmodel import SQLModel, Field
from datetime import datetime, date
from pydantic import EmailStr, BaseModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None , primary_key=True)
    name : str = Field(min_length=1 , max_length=100)
    email: EmailStr = Field(index=True , unique=True)
    created_at : datetime = Field(default=datetime.utcnow())
    password : str = Field(min_length=8)





class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

