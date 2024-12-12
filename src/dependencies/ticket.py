import qrcode
import io
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from src.models.ticket import UserTicket
from src.database.models.ticket import Ticket
from src.models.user import UserResponse

def get_qrcode(content: str):
    qr_code = qrcode.make(content)
    buffer = io.BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

def get_tickets(user: UserResponse, db: Session):
    tickets = db.query(Ticket).filter(Ticket.user_id == user.user_id).all()
    tickets_list = [UserTicket(ticket_id=ticket.ticket_id, event=ticket.event.title) for ticket in tickets]
    return tickets_list