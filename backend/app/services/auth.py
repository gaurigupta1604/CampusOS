from sqlalchemy.orm import Session
from app.core.security import create_token,decode_token,verify_password
from app.repositories.users import UserRepository
class AuthenticationError(ValueError):pass
class AuthService:
    def __init__(self,db:Session):self.users=UserRepository(db)
    def login(self,email,password):
        user=self.users.by_email(email)
        if not user or not user.is_active or not verify_password(password,user.password_hash):raise AuthenticationError("Invalid email or password")
        return user,create_token(str(user.id)),create_token(str(user.id),"refresh")
    def refresh(self,token):
        try:payload=decode_token(token,"refresh");user=self.users.by_id(int(payload["sub"]))
        except (ValueError,TypeError):raise AuthenticationError("Invalid refresh token")
        if not user or not user.is_active:raise AuthenticationError("Account unavailable")
        return create_token(str(user.id)),create_token(str(user.id),"refresh")
