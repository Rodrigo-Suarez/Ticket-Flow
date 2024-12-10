from fastapi import APIRouter, Depends
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.dependencies.auth import authenticate_token, authenticate_user, get_jwt, verify_admin
from src.models.user import UserResponse
from src.database.db import get_db
from src.config import ACCESS_TOKEN_EXPIRES_MINUTES

router = APIRouter()


@router.post("/login", tags=["Login"], status_code=200, response_description="Acceso permitido")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_jwt = get_jwt({"sub": user.username, "role": user.role}, ACCESS_TOKEN_EXPIRES_MINUTES)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

@router.get("/users/me", tags=["User"])
async def get_users_me(user: UserResponse = Depends(authenticate_token)) -> UserResponse:
    return user

@router.get("/test", tags=["User"])
async def test(user: UserResponse = Depends(verify_admin)) -> UserResponse:
    return user