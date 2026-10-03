from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest,LoginResponse,RefreshRequest,TokenPair,UserView
from app.services.auth import AuthService,AuthenticationError
router=APIRouter(prefix="/auth",tags=["authentication"])
@router.post("/login",response_model=LoginResponse)
def login(payload:LoginRequest,db:Session=Depends(get_db)):
    try:user,access,refresh=AuthService(db).login(payload.email,payload.password)
    except AuthenticationError as exc:raise HTTPException(status.HTTP_401_UNAUTHORIZED,str(exc))
    return LoginResponse(access_token=access,refresh_token=refresh,user=UserView(id=user.id,email=user.email,full_name=user.full_name,role=user.role))
@router.post("/refresh",response_model=TokenPair)
def refresh(payload:RefreshRequest,db:Session=Depends(get_db)):
    try:access,new_refresh=AuthService(db).refresh(payload.refresh_token)
    except AuthenticationError as exc:raise HTTPException(status.HTTP_401_UNAUTHORIZED,str(exc))
    return TokenPair(access_token=access,refresh_token=new_refresh)
