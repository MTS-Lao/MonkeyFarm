from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    phone: Optional[str] = None
    is_admin: bool = False

class UserCreate(UserBase):
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserUpdate(UserBase):
    password: Optional[str] = None
    confirm_password: Optional[str] = None

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and values['password'] and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserInDBBase(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str