from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from src.database.models.event import Event
from src.database.models.ticket import Ticket
from sqlalchemy.orm import Session
from src.dependencies.auth import authenticate_token
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

    if event.avaiable_tickets == 0:
        raise HTTPException(status_code=400, detail="No quedan entradas disponibles para el evento")

    event.avaiable_tickets -= 1
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket) #Sincroniza la informacion entre la API y la Base de Datos
    
    return RedirectResponse(url=f"/ticket/{new_ticket.ticket_id}", status_code=303)

