from fastapi import APIRouter, Depends, HTTPException

from src.models.ticket import TicketResponse
from src.database.models.ticket import Ticket
from src.dependencies.auth import verify_admin
from src.models.user import UserResponse
from src.database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Ticket Validation"])

@router.post("/tickets/{qr_code}/validate", status_code=200, response_description="Ticket válido y acceso permitido", response_model=TicketResponse)
def validate_ticket(qr_code: str, db: Session = Depends(get_db), admin: UserResponse = Depends(verify_admin)) -> TicketResponse:
    qr = db.query(Ticket).filter(Ticket.qr_code == qr_code).first()
    if not qr:
        raise HTTPException(status_code=404, detail="No se encontro ningun ticket")
    if not qr.event.administrador_id == admin.user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para validar este ticket")
    if qr.status == "usada":
        raise HTTPException(status_code=409, detail="Ticket usado")

    qr.status = "usada"
    db.commit()
    db.refresh(qr)

    return TicketResponse(
        response= "Ticket validado correctamente",
        user= qr.user.username,
        event= qr.event.title,
        ticket_id= qr.ticket_id
    )
