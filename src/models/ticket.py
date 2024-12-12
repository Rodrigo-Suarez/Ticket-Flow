from pydantic import BaseModel
from typing import Literal


class TicketResponse(BaseModel):
    response: str
    user: str
    event: str
    ticket_id: int