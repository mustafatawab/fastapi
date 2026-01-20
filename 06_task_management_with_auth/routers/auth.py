from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel, Field
from database import get_session
from core.security import hash_password, verify_password ,create_access_token, verify_access_token
from models.users import User, UserCreate, UserLogin


router = APIRouter(prefix="/auth", tags=['auth'])



# class User(SQLModel, table=True):
#     id: int | None = Field(default=None , primary_key=True)
#     name : str = Field(min_length=1 , max_length=100)
#     email: EmailStr = Field(index=True , unique=True)
#     created_at : datetime = Field(default=datetime.utcnow())
#     password : str = Field(min_length=8)


# class UserCreate(BaseModel):
#     name : str
#     email : EmailStr
#     password : str

# class UserLogin(BaseModel):
#     email : EmailStr
#     password : str




@router.post("/register", response_model=dict[str, str])
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name , username=user.username, email=user.email , password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"detail": "User registered successfully."}
    


@router.post("/login", response_model=dict[str, str])
async def login_user(user: UserLogin, session: Session = Depends(get_session)):
    print("\n Login attempt for email:", user.email)  # Debugging line
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub" : existing_user.username , "email": existing_user.email })

    return {"access_token": token, "token_type": "bearer"}


