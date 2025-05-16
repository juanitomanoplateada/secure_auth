from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Importación de recursos internos del sistema
from app.database import SessionLocal
from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    generate_salt,
    generate_hmac,
    verify_hmac,
)

from fastapi.middleware.cors import CORSMiddleware

# ----------------------------------------------------------------------
# Inicialización de la aplicación FastAPI
app = FastAPI()

# ----------------------------------------------------------------------
# Middleware CORS: solo permite solicitudes del frontend autorizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://secure-auth-frontend-production.up.railway.app"],  # Frontend permitido
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------
# Dependencia de base de datos: cada petición abrirá una sesión segura
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------------------------
# Modelo de datos para el registro de usuarios
class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


# ----------------------------------------------------------------------
# Modelo de datos para el login de usuarios
class LoginRequest(BaseModel):
    username: str
    password: str
    hmac_token: str  # Token HMAC para validar integridad del mensaje


# ----------------------------------------------------------------------
# Endpoint básico para verificar si el servidor está activo
@app.get("/")
def root():
    return {"message": "Servidor activo"}


# ----------------------------------------------------------------------
# Registro seguro de un nuevo usuario
@app.post("/register")
def register(req: RegisterRequest, db: Session=Depends(get_db)):
    # Verifica si el usuario ya existe
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    # Genera sal y hash de la contraseña
    salt = generate_salt()
    hashed = hash_password(req.password, salt)

    # Crea nuevo usuario
    new_user = User(
        username=req.username,
        email=req.email,
        salt=salt,
        password_hash=hashed
    )
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado correctamente"}


# ----------------------------------------------------------------------
# Inicio de sesión seguro validado por HMAC y hash de contraseña
@app.post("/login")
def login(req: LoginRequest, db: Session=Depends(get_db)):
    # Busca el usuario
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verifica integridad del mensaje con HMAC
    message = f"{req.username}:{req.password}"
    if not verify_hmac(message, req.hmac_token):
        raise HTTPException(status_code=400, detail="HMAC inválido")

    # Verifica la contraseña ingresada
    if not verify_password(req.password, user.salt, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}


# ----------------------------------------------------------------------
# Endpoint expuesto para que el cliente obtenga el token HMAC válido
@app.post("/generate-hmac")
def generate_hmac_endpoint(req: LoginRequest):
    message = f"{req.username}:{req.password}"
    return {"hmac_token": generate_hmac(message)}
