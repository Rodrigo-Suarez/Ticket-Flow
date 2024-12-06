from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from src.routers import login, register, events, ticket_purchase, ticket_validation
from src.database.db import Session
from sqlalchemy import text

app = FastAPI(title="Ticket Flow", version="Alpha")

@app.get("/", tags= ["Home"], status_code=200, response_description="Respuesta exitosa")
def home(request: Request):
    session = request.state.db
    consulta = session.execute(text("SELECT * FROM ticket_flow.user")).fetchall()
    resultado = [row._asdict() for row in consulta]
    return {"consulta": resultado}


app.include_router(login.router)
app.include_router(register.router)
app.include_router(events.router)
app.include_router(ticket_purchase.router)
app.include_router(ticket_validation.router)


@app.middleware("http")
async def get_db_connection(request: Request, call_next):
    try:
        session = Session()
        request.state.db = session
        response = await call_next(request)
        session.commit()
        print("Conexion exitosa a base de datos")
        return response
    
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return PlainTextResponse(content="Error interno en la conexión a la base de datos", status_code=500)
    
    finally:
        if session:
            session.close()
            print("Conexion a base de datos finalizada")

