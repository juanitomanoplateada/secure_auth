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
| Frontend     | Angular 18 (en repositorio separado) |

---

## 🔒 Características de seguridad

- Las contraseñas **nunca se almacenan ni transmiten en texto plano**.
- Cada contraseña es protegida con una **sal única de 16 bytes**.
- Las peticiones de login se validan con un **token HMAC** para garantizar que no hayan sido alteradas.
- Claves HMAC y URL de la base de datos se gestionan por medio de **variables de entorno**.

---
