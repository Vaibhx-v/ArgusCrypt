from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from key_manager import generate_salt, derive_key

from file_handler import read_file

def encrypt_file(file_path, password):
    pass