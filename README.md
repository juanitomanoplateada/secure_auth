# 🔐 SecureAuth – Autenticación segura con Hash, Sal y HMAC

SecureAuth es un sistema de autenticación backend desarrollado con **FastAPI**, **SQLAlchemy** y **PostgreSQL**, que implementa mecanismos modernos de seguridad como:

- 🔑 Hashing de contraseñas con **PBKDF2-HMAC-SHA256**
- 🧂 Generación de **sal aleatoria** por usuario
- ✅ Validación de integridad de credenciales mediante **HMAC**
- 🧠 API documentada automáticamente con OpenAPI/Swagger
- 🚀 Desplegado en Railway (backend y frontend)

---

## 🚀 Tecnologías utilizadas

| Componente   | Tecnología |
|--------------|------------|
| Backend API  | FastAPI    |
| Base de datos| PostgreSQL |
| ORM          | SQLAlchemy |
| Auth segura  | HMAC + SAL |
| Servidor     | Uvicorn    |
| Entorno      | Python 3.11 (Docker) |
| Frontend     | Angular 18 (repositorio separado) |

---

## 📁 Estructura del proyecto

```text
.
├── auth.py            # Funciones de hashing, sal y HMAC
├── main.py            # API REST con endpoints de registro y login
├── models.py          # Modelo ORM de usuario
├── database.py        # Configuración de SQLAlchemy y conexión
├── Dockerfile         # Imagen para despliegue en Railway
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación
```

---

## 🔐 Endpoints principales

- `POST /register` – Registro seguro con hash + sal
- `POST /login` – Inicio de sesión validando HMAC y hash
- `POST /generate-hmac` – Genera HMAC para validación desde frontend
- `GET /` – Verificación de estado del servidor

---

## 🔒 Seguridad aplicada

- Cada contraseña se transforma en hash mediante `PBKDF2-HMAC-SHA256` con 100.000 iteraciones.
- Cada usuario tiene su propia **sal aleatoria de 16 bytes**.
- El **token HMAC** asegura la integridad de las credenciales durante el envío.
- El backend nunca almacena ni transmite contraseñas en texto plano.
- Variables sensibles como `HMAC_SECRET_KEY` y `DATABASE_URL` se cargan mediante `.env`.

---

## ⚙️ Variables de entorno requeridas

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/db
HMAC_SECRET_KEY=kept-you-waiting-huh?
```

---

## 🐳 Uso con Docker

```bash
docker build -t secure-auth-backend .
docker run -e DATABASE_URL=... -e HMAC_SECRET_KEY=... -p 8000:8000 secure-auth-backend
```

---

## 🧪 Pruebas del backend

Puedes probar los endpoints directamente desde `http://localhost:8000/docs` gracias a la interfaz automática de Swagger.

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la **MIT License**.
