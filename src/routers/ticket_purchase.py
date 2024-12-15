from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from src.models.ticket import PaymentRequest
from src.database.models.event import Event
from src.database.models.ticket import Ticket
from sqlalchemy.orm import Session
from src.dependencies.auth import authenticate_token
from src.models.user import UserResponse
from src.database.db import get_db
from datetime import datetime
from src.config import prod_access_token
import mercadopago

router = APIRouter(tags=["Ticket Purchase"])


sdk = mercadopago.SDK(prod_access_token)


@router.post("/events/{id}/tickets")
def purchase_ticket(id: int, db: Session = Depends(get_db), user: UserResponse = Depends(authenticate_token)):
    event = db.query(Event).filter(Event.event_id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="No se encontro ningun evento")
    if event.avaiable_tickets == 0:
        raise HTTPException(status_code=400, detail="No quedan entradas disponibles para el evento")
    if event.price == 0:
        pass
    
    payment = PaymentRequest(
        amount=event.price,
        description=event.title,
        email=user.email
    )
    try:
        # Crear una preferencia de pago (MercadoPago)
        preference_data = {
            "items": [
                {
                    "title": payment.description,
                    "quantity": 1,
                    "currency_id": "ARS",  # O la moneda que desees
                    "unit_price": payment.amount
                }
            ],

            "payer": {
                "email": payment.email
            },

            "back_urls": {
                "success": f"https://ticket-flow-s9wk.onrender.com/correct",
                "failure": "https://ticket-flow-s9wk.onrender.com/failure",
                "pending": "https://ticket-flow-s9wk.onrender.com/failure"
            },

            "auto_return": "approved"
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Regresar la URL para que el cliente haga el pago
        return {"url": preference["init_point"]}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)



@router.get("/correct")
def correct():
    return "compra exitosa"

@router.get("/failure")
def correct():
    return "compra fallida"

"""
qr_data = f"user_id = {user.user_id}, event_id = {event.event_id}, creation_date = {datetime.now()}"

    new_ticket = Ticket(
        user_id = user.user_id ,
        event_id = event.event_id,
        qr_code = qr_data
    )

    event.avaiable_tickets -= 1
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket) #Sincroniza la informacion entre la API y la Base de Datos

    return RedirectResponse(url=f"/ticket/{new_ticket.ticket_id}/send", status_code=307)
"""