from jose import jwt, JWTError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime , timedelta
from config.settings import get_settings



ph = PasswordHash((Argon2Hasher(),))


def password_hashing(password: str):
    return ph.hash(password)

def verify_password(plain_pass: str, hashed_pass: str):
    print(f"\n[DEBUG] verify_password called:")
    print(f"  Input password: {plain_pass}")
    print(f"  Stored hash: {hashed_pass}")
    try:
        result = ph.verify(plain_pass, hashed_pass)
        print(f"  Verification result: {result}")
        print(f"  Result type: {type(result)}")
        return result
    except Exception as e:
        print(f"  Verification error: {e}")
        return False


def create_jwt_token(data: dict):
    encode = data.copy()
    exp_time = datetime.today() + timedelta(days=1)
    encode.update({"exp" : exp_time})
    token = jwt.encode(encode , get_settings().JWT_SECRET)
    return token



def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, get_settings().JWT_SECRET)
    except JWTError:
        return None