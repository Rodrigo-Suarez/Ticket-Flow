from sqlalchemy import Enum, Integer, BLOB,Column, String, Text, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id = Column(Integer, autoincrement=True primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id")) 
    event_id = Column(Integer, ForeignKey("event.event_id"))
    qr_code = Column(BLOB, nullable=False)
    status = Column(Enum("activa", "usada"), nullable=False, default="activa")

    user = relationship("User", backref="tickets")
    event = relationship("Event", backref="tickets")