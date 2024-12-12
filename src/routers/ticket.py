from fastapi import APIRouter, Depends, HTTPException
from src.dependencies.auth import authenticate_token
from src.database.models.ticket import Ticket
from src.models.user import UserResponse
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.dependencies.ticket import get_qrcode

router = APIRouter(tags=["Ticket"])

@router.get("/ticket/{id}")
def get_ticket_qrcode(id: int, db:Session = Depends(get_db), user: UserResponse = Depends(authenticate_token)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == id).first()
    if not ticket.user_id == user.user_id:
        raise HTTPException(status_code=403, detail="El ticket no es suyo")
    
    return get_qrcode(ticket.qr_code)