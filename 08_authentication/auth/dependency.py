from sqlmodel import Session , select
from fastapi import Request , Depends , HTTPException, status
from db.session import get_session
from models.user import User
from auth.security import decode_access_token


def get_current_user(request: Request, session: Session = Depends(get_session)):

    token = request.cookies.get("access_token") 

    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Un Authencticated !!!")


    payload = decode_access_token(token)

    email = payload["email"]

    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Email not found as key in payload .... ")


    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found in the database....")
    

    return user
