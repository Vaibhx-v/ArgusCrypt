import os
import time
from datetime import datetime

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from key_manager import generate_salt, derive_key
from file_handler import read_file, write_file


MAGIC_HEADER = b"AGCT"
VERSION = 1
ALGORITHM_ID = 1  # 1 = AES-256-GCM


def encrypt_file(file_path, password):
    """
    Encrypt a file using AES-256-GCM.

    Returns a dictionary containing encryption metadata.
    """

    start_time = time.perf_counter()

    data, path = read_file(file_path)

    salt = generate_salt()
    key = derive_key(password, salt)

    nonce = os.urandom(12)

    aes = AESGCM(key)

    ciphertext = aes.encrypt(
        nonce,
        data,
        None
    )

    extension = path.suffix.encode()

    extension_length = len(extension).to_bytes(1, "big")

    timestamp = int(time.time()).to_bytes(8, "big")

    final_data = (
        MAGIC_HEADER +
        VERSION.to_bytes(1, "big") +
        ALGORITHM_ID.to_bytes(1, "big") +
        timestamp +
        extension_length +
        extension +
        salt +
        nonce +
        ciphertext
    )

    os.makedirs("encrypted", exist_ok=True)

    output_file = f"encrypted/{path.stem}.enc"

    write_file(output_file, final_data)

    elapsed = round(time.perf_counter() - start_time, 3)

    return {
        "success": True,
        "message": "Encryption Successful",
        "algorithm": "AES-256-GCM",
        "input_file": str(path),
        "output_file": output_file,
        "original_size": len(data),
        "encrypted_size": len(final_data),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time_taken": elapsed
    }


def decrypt_file(file_path, password):
    """
    Decrypt an ArgusCrypt encrypted file.

    Returns a dictionary containing decryption metadata.
    """

    start_time = time.perf_counter()

    encrypted_data, path = read_file(file_path)

    if encrypted_data[:4] != MAGIC_HEADER:
        raise ValueError("Invalid ArgusCrypt encrypted file.")

    version = encrypted_data[4]

    if version != VERSION:
        raise ValueError("Unsupported file version.")

    algorithm = encrypted_data[5]

    if algorithm != ALGORITHM_ID:
        raise ValueError("Unsupported encryption algorithm.")

    timestamp_offset = 6

    extension_length_offset = timestamp_offset + 8

    extension_length = encrypted_data[extension_length_offset]

    extension_start = extension_length_offset + 1
    extension_end = extension_start + extension_length

    extension = encrypted_data[extension_start:extension_end].decode()

    salt_start = extension_end
    salt_end = salt_start + 16

    salt = encrypted_data[salt_start:salt_end]

    nonce_start = salt_end
    nonce_end = nonce_start + 12

    nonce = encrypted_data[nonce_start:nonce_end]

    ciphertext = encrypted_data[nonce_end:]

    key = derive_key(password, salt)

    aes = AESGCM(key)

    try:
        plaintext = aes.decrypt(
            nonce,
            ciphertext,
            None
        )

    except InvalidTag:
        return {
            "success": False,
            "message": "Incorrect password or corrupted file."
        }

    os.makedirs("decrypted", exist_ok=True)

    output_file = f"decrypted/{path.stem}_decrypted{extension}"

    write_file(output_file, plaintext)

    elapsed = round(time.perf_counter() - start_time, 3)

    return {
        "success": True,
        "message": "Decryption Successful",
        "algorithm": "AES-256-GCM",
        "input_file": str(path),
        "output_file": output_file,
        "decrypted_size": len(plaintext),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time_taken": elapsed
    }
