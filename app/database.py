from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# -------------------------------------------------------------------------
# Carga las variables de entorno definidas en un archivo .env (si existe).
# Esto permite manejar credenciales y configuraciones sin exponerlas en el código.
load_dotenv()

# -------------------------------------------------------------------------
# Obtiene la URL de conexión a la base de datos desde una variable de entorno.
# Formato esperado (PostgreSQL):
# postgresql://usuario:contraseña@host:puerto/nombre_base_datos
DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------------------------------------------------------
# Crea el motor de conexión con SQLAlchemy usando la URL proporcionada.
# Este motor se reutiliza para ejecutar consultas a la base de datos.
engine = create_engine(DATABASE_URL)

# -------------------------------------------------------------------------
# Configura una clase de sesión local. Las sesiones creadas con SessionLocal()
# se usarán para interactuar con la base de datos dentro de cada petición.
#
# autocommit=False → se requiere llamar manualmente a db.commit().
# autoflush=False → los cambios no se envían automáticamente a la base.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
