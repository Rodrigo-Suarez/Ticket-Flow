from src.models.user import UserResponse
from src.database.models.user import User
from src.database.models.event import Event
from src.database.models.ticket import Ticket
from src.dependencies.mail import send_ticket
from sqlalchemy.orm import Session
from datetime import datetime



def process_successful_payment(event_id: int, user_id: int, db: Session):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    print("#############################################")
    print(event)
    print("#############################################")
    user_db = db.query(User).filter(User.user_id == user_id).first()
    print("#############################################")
    print(user_db)
    print("#############################################")
    qr_data = f"user_id = {user_db.user_id}, event_id = {event.event_id}, creation_date = {datetime.now()}"
    
    new_ticket = Ticket(
        user_id = user_db.user_id ,
        event_id = event.event_id,
        qr_code = qr_data
    )
    
    user = UserResponse(
        user_id = user_db.user_id,
        username = user_db.username,
        email = user_db.email,
        role = user_db.role,
    )

    event.avaiable_tickets -= 1
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket) #Sincroniza la informacion entre la API y la Base de Datos
    
    response = send_ticket(new_ticket.ticket_id, db, user)
    return response

