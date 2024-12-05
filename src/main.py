from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from src.routers import login, register, events, ticket_purchase, ticket_validation
from src.database.db import Session
from sqlalchemy import text

app = FastAPI(title="Ticket Flow", version="Alpha")

@app.get("/", tags= ["Home"], status_code=200, response_description="Respuesta exitosa")
def home():
    return PlainTextResponse(content="home")

app.include_router(login.router)
app.include_router(register.router)
app.include_router(events.router)
app.include_router(ticket_purchase.router)
app.include_router(ticket_validation.router)

try:
    # Crear una sesión y probar
    session = Session()
    session.execute(text('INSERT INTO user (name, email, password, role) VALUES ("dadad", "ffffffffffa@gmail.com", "adadadd", "administrador" )'))  # Realizar una consulta básica
    print("Conexión exitosa a la base de datos")
    session.commit()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    session.close()


"""
try:
    session = Session()
    print("Conexion a base de datos exitosa")

except Exception as e:
    raise f"{e}: No fue posible conectarse a base de datos"

finally:
    session.close()
"""