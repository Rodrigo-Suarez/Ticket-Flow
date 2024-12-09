from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
from src.routers import login, register, events, ticket_purchase, ticket_validation

app = FastAPI(title="Ticket Flow", version="Alpha")

@app.get("/", tags= ["Home"], status_code=200, response_description="Respuesta exitosa")
def home():
    return PlainTextResponse(content="Home")


app.include_router(login.router)
app.include_router(register.router)
app.include_router(events.router)
app.include_router(ticket_purchase.router)
app.include_router(ticket_validation.router)


@app.middleware("http")
async def httt_error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail={f"error: {e}"})