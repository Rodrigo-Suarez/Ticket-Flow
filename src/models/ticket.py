from pydantic import BaseModel

class TicketResponse(BaseModel):
    response: str
    user: str
    event: str
    ticket_id: int

class UserTicket(BaseModel):
    ticket_id: int
    event: str
