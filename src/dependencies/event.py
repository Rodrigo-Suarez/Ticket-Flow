from fastapi.exceptions import HTTPException
from src.database.models.event import Event
from sqlalchemy.orm import Session
from src.models.user import UserResponse


def get_event_by_id(id: int, admin: UserResponse, db: Session):
    event = db.query(Event).filter(Event.event_id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="No se encontro ningun evento")

    if not event.administrador.user_id == admin.user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder")
    
    return event