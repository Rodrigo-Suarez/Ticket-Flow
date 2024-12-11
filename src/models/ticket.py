from pydantic import BaseModel
from typing import Literal


class Ticket(BaseModel):
    ticket_id: int
    user_id = int 
    event_id = int
    qr_code = str
    status = Literal["activa", "usada"]

    class Config:
        from_attributes = True