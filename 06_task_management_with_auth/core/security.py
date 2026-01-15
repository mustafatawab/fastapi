from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import Settings
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

settings = Settings()

password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """Hash a password with Argon2."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return password_hash.verify(plain_password, hashed_password)



def create_access_token(data: dict, expired_delta: timedelta | None = None):
    """ Create JWT Access Token for the logged in user """
    to_encode= data.copy()

    expire = datetime.utcnow() + (expired_delta or timedelta(minutes=15))

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm="HS256")



def verify_access_token(token: str) -> dict | None:
    """ Verify JWT Access Token and return the payload"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        print("[+] Payload" , payload)
        return payload
    
    except JWTError:
        return None