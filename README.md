# Ticket Flow 🎟️

**Ticket Flow** es una aplicación backend diseñada para la gestión eficiente de eventos y tickets digitales. Este proyecto implementa un sistema robusto y seguro para la compra, validación y administración de entradas, integrando tecnologías modernas y buenas prácticas de desarrollo.

## 🚀 Funcionalidades principales

- 🔒 **Registro de usuarios**: Gestión segura de datos con autenticación basada en **JWT**.  
- 🎛 **Compra de tickets**: Generación automática de tickets con **códigos QR únicos** y sistema de pagos integrado mediante **Mercado Pago**.  
- 📅 **Gestión de eventos**: Endpoints RESTful para crear, modificar y eliminar eventos.  
- ✅ **Validación de tickets**: Verificación en tiempo real para controlar el acceso a eventos.  
- 🛡️ **Buenas prácticas de desarrollo**: Validación de datos, uso adecuado de status codes HTTP y medidas de seguridad como encriptación de contraseñas.  
- 💿 **Base de datos relacional**: Diseño e integración con **MySQL** para garantizar la integridad y consistencia de los datos.

## 🛠️ Tecnologías utilizadas

- **Lenguaje y Framework:**  
  - 🐍 Python  
  - FastAPI (desarrollo rápido y escalable de APIs RESTful)  
- **Base de datos:**  
  - MySQL (modelado y persistencia de datos relacionales)  
  - SQLAlchemy (ORM para interacción con la base de datos)  
- **Autenticación:**  
  - JWT (tokens para sesiones seguras)  
- **Documentación y pruebas:**  
  - Swagger (para probar y documentar la API)  
- **Pagos integrados:**  
  - Mercado Pago (procesamiento seguro de pagos).  



## 🚦 Cómo ejecutar el proyecto

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/ticket-flow.git
   cd ticket-flow
   ```

2. **Configura el entorno virtual y las dependencias:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configura el archivo `.env`:**
   - Crea un archivo `.env` en la raíz del proyecto con las variables del archivo .env.example:

4. **Ejecuta el servidor FastAPI:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Prueba la API en Swagger:**
   - Visita `http://localhost:8000/docs` para acceder a la documentación generada automáticamente.

## 📜 Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).
