Ticket Flow 🎟️
Ticket Flow es una aplicación backend diseñada para la gestión eficiente de eventos y tickets digitales. Este proyecto implementa un sistema robusto y seguro para la compra, validación y administración de entradas, integrando tecnologías modernas y buenas prácticas de desarrollo.

🚀 Funcionalidades principales
🔐 Registro de usuarios: Gestión segura de datos con autenticación basada en JWT.
🎫 Compra de tickets: Generación automática de tickets con códigos QR únicos y sistema de pagos integrado mediante Mercado Pago.
📅 Gestión de eventos: Endpoints RESTful para crear, modificar y eliminar eventos.
✅ Validación de tickets: Verificación en tiempo real para controlar el acceso a eventos.
🛡️ Buenas prácticas de desarrollo: Validación de datos, uso adecuado de status codes HTTP y medidas de seguridad como encriptación de contraseñas.
💾 Base de datos relacional: Diseño e integración con MySQL para garantizar la integridad y consistencia de los datos.
🛠️ Tecnologías utilizadas
Lenguaje y Framework:
🐍 Python
FastAPI (desarrollo rápido y escalable de APIs RESTful)
Base de datos:
MySQL (modelado y persistencia de datos relacionales)
SQLAlchemy (ORM para interacción con la base de datos)
Autenticación:
JWT (tokens para sesiones seguras)
Documentación y pruebas:
Swagger (para probar y documentar la API)
Pagos integrados:
Mercado Pago (procesamiento seguro de pagos).

🚦 Cómo ejecutar el proyecto
Clona este repositorio:

bash
Copiar código
git clone https://github.com/tu-usuario/ticket-flow.git
cd ticket-flow
Configura el entorno virtual y las dependencias:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
Configura el archivo .env:

Crea un archivo .env en la raíz del proyecto con las siguientes variables:
php
Copiar código
DATABASE_URL=mysql+pymysql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>
MERCADOPAGO_ACCESS_TOKEN=<tu_token_de_acceso>
Ejecuta el servidor FastAPI:

bash
Copiar código
uvicorn app.main:app --reload
Prueba la API en Swagger:

Visita http://localhost:8000/docs para acceder a la documentación generada automáticamente.
📜 Licencia
Este proyecto se distribuye bajo la licencia MIT.

💡 Nota: Personaliza las secciones y variables del archivo .env según tu configuración específica. Si necesitas instrucciones adicionales o encuentras un problema, no dudes en abrir un issue.
