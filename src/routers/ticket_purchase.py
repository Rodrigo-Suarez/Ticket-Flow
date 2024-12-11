from fastapi import APIRouter, Depends, HTTPException
from src.database.models.event import Event
from src.database.models.ticket import Ticket
from sqlalchemy.orm import Session
from src.dependencies.auth import authenticate_token
from src.dependencies.ticket import get_qrcode
from src.models.user import UserResponse
from src.database.db import get_db
from datetime import datetime

router = APIRouter(tags=["Ticket Purchase"])

@router.post("/events/{id}/tickets", status_code=201, response_description="Compra de ticket exitosa, ticket generado")
def purchase_ticket(id: int, db: Session = Depends(get_db), user: UserResponse = Depends(authenticate_token)):
    event = db.query(Event).filter(Event.event_id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="No se encontro ningun evento")
    
    qr_data = f"user_id = {user.user_id}, event_id = {event.event_id}, creation_date = {datetime.now()}"

    new_ticket = Ticket(
        user_id = user.user_id ,
        event_id = event.event_id,
        qr_code = qr_data
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket) #Sincroniza la informacion entre la API y la Base de Datos

    return get_qrcode(qr_data)

