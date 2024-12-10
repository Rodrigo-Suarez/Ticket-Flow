from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from src.dependencies.auth import verify_admin, authenticate_token
from src.models.user import UserResponse
from src.models.event import CreateEvent, EventResponse, EventAdminResponse, GetEvents
from src.database.models.event import Event
from sqlalchemy.orm import Session
from src.database.db import get_db


router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", status_code=200, response_description="Respuesta exitosa", response_model= GetEvents)
def get_events(
    skip: int = Query(default=0, ge=0, description="Eventos a omitir"), 
    limit: int = Query(default=10, ge=1, le=20), 
    user: UserResponse = Depends(authenticate_token), 
    db: Session = Depends(get_db)
    ) -> GetEvents:

    events = db.query(Event).offset(skip).limit(limit).all()
    events_list = [EventResponse.model_validate(event) for event in events]
    
    return GetEvents(
        total_events= db.query(Event).count(),
        showed_events= len(events),
        events= events_list
    )


@router.get("/{id}", status_code=200, response_description="Respuesta exitosa")
def get_event():
    pass

@router.post("/", status_code=201, response_description="Evento creado exitosamente", response_model=EventAdminResponse)
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
    except Exception as e:
        raise HTTPException(status_code=422, detail="El evento no se pudo crear correctamente")
    
    db.commit()
    db.refresh(new_event)
    
    return new_event


@router.put("/{id}", status_code=200, response_description="Evento modificado exitosamente")
def put_event(id: int, admin: UserResponse = Depends(verify_admin)):
    pass

@router.delete("/{id}", status_code=204, response_description="Evento eliminado correctamente")
def delete_event(id: int, admin: UserResponse = Depends(verify_admin)):
    pass