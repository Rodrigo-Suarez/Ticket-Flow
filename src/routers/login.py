from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from src.models.user import GetUser
from src.database.models.user import User
from src.database.db import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Union
from src.config import ALGORITHM, SECRET_KEY

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes=["bcrypt"]) #Contexto de encriptacion de la contraseña

def get_user(username, db: Session): #Obtiene el usuario de la base de datos y lo transforma en un modelo pydantic
    user = db.query(User).filter(User.username == username).first()
    if user:
        return GetUser(
            username = user.username,
            password = user.password,
        )
    return []


def check_password(plane_password, db_password): #Compara la contraseña de la base de datos con la ingresada por el usuario y devuelve True o False
    return pwd_context.verify(plane_password, db_password)
    

def authenticate_user(username, password, db: Session): #Obtiene el usuario y verifica si el nombre y contraseña son correctos
    user = get_user(username, db)
    print(user)
    if not user:
        print("usuario no encontrado")
        raise HTTPException(status_code=401, detail="No se pudo autenticar", headers={"WWW-Authenticate": "Bearer"})
    if not check_password(password, user.password):
        print("Contraseña incorrecta")
        raise HTTPException(status_code=401, detail="No se pudo autenticar", headers={"WWW-Authenticate": "Bearer"})
    return user

def get_jwt(data: dict, expires_token: Union[datetime, None] = None):
    data_copy = data.copy()
    if expires_token is None:
        expires = datetime.now() + timedelta(minutes=30)
    else:
        expires = datetime.now() + expires_token
    data_copy.update({"exp": expires})
    token = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

    

@router.post("/login", tags=["Login"], status_code=200, response_description="Acceso permitido")
def login(token: str = Depends(oauth2_schema)):
    return token


@router.post("/token", tags=["Login"])
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(hours=1)
    access_token_jwt = get_jwt({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }