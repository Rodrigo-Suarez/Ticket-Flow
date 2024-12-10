from src.models.user import UserCreate, UserResponse
from src.database.models.user import User
from sqlalchemy.orm import Session

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


def get_user(username, db: Session) -> UserCreate: #Obtiene el usuario de la base de datos y lo transforma en un modelo pydantic
    user = db.query(User).filter(User.username == username).first()
    if user:
        return UserCreate(
            username = user.username,
            password = user.password,
            role = user.role,
            email = user.email
        )
    return []