from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
from src.routers import login, register, events, ticket_purchase, ticket_validation, ticket, webhook
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ticket Flow", version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (puedes limitarlo a dominios específicos)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)



@app.get("/", tags= ["Home"], status_code=200, response_description="Respuesta exitosa")
def home():
    return PlainTextResponse(content="Home")


app.include_router(login.router)
app.include_router(register.router)
app.include_router(events.router)
app.include_router(ticket_purchase.router)
app.include_router(ticket_validation.router)
app.include_router(ticket.router)
app.include_router(webhook.router)


@app.middleware("http")
async def httt_error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail={f"error: {e}"})
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)