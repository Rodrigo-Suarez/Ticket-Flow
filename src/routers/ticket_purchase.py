from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from src.models.ticket import PaymentRequest
from src.database.models.event import Event
from src.database.models.ticket import Ticket
from src.routers.ticket_mail import send_ticket
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
async def purchase_ticket(id: int, db: Session = Depends(get_db), user: UserResponse = Depends(authenticate_token)):
    event = db.query(Event).filter(Event.event_id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="No se encontro ningun evento")
    if event.avaiable_tickets == 0:
        raise HTTPException(status_code=400, detail="No quedan entradas disponibles para el evento")
    if event.price == 0:
        return RedirectResponse(url=f"/events/tickets/{event.event_id}/correct", status_code=303)
    
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
                "success": "https://ticket-flow-s9wk.onrender.com/payment-success",
                "failure": "https://ticket-flow-s9wk.onrender.com/payment-failure",
                "pending": "https://ticket-flow-s9wk.onrender.com/payment-pending"
            },

            "auto_return": "approved",
            "external_reference": f"{event.event_id}|{user.user_id}",
            "notification_url": "https://tu-dominio.com/webhook/mercadopago"
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Regresar la URL para que el cliente haga el pago
        return {"url": preference["init_point"]}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)



@router.get("/payment-success")
def payment_success():
    return {"message": "¡Pago aprobado! Revisa tu correo para más detalles."}

@router.get("/payment-failure")
def payment_failure():
    return {"message": "Pago fallido. Por favor, inténtalo nuevamente."}

@router.get("/payment-pending")
def payment_pending():
    return {"message": "Tu pago está pendiente. Recibirás una confirmación cuando sea procesado."}


