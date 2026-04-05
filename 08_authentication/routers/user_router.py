from fastapi import APIRouter, Depends, Response
from service.user_service import UserService
from db.session import get_session
from sqlmodel import Session
from schema.user_schema import UserRegister, UserLogin, UserResponse
from auth.security import decode_access_token
from fastapi import HTTPException, status



router = APIRouter(prefix="/users", tags=["Users"])




auth_service = UserService()


@router.post("/register" , response_model=UserResponse)
def register_user(user: UserRegister , session: Session = Depends(get_session)):
    return auth_service.user_registration(user, session)


@router.post("/login" , response_model=dict)
def register_user(response: Response, user: UserLogin , session: Session = Depends(get_session)):
    token = auth_service.user_login(user, session)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True
    )

    return {"messsage" : "User logged in successfully....."}



@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message" : "User logged out successfully........................"}

