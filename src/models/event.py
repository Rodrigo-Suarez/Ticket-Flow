from pydantic import BaseModel, Field
from datetime import date, time

class CreateEvent(BaseModel):
    title: str  = Field(max_length=50)
    description: str
    place: str = Field(max_length=50)
    date: date
    time: time
    avaiable_tickets: int = Field(default=0)

class EventResponse(CreateEvent):
    class Config:
        from_attributes =True

class EventAdminResponse(CreateEvent):
    event_id: int
    administrador_id: int

    class Config:
        from_attributes = True


class GetEvents(BaseModel):
    total_events: int 
    showed_events: int            
    events: list  
