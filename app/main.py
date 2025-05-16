from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Base, User
from app.auth import (
    hash_password,
    verify_password,
    generate_salt,
    generate_hmac,
    verify_hmac,
)

from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # 🚨 puedes usar ["*"] en pruebas, pero no en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class LoginRequest(BaseModel):
    username: str
    password: str
    hmac_token: str


@app.get("/")
def root():
    return {"message": "Servidor activo"}


@app.post("/register")
def register(req: RegisterRequest, db: Session=Depends(get_db)):
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    salt = generate_salt()
    hashed = hash_password(req.password, salt)

    new_user = User(
        username=req.username,
        email=req.email,
        salt=salt,
        password_hash=hashed
    )
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado correctamente"}


@app.post("/login")
def login(req: LoginRequest, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    message = f"{req.username}:{req.password}"
    if not verify_hmac(message, req.hmac_token):
        raise HTTPException(status_code=400, detail="HMAC inválido")

    if not verify_password(req.password, user.salt, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}


@app.post("/generate-hmac")
def generate_hmac_endpoint(req: LoginRequest):
    message = f"{req.username}:{req.password}"
    return {"hmac_token": generate_hmac(message)}

