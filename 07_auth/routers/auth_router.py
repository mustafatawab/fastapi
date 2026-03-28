from fastapi import APIRouter, Depends , Response , Request, HTTPException
from db.session import get_session
from sqlmodel import Session, select
from schema.user import UserLogin, UserRegister, UserResponse
from service.auth_service import AuthService
from auth.security import decode_jwt_token
from models.user import User as UserTable

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
        "token" : token
    }


@router.get("/me")
def get_me(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=400 , detail="User is not logged in")


    data = decode_jwt_token(token)

    print("\n Payload Data " , data)
    # if data is None:
    #     raise HTTPException(status_code=400 , detail="User is not logged in")

    user = session.exec(select(UserTable).where(UserTable.email == data["email"])).first()

    return user


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message" : "user logout succesfully"}

