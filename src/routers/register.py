from fastapi import APIRouter


router = APIRouter()

@router.post("/register", tags=["Register"], status_code=201, response_description="Usuario creado exitosamente")
def register():
    pass