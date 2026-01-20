from sqlmodel import SQLModel, Field
from datetime import datetime, date
from pydantic import EmailStr, BaseModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None , primary_key=True)
    name : str = Field(min_length=1 , max_length=100)
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True)
    created_at : datetime = Field(default=datetime.utcnow())
    password : str = Field(min_length=8)





class UserCreate(BaseModel):
    name : str
    username : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    username : str
    password : str

