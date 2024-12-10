from fastapi import APIRouter



router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", status_code=200, response_description="Respuesta exitosa")
def get_events():
    pass

@router.get("/{id}", status_code=200, response_description="Respuesta exitosa")
def get_event(id: int):
    pass

@router.post("/", status_code=201, response_description="Evento creado exitosamente")
def post_event():
    pass

@router.put("/{id}", status_code=200, response_description="Evento modificado exitosamente")
def put_event(id: int):
    pass

@router.delete("/{id}", status_code=204, response_description="Evento eliminado correctamente")
def delete_event(id: int):
    pass