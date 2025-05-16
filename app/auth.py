import os
import hashlib
import hmac
import secrets

# 🔐 Clave secreta para generar y verificar HMAC.
# Se espera que esté definida en una variable de entorno para mayor seguridad.
# Ejemplo en .env: HMAC_SECRET_KEY=kept-you-waiting-huh?
HMAC_SECRET_KEY = os.environ["HMAC_SECRET_KEY"].encode()


# -----------------------------------------------------------------------------
# 🔸 Función: generate_salt
# -----------------------------------------------------------------------------
# Genera una sal (salt) aleatoria de 16 bytes para proteger cada contraseña
# con un valor único y no predecible.
# Esto evita ataques con tablas arcoíris y mejora la seguridad del hash.
def generate_salt() -> bytes:
    return secrets.token_bytes(16)


# -----------------------------------------------------------------------------
# 🔸 Función: hash_password
# -----------------------------------------------------------------------------
# Genera un hash seguro de una contraseña utilizando el algoritmo PBKDF2-HMAC
# con SHA-256, usando la sal proporcionada y 100.000 iteraciones.
#
# Parámetros:
# - password (str): Contraseña en texto plano.
# - salt (bytes): Sal única para ese usuario.
#
# Retorna:
# - bytes: Hash de la contraseña.
def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)


# -----------------------------------------------------------------------------
# 🔸 Función: verify_password
# -----------------------------------------------------------------------------
# Verifica si una contraseña proporcionada coincide con el hash almacenado,
# aplicando la misma función de hash con la sal original.
#
# Parámetros:
# - password (str): Contraseña en texto plano ingresada por el usuario.
# - salt (bytes): Sal usada originalmente para generar el hash.
# - stored_hash (bytes): Hash almacenado en la base de datos.
#
# Retorna:
# - bool: True si la contraseña es válida, False si no lo es.
def verify_password(password: str, salt: bytes, stored_hash: bytes) -> bool:
    new_hash = hash_password(password, salt)
    return hmac.compare_digest(new_hash, stored_hash)


# -----------------------------------------------------------------------------
# 🔸 Función: generate_hmac
# -----------------------------------------------------------------------------
# Genera un código de autenticación de mensaje (HMAC) usando SHA-256
# y la clave secreta del servidor. Se usa para firmar mensajes sensibles
# como credenciales antes de enviarlos.
#
# Parámetros:
# - message (str): Texto a firmar (ej. "username:password").
#
# Retorna:
# - str: HMAC en formato hexadecimal.
def generate_hmac(message: str) -> str:
    return hmac.new(HMAC_SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()


# -----------------------------------------------------------------------------
# 🔸 Función: verify_hmac
# -----------------------------------------------------------------------------
# Verifica que un HMAC recibido coincida con el que debería haberse generado
# a partir del mensaje original.
#
# Parámetros:
# - message (str): Mensaje base usado para la firma.
# - received_token (str): Token HMAC recibido desde el cliente.
#
# Retorna:
# - bool: True si el token es válido, False si ha sido alterado.
def verify_hmac(message: str, received_token: str) -> bool:
    expected_token = generate_hmac(message)
    return hmac.compare_digest(expected_token, received_token)
