from fastapi import HTTPException
import qrcode
import io
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from src.models.ticket import UserTicket
from src.database.models.ticket import Ticket
from src.models.user import UserResponse
from starlette.datastructures import UploadFile as StarletteUploadFiles

def get_qrcode(content: str):
    qr_code = qrcode.make(content)
    buffer = io.BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


def get_qr_upload_file(content: str):
    qr_image = qrcode.make(content)
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    buffer.seek(0)
    qr_upload_file = StarletteUploadFiles(file=buffer, filename="ticket_qr.png") #Esta clase nos permite enviar archivos de tipo BinaryIO, indispensable para no crear archivos temporales
    return qr_upload_file


def get_tickets(user: UserResponse, db: Session):
    tickets = db.query(Ticket).filter(Ticket.user_id == user.user_id).all()
    tickets_list = [UserTicket(ticket_id=ticket.ticket_id, event=ticket.event.title) for ticket in tickets]
    return tickets_list


def get_ticket(id: int, user, db: Session):
    print(id)
    ticket = db.query(Ticket).filter(Ticket.ticket_id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="El ticket no existe")
    if not ticket.user_id == user.user_id:
        raise HTTPException(status_code=403, detail="El ticket no es suyo")
    
    return ticket