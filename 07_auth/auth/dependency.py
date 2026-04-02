from sqlmodel import Session , select
from models.user import User
from auth.security import decode_jwt_token
from fastapi import Request , HTTPException , status, Depends
from db.session import get_session

def get_user(req : Request , session: Session = Depends(get_session)):

    # getting token from the cookies - using "access_token" key in the cookies
    token = req.cookies.get("access_token")

    # If there was no token in the cookies - then it means the user is not logged in
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User is not logged in yet...")
    
    # Decode the token to get the user data that is stored in the decoded/hashed token
    payload = decode_jwt_token(token)

    # get the email from the decoded data
    email = payload.get("email")

    # if there was no email in the docoded data then raise error
    if not email:
        raise HTTPException(status_code=400, detail="Email does not exists")
    
    # Now email found - check the email with the User table in the database and get the whole User record
    user = session.exec(select(User).where(User.email == email)).first()

    # If email does not match with the User table in the database then raise error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")
    
    # Now the user exists in the database with that email - so return the whole user record/data
    return user