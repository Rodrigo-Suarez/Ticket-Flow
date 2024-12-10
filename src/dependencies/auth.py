from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Union
from sqlalchemy.orm import Session
from src.models.user import UserResponse
from src.database.db import get_db
from src.dependencies.user import get_user, get_user_db
from src.config import ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"]) #Contexto de encriptacion de la contraseña


def check_password(plane_password, db_password): #Compara la contraseña de la base de datos con la ingresada por el usuario y devuelve True o False
    return pwd_context.verify(plane_password, db_password)
    

def authenticate_user(username, password, db: Session): #Obtiene el usuario y verifica si el nombre y contraseña son correctos
    user = get_user(username, db)
    print(user)
    if not user:
        print("usuario no encontrado")
        raise HTTPException(status_code=401, detail="El ususario no existe", headers={"WWW-Authenticate": "Bearer"})
    if not check_password(password, user.password):
        print("Contraseña incorrecta")
        raise HTTPException(status_code=401, detail="Contraseña incorrecta", headers={"WWW-Authenticate": "Bearer"})
    return user


def get_jwt(data: dict, expires_token: Union[datetime, None] = None):
    data_copy = data.copy()
    if expires_token is None:
        expires = datetime.now() + timedelta(minutes=30)
    else:
        expires = datetime.now() + expires_token
    print(expires)
    data_copy.update({"exp": expires.timestamp()})
    token = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def authenticate_token(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        decode_token = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = decode_token.get("sub")
        if username == None:
            raise HTTPException(status_code=401, detail="No se pudo autenticar3", headers={"WWW-Authenticate": "Bearer"})
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"No se pudo autenticar4: {e}", headers={"WWW-Authenticate": "Bearer"})
    
    user = get_user_db(username, db)
    if not user:
        print("usuario no encontrado")
        raise HTTPException(status_code=401, detail="El ususario no existe", headers={"WWW-Authenticate": "Bearer"})
    
    return user


def verify_admin(user: UserResponse = Depends(authenticate_token)) -> UserResponse:
    if user.role == "administrador":
        return user
    raise HTTPException(status_code=403, detail="No tienes permiso para acceder")