from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import Settings

settings = Settings()

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
        return payload
    
    except JWTError:
        return None