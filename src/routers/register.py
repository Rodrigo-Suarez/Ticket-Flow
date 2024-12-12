from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.models.user import UserCreate, UserResponse
from src.database.models.user import User
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.dependencies.auth import pwd_context

router = APIRouter()

def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/register", tags=["Register"], status_code=201, response_description="Usuario creado exitosamente", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    user_validator = db.query(User).filter(User.username == user.username).first() #Busca si existe un usuario con el nombre ingresado y lo devuelve
    if user_validator: 
        raise  HTTPException(status_code=409, detail="El nombre de usuario ya está registrado") #409: Conflicto con los recursos existentes
    
    email_validator = db.query(User).filter(User.email == user.email).first() #Busca si existe un usuario con el gmail ingresado y lo devuelve
    if email_validator:#Si existe un usuario con ese gmail, lanza una exepción, si no continua
        raise  HTTPException(status_code=409, detail="El correo electrónico ya está registrado") 
    
    #Se crea una nueva variable con los datos para no perder los datos originales. Ademas permite hacer modificaciones en los mismos, como hashear la contraseña
    new_user = User(
        username = user.username,
        email = user.email,
        password=hash_password(user.password),
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #Sincroniza la informacion entre la API y la Base de Datos

    return  UserResponse.model_validate(new_user)





