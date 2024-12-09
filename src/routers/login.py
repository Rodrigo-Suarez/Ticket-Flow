from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from src.models.user import GetUser, UserResponse
from src.database.models.user import User
from src.database.db import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Union
from src.config import ALGORITHM, SECRET_KEY

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"]) #Contexto de encriptacion de la contraseña


def get_user_db(username, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return UserResponse(
            user_id = user.user_id,
            username = user.username,
            email = user.email,
            role = user.role,
            creation_date = user.creation_date
        )
    return []


def get_user(username, db: Session) -> GetUser: #Obtiene el usuario de la base de datos y lo transforma en un modelo pydantic
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


@router.post("/login", tags=["Login"], status_code=200, response_description="Acceso permitido")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(hours=20)
    access_token_jwt = get_jwt({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }
    

@router.get("/users/me", tags=["User"])
def get_users_me(user: UserResponse = Depends(authenticate_token)) -> UserResponse:
    return user