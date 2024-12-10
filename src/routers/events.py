from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from src.dependencies.auth import verify_admin, authenticate_token
from src.models.user import UserResponse
from src.models.event import CreateEvent, EventResponse, EventAdminResponse, GetEvents, UpdateEvent
from src.database.models.event import Event
from sqlalchemy.orm import Session
from src.database.db import get_db


router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", status_code=200, response_description="Respuesta exitosa", response_model= GetEvents)
def get_events(
    skip: int = Query(default=0, ge=0, description="Eventos a omitir"), 
    limit: int = Query(default=10, ge=1, le=20, description="Eventos por pagina"),  
    db: Session = Depends(get_db)
    ) -> GetEvents:

    events = db.query(Event).offset(skip).limit(limit).all()
    events_list = [EventResponse.model_validate(event) for event in events]
    return GetEvents(
        total_events= db.query(Event).count(),
        showed_events= len(events),
        events= events_list
    )


@router.get("/search", status_code=200, response_description="Respuesta exitosa", response_model=GetEvents)
def get_event(
    name: str = Query(default="", min_length=0, description="Buscar: "),
    skip: int = Query(default=0, ge=0, description="Eventos a omitir"), 
    limit: int = Query(default=10, ge=1, le=20, description="Eventos por pagina"), 
    db: Session = Depends(get_db)) -> GetEvents:

    events = db.query(Event).filter(Event.title.like(f"%{name}%")).offset(skip).limit(limit).all()

    if not events:
        raise HTTPException(status_code=404, detail="No se encontro ningun evento")
    
    events_list = [EventResponse.model_validate(event) for event in events]
    return GetEvents(
        total_events= db.query(Event).filter(Event.title.like(f"%{name}%")).count(),
        showed_events= len(events),
        events= events_list
    )

@router.post("/create", status_code=201, response_description="Evento creado exitosamente", response_model=EventAdminResponse)
def post_event(event: CreateEvent, admin: UserResponse = Depends(verify_admin), db: Session = Depends(get_db)):
    new_event = Event(
        title = event.title,
        description = event.description,
        place = event.place,
        date = event.date,
        time = event.time,
        avaiable_tickets = event.avaiable_tickets,
        administrador_id = admin.user_id
    )

    try:
        db.add(new_event)
    except:
        raise HTTPException(status_code=422, detail="El evento no se pudo crear correctamente")
    
    db.commit()
    db.refresh(new_event)
    
    return new_event



@router.put("/", status_code=200, response_description="Evento modificado exitosamente")
def put_event(changed_event: UpdateEvent, id: int = Query(ge=1), admin: UserResponse = Depends(verify_admin), db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="No se encontro ningun evento")

    if not event.administrador.user_id == admin.user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder")

    to_update = changed_event.model_dump(exclude_unset=True) #Convierte el objeto event en un diccionario excluyendo los campos no definidos
    for key, value in to_update.items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    return EventResponse.model_validate(event)


@router.delete("/{id}", status_code=204, response_description="Evento eliminado correctamente")
def delete_event(id: int, admin: UserResponse = Depends(verify_admin)):
    pass