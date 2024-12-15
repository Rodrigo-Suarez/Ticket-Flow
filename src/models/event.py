from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as Date, time as Time

class CreateEvent(BaseModel):
    title: str  = Field(max_length=50)
    description: str
    place: str = Field(max_length=50)
    date: Date
    time: Time
    avaiable_tickets: int = Field(default=0)
    price: float = Field(default=0)

class EventResponse(CreateEvent):
    class Config:
        from_attributes =True

class EventAdminResponse(CreateEvent):
    event_id: int
    administrador_id: int

    class Config:
        from_attributes = True

class UpdateEvent(BaseModel):
    title: Optional[str]  = Field(None, max_length=50)
    description: Optional[str] = None
    place: Optional[str] = Field(None, max_length=50)
    date: Optional[Date] = None
    time: Optional[Time] = None
    avaiable_tickets: Optional[int] = None
    price: float = Field(default=0)

    class Config:
        from_attributes = True


class GetEvents(BaseModel):
    total_events: int 
    showed_events: int            
    events: list  

class AdminEvent(BaseModel):
    event_id: int
    event: str