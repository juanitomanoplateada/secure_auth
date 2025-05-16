# ----------------------------------------------------------------------
# Usa una imagen ligera de Python 3.11 optimizada para producción.
FROM python:3.11-slim

# ----------------------------------------------------------------------
# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# ----------------------------------------------------------------------
# Copia todo el contenido del proyecto al directorio de trabajo del contenedor.
COPY . /app

# ----------------------------------------------------------------------
# Instala las dependencias necesarias para ejecutar el backend.
# --no-cache-dir evita almacenar archivos temporales para reducir tamaño.
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------
# Comando por defecto que ejecuta el servidor FastAPI usando Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
