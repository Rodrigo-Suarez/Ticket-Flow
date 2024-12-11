from sqlalchemy import Enum, Integer,Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False) 
    event_id = Column(Integer, ForeignKey("event.event_id"), nullable=False)
    qr_code = Column(String, nullable=False)
    status = Column(Enum("activa", "usada"), nullable=False, default="activa")

    user = relationship("User", backref="tickets")
    event = relationship("Event", backref="tickets")