from fastapi import APIRouter


router = APIRouter()

@router.post("/login", tags=["Login"], status_code=200, response_description="Ticket válido y acceso permitido")
def login():
    pass