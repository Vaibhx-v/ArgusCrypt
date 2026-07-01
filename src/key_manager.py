import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_salt():
    """
    Generates a secure random salt.
    """
    salt = os.urandom(16)
    return salt


def derive_key(password, salt):
    """
    Derives a secure AES-256 key from the user's password.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = kdf.derive(password.encode())

    return key