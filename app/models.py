from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

# Declaración base para definir clases de modelos con SQLAlchemy ORM
Base = declarative_base()


# -------------------------------------------------------------------
# Modelo de usuario: representa la tabla 'users' en la base de datos
class User(Base):
    __tablename__ = "users"

    # ID autoincremental como clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre de usuario único, obligatorio y con índice para búsquedas rápidas
    username = Column(String, unique=True, index=True, nullable=False)

    # Correo electrónico del usuario (opcional)
    email = Column(String, nullable=True)

    # Sal aleatoria binaria utilizada para hashear la contraseña
    salt = Column(LargeBinary, nullable=False)

    # Hash de la contraseña protegida con la sal (usando PBKDF2-HMAC-SHA256)
    password_hash = Column(LargeBinary, nullable=False)
