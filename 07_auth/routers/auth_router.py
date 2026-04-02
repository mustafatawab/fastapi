from fastapi import APIRouter, Depends , Response , Request, HTTPException
from db.session import get_session
from sqlmodel import Session, select
from schema.user import UserLogin, UserRegister, UserResponse
from service.auth_service import AuthService
from auth.security import decode_jwt_token
from models.user import User as UserTable
from auth.dependency import get_user


auth = AuthService()



router = APIRouter(prefix="/auth" , tags=['auth'])


@router.post("/register", response_model=UserResponse)
def user_registeration(user: UserRegister , session: Session = Depends(get_session)):
    return auth.register(user, session)


@router.post("/login")
def user_login(response : Response , user: UserLogin , session: Session = Depends(get_session)):
    token = auth.login(user, session)

    response.set_cookie(key="access_token", value=token , httponly=True)

    return {
        "message" : "Logged In Successfuly",
    }



@router.get("/me", response_model=UserResponse)
def get_logged_in_user(current_user: UserTable = Depends(get_user), session: Session = Depends(get_session)):
    return current_user
    

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {
        "message"  : 'You have been logged out successfully...........................'
    }