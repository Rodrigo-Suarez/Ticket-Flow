from fastapi import APIRouter


router = APIRouter(tags=["Ticket Validation"])

@router.post("/tickets/{qr_code}/validate", status_code=200, response_description="Ticket válido y acceso permitido")
def register(qr_code: int):
    pass