from fastapi import APIRouter


router = APIRouter(tags=["Ticket Purchase"])

@router.post("/events/{id}/tickets", status_code=201, response_description="Compra de ticket exitosa, ticket generado")
def purchase_ticket(id: int):
    pass