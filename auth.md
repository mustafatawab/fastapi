#### Folder Structure 

```
app/
│
├── main.py
├── database.py
├── config.py
│
├── models/
│   ├── user.py
│   └── task.py
│
├── schemas/
│   ├── user.py
│   └── task.py
│
├── auth/
│   ├── security.py        # hashing + JWT
│   └── dependencies.py   # get_current_user
│
├── routers/
│   ├── auth.py
│   └── tasks.py
│
└── __init__.py

```

##### Rule
- ❌ Routers should NOT import from database.py directly except get_session
- ❌ JWT logic should NOT be in routers
- ✅ Auth logic lives in auth/



#### Step 1

Command : `uv add pydantic-settings`

`config.py`

```python

from pydantic_settings import BaseSettings
from functool import lru_cache

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str = "SUPER_SECRET_KEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

```


#### Step 2 - Password Hashing and JWT

Command: `uv add python-jose "pwdlib[argon2]"`

`auth/security.py`
```python
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, date, timedelta
from jose import jwt, JWTError
from config import get_settings

settings = get_settings()

hash_context = PasswordHash((Argone2Hasher(),))


def hash_password(password: str) -> str:
    """ Convert plain password to hash password """
    return hash_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify whether the password match with the hash """
    return hash_context.verify(plain_password,hashed_password)


def create_access_token(data: dict , expire_time: timedelta | None = None) -> str:
    """ Create JWT Access Token for the login """
    to_encode = data.copy()

    expire = datetime.utcnow() + (expire_time or timedelta(minutes=settings.access_token_expire_minutes))

    to_encode.update({"exp"  : expire})

    return jwt.encode(to_encode , settings.jwt_secret_key , settings.jwt_algorithm)


def decode_token(token) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret_key , settings.jwt_algorithm)
    except JWTError:
        return None

```



#### Step 3 - Database Session

command: `uv add sqlmodel psycopg2-binary`

`database.py`

```python
from sqlmodel import SQLModel, create_engine, Session
from config import get_settings

settings = get_settings()

engine = create_engine(settings.databaseurl , echo=True)

def create_tables():
    """ Create all tables in the database """
    SQLModel.metadata.create_all(engine)


def get_session():
    """ Dependency that provides the database session """ 
    with Session(engine) as session:
        yield session


```

#### Step 4 - Create Models 
`models/user.py`

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```


`models/task.py`

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

```


#### Step 5 - Auth Dependency (Most Important)

`auth/dependency.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.security import decode_token
from database import get_session
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme) , session: Session = Depends(get_session)) -> User:
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.exec(select(User).where(User.id == user_id))
    user = result.first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


```