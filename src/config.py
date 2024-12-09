from dotenv import load_dotenv
import os

load_dotenv()

#Configuracion de conexion a base de datos
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

#Configuración JWT
ALGORITHM= os.getenv("ALGORITHM")
SECRET_KEY= os.getenv("SECRET_KEY")

