from models.users import User
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token
from database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



async def get_current_user(
        token: str = Depends(oauth2_scheme) , 
        session: Session = Depends(get_session)
        ):
    
    payload = verify_access_token(token=token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid or Expire token")
    
    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Token payload")
    
    result =  session.exec(select(User).where(User.username == username))
    user = result.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="user not found")

    print("\n[+] User " , user)
    return user