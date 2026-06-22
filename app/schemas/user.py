from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegisterSchema(BaseModel):
    name     : str
    email    : EmailStr
    password : str
    is_host  : bool = False

class LoginSchema(BaseModel):
    email    : EmailStr
    password : str

class UserResponse(BaseModel):
    id         : int
    name       : str
    email      : str
    is_host    : bool
    created_at : datetime

    class Config:
        from_attributes = True