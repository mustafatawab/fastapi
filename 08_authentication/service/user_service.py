from pydantic import BaseSettings
from schema.user_schema import UserRegister, UserLogin, UserResponse
from db.engine import engine
from db.session import get_session
from sqlmodel import Session, select
from models.user import User
from fastapi import HTTPException, status
from auth.security import hash_password, verify_password, create_access_token, decode_access_token
from datetime import timedelta


class UserService:

    def user_registration(self, user: UserRegister, session : Session):
        # Logic for user registration
        exising_user = session.exec(select(User).where(User.email == user.email)).first()
        if exising_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        
        new_user = User(name=user.name, email=user.email, hashed_password=hash_password(user.password))

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    
    def user_login(self, user: UserLogin, session : Session):
        exising_user = session.exec(select(User).where(User.email == user.email)).first()
        if not exising_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email does not exist")
        
        if not verify_password(user.password, exising_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    
        data = {
            "user_id" : exising_user.id,
            "email" : exising_user.email,
        }
        

        token = create_access_token(data , expire_time=timedelta(minutes=60))

        return {"message" : "User logged in successfully", "access_token" : token}