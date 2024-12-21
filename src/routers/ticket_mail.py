from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema
from src.dependencies.auth import authenticate_token
from src.models.user import UserResponse
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.dependencies.ticket import get_qr_upload_file, get_ticket
from src.config import conf


#router = APIRouter(tags=["Mail"])

fm = FastMail(conf)

#@router.post("/ticket/{id}/send", status_code=200, response_description="Correo enviado exitosamente")
async def send_ticket(id: int, db:Session, user: UserResponse): #= Depends(get_db), user: UserResponse = Depends(authenticate_token)):
    ticket = get_ticket(id, user, db)
    qr_upload_file = get_qr_upload_file(ticket.qr_code)

    message = MessageSchema(
        subject="¡Gracias por tu compra!",
        recipients=[user.email],
        body=f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Hola {user.username},</h2>
            <p>Gracias por tu compra en <strong>Ticket Flow</strong>. Aquí tienes los detalles de tu compra:</p>
            <ul>
                <li><strong>Ticket ID:</strong> {ticket.ticket_id}</li>
                <li><strong>Evento:</strong> {ticket.event.title}</li>
                <li><strong>Lugar:</strong> {ticket.event.place}</li>
                <li><strong>Dia:</strong> {ticket.event.date}</li>
                <li><strong>Hora:</strong> {ticket.event.time}</li>
            </ul>
            <p>Adjuntamos tu ticket con el código QR.</p>
            <p>Si tienes dudas, responde a este correo o contáctanos en <a href="mailto:ticketflow1@gmail.com">ticketflow1@gmail.com</a>.</p>
            <p>¡Gracias por elegirnos!<br>El equipo de <strong>Ticket Flow</strong></p>
        </body>
        </html>
        """,
        subtype="html",
        attachments=[qr_upload_file]
    )
    try:
        await fm.send_message(message)
        return {"message": f"¡Gracias por su compra! Su ticket fue enviado a la direccion de correo electronico '{user.email}'"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo enviar el correo: {e}")