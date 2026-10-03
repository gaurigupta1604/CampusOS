from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt
from .config import settings

ALGORITHM="HS256"
def hash_password(password:str)->str: return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
def verify_password(password:str,hashed:str)->bool:
    try:return bcrypt.checkpw(password.encode(),hashed.encode())
    except ValueError:return False
def create_token(subject:str,kind:str="access"):
    lifetime=timedelta(minutes=settings.access_token_minutes) if kind=="access" else timedelta(days=settings.refresh_token_days)
    return jwt.encode({"sub":subject,"type":kind,"iat":datetime.now(timezone.utc),"exp":datetime.now(timezone.utc)+lifetime},settings.jwt_secret,algorithm=ALGORITHM)
def decode_token(token:str,kind:str="access"):
    try:
        payload=jwt.decode(token,settings.jwt_secret,algorithms=[ALGORITHM])
        if payload.get("type")!=kind or not payload.get("sub"): raise JWTError()
        return payload
    except JWTError as exc: raise ValueError("Invalid or expired token") from exc
