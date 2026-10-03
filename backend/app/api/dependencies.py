from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.domain import Role,User
bearer=HTTPBearer(auto_error=False)
def current_user(credentials:HTTPAuthorizationCredentials|None=Depends(bearer),db:Session=Depends(get_db)):
    if not credentials:raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Authentication required")
    try:user=db.get(User,int(decode_token(credentials.credentials)["sub"]))
    except (ValueError,TypeError):raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid or expired token")
    if not user or not user.is_active:raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Account unavailable")
    return user
def allow(*roles:Role):
    def dependency(user:User=Depends(current_user)):
        if user.role not in roles:raise HTTPException(status.HTTP_403_FORBIDDEN,"Insufficient permissions")
        return user
    return dependency
