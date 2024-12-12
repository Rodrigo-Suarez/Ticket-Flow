from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal

    
class UserCreate(BaseModel):
    username: str = Field(max_length=50, min_length=1)
    password: str = Field(min_length=8)
    email: EmailStr
    role: Literal["administrador", "asistente"]

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str
    creation_date: datetime

    class Config:
        from_attributes = True

class UserDashboard(BaseModel):
    username: str
    email: str
    role: Literal["administrador", "asistente"]
    tickets: list
    
class UserAdminDashboard(BaseModel):
    username: str
    email: str
    role: Literal["administrador", "asistente"]
    events: list