from fastapi import APIRouter, Depends
from service.user_service import UserService
from db.session import get_session
from sqlmodel import Session
from schema.user_schema import UserRegister, UserLogin, UserResponse
from auth.security import decode_access_token
from fastapi import HTTPException, status

router = APIRouter(prefix="/users", tags=["Users"])


