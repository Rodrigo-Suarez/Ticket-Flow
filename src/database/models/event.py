from sqlalchemy import Integer, Column, String, Text, Date, Time, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database.db import Base

class Event(Base):
    __tablename__ = "event"
    
    event_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    place = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    avaiable_tickets = Column(Integer, nullable=False, default=0)
    administrador_id = Column(Integer,ForeignKey("user.user_id"))
    price = Column(Float, nullable=False, default=0)

    administrador = relationship("User", backref="events")
    
