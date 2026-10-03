from pydantic import BaseModel, Field
from app.models.domain import Role
class LoginRequest(BaseModel): email:str=Field(min_length=3,max_length=255,pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$"); password:str=Field(min_length=8,max_length=128)
class TokenPair(BaseModel): access_token:str; refresh_token:str; token_type:str="bearer"
class RefreshRequest(BaseModel): refresh_token:str
class UserView(BaseModel): id:int; email:str; full_name:str; role:Role
class LoginResponse(TokenPair): user:UserView
