from fastapi import APIRouter, Depends
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.dependencies.event import get_events
from src.dependencies.ticket import get_tickets
from src.dependencies.auth import authenticate_token, authenticate_user, get_jwt
from src.models.user import UserAdminDashboard, UserResponse, UserDashboard
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


@router.get("/users/me", tags=["User"], status_code=200, response_description="Respuesta exitosa")                         
async def get_users_me(user: UserResponse = Depends(authenticate_token), db: Session = Depends(get_db)) -> UserDashboard | UserAdminDashboard:
    if user.role == "administrador":
        return UserAdminDashboard(
            username = user.username,
            email = user.email,
            role = user.role,
            events = get_events(user, db)
    )
    return UserDashboard(
        username = user.username,
        email = user.email,
        role = user.role,
        tickets = get_tickets(user, db)
    )




