from datetime import timedelta
from dotenv import load_dotenv
import os
from fastapi_mail import ConnectionConfig

load_dotenv()

#Configuracion de conexion a base de datos
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

#Configuración JWT
ALGORITHM= os.getenv("ALGORITHM")
SECRET_KEY= os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRES_MINUTES = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")))

#Configuracion email
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("GMAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("GMAIL_PASSWORD"),
    MAIL_FROM=os.getenv("GMAIL_ADDRESS"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

#Configuración Mercado Pago
prod_access_token = os.getenv("PROD_ACCESS_TOKEN")

