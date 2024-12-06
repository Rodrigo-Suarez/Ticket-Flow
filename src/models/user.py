from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal

class UserCreate(BaseModel):
    name: str = Field(max_length=50, min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["administrador", "asistente"]

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: str
    creation_date: datetime

    class Config:
        from_attributes = True
