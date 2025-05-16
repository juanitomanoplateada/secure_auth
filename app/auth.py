import os
import hashlib
import hmac
import secrets

HMAC_SECRET_KEY = b'super-secret-hmac-key'


def generate_salt() -> bytes:
    return secrets.token_bytes(16)


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)


def verify_password(password: str, salt: bytes, stored_hash: bytes) -> bool:
    new_hash = hash_password(password, salt)
    return hmac.compare_digest(new_hash, stored_hash)


def generate_hmac(message: str) -> str:
    return hmac.new(HMAC_SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()


def verify_hmac(message: str, received_token: str) -> bool:
    expected_token = generate_hmac(message)
    return hmac.compare_digest(expected_token, received_token)
