from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config.setting import get_settings

setting = get_settings()

pass_hasher = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return pass_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pass_hasher.verify(plain_password, hashed_password)



def create_access_token(data : dict , expire_time: timedelta | None = None):
    to_encode = data.copy()

    exp = datetime.utcnow() + ( expire_time or timedelta(days=1)) 

    to_encode.update({"exp": exp})
    
    return jwt.encode(to_encode, setting.JWT_SECRET_KEY)



def decode_access_token(token: str):
    try:
       return jwt.decode(token, setting.JWT_SECRET_KEY)
    except JWTError:
        return None