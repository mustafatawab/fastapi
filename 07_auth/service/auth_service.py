from auth.security import password_hashing , verify_password ,  create_jwt_token ,  decode_jwt_token
from sqlmodel import Session, select
from schema.user import UserRegister, UserLogin, UserResponse
from models.user import User as UserTable
from fastapi import HTTPException



class AuthService:

    def existing_user(self, email: str, session : Session):
        user = session.exec(select(UserTable).where(UserTable.email == email)).first()
        return user

    def register(self, user: UserRegister , session: Session):
        if  self.existing_user(user.email, session):
            raise HTTPException(status_code=400, detail="User or email already exists")
    
        new_user = UserTable(email=user.email , name=user.name, hash_password=password_hashing(user.password))
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    

    def login(self, user: UserLogin , session: Session):
        ex_user = self.existing_user(user.email, session)
        print(f"\n[DEBUG] Login attempt:")
        print(f"  Email: {user.email}")
        print(f"  Input password: {user.password}")
        print(f"  Found user: {ex_user}")
        if ex_user:
            print(f"  Stored hash: {ex_user.hash_password}")
        
        if not ex_user:
            raise HTTPException(status_code=401, detail="User or email not found")

        verification = verify_password(user.password , ex_user.hash_password)
        print(f"  Final verification result: {verification}")
        
        if not verification:
            raise HTTPException(status_code=401, detail="Password is incorrect")
        
        data = {
            "id" : str(ex_user.id),
            "email" : ex_user.email,
        }

        return create_jwt_token(data)