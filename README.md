# Ticket-Flow
### **Objetivo**

Crear un sistema backend que permita a los usuarios gestionar eventos y generar entradas digitales con códigos QR que puedan ser validados en la entrada del evento.

---

### **Especificaciones Técnicas**

---

### **1. Funcionalidades Principales**

1. **Gestión de Usuarios**:
    - Registro e inicio de sesión de usuarios (administradores y asistentes).
    - Roles: administrador (creador de eventos) y asistente (comprador de entradas).
2. **Gestión de Eventos**:
    - CRUD de eventos por los administradores.
    - Atributos del evento: título, descripción, lugar, fecha y hora, número de entradas disponibles.
3. **Compra de Entradas**:
    - Registro de entradas compradas por asistentes.
    - Generación automática de códigos QR únicos para cada entrada.
    - Visualización del historial de entradas compradas.
4. **Validación de Entradas**:
    - Endpoint para validar el QR en la entrada del evento.
    - Estado de la entrada: activa, usada o inválida.

---

### **2. Estructura de Datos**

1. **Base de Datos**:
    - **Usuarios**: ID, nombre, correo, contraseña (hash), rol.
    - **Eventos**: ID, título, descripción, lugar, fecha, hora, entradas disponibles, administrador_ID.
    - **Entradas**: ID, usuario_ID, evento_ID, código_QR, estado (activa/usada).
2. **Endpoints**:
    - `/register` y `/login` - Registro e inicio de sesión.
    - `/events` (GET, POST, PUT, DELETE) - Gestión de eventos.
    - `/events/{id}/tickets` (POST) - Compra de entradas.
    - `/tickets/{qr_code}/validate` (POST) - Validación de entrada.

---

### **Tecnologías**

- **Lenguaje**: Python.
- **Framework Backend**: FastAPI.
- **Base de Datos**: MySQL.
- **Generación de Códigos QR**: Biblioteca `qrcode`.
- **Autenticación**: JWT (JSON Web Tokens) para proteger los endpoints.
- **Servidor de Despliegue**: Heroku, Render o AWS.
- **Documentación de API**: Swagger o FastAPI Docs.

---

### **Extras Opcionales**

- **Notificaciones**: Correo electrónico al usuario con la entrada y el código QR.
- **Panel de Administración**: Dashboard para listar eventos y estadísticas (por ejemplo, entradas vendidas por evento).
- **Integración de Pagos**: Uso de Stripe o PayPal para simular compras reales.
