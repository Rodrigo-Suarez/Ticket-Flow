from fastapi import APIRouter, Depends
from src.dependencies.auth import authenticate_token
from src.models.user import UserResponse
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.dependencies.ticket import get_qrcode, get_ticket


router = APIRouter(tags=["Ticket"])


@router.get("/ticket/{id}")
def get_ticket_qrcode(id: int, db:Session = Depends(get_db), user: UserResponse = Depends(authenticate_token)):
    ticket = get_ticket(id, user, db)
    return get_qrcode(ticket.qr_code)

