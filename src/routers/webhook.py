from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies.webhook import process_successful_payment
from src.database.db import get_db
import mercadopago
from src.config import prod_access_token

router = APIRouter(tags=["MercadoPago Webhook"])

sdk = mercadopago.SDK(prod_access_token)

@router.post("/webhook/mercadopago")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        # Extraer el cuerpo de la solicitud
        payload = await request.json()
        print("#############################################")
        print(payload)
        print("#############################################")
        topic = payload.get("type")
        print("#############################################")
        print(topic)
        print("#############################################")
        resource_id = payload.get("data", {}).get("id")
        print("#############################################")
        print(resource_id)
        print("#############################################")
        if topic == "payment":
            # Obtener la información del pago desde MercadoPago
            payment_info = sdk.payment().get(resource_id)
            if payment_info["status"] != 200:
                raise HTTPException(status_code=400, detail="No se pudo obtener la información del pago")
            print("#############################################")
            print(payment_info)
            print("#############################################")
            payment_data = payment_info["response"]
            print("#############################################")
            print(payment_data)
            print("#############################################")
            payment_status = payment_data["status"]
            print("#############################################")
            print(payment_status)
            print("#############################################")
            external_reference = payment_data.get("external_reference")
            print("#############################################")
            print(external_reference)
            print("#############################################")

            if not external_reference:
                raise HTTPException(status_code=400, detail="No se encontró el external_reference")

            # Separar event_id y user_id del external_reference
            event_id, user_id = map(int, external_reference.split("|"))
            print("#############################################")
            print(event_id, user_id)
            print("#############################################")

            # Validar el estado del pago
            if payment_status == "approved":
                # Procesar el pago exitoso
                await process_successful_payment(event_id, user_id, db)

            elif payment_status in ["pending", "in_process"]:
                # Aquí no se realiza ninguna lógica, solo un mensaje de confirmación
                return {"message": "Pago pendiente o en proceso"}
            
            elif payment_status in ["cancelled", "rejected"]:
                # Aquí tampoco se realiza ninguna lógica
                return {"message": "Pago cancelado o rechazado"}
            else:
                raise HTTPException(status_code=400, detail="Estado de pago desconocido")

        return {"message": "Webhook recibido correctamente"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
