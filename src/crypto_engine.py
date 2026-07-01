import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from key_manager import generate_salt, derive_key
from file_handler import read_file, write_file


def encrypt_file(file_path, password):
    """
    Encrypts a file using AES-256-GCM.
    """

    # Step 1: Read the image
    data, path = read_file(file_path)

    # Step 2: Generate a random salt
    salt = generate_salt()

    # Step 3: Derive a 256-bit AES key
    key = derive_key(password, salt)

    # Step 4: Create AES-GCM object
    aes = AESGCM(key)

    # Step 5: Generate a 12-byte nonce
    nonce = os.urandom(12)

    # Step 6: Encrypt the file bytes
    encrypted_data = aes.encrypt(
        nonce,
        data,
        None
    )

    # Step 7: Combine everything
    final_data = salt + nonce + encrypted_data

    # Step 8: Output filename
    output_file = f"encrypted/{path.stem}.enc"

    # Step 9: Save encrypted file
    write_file(output_file, final_data)

    return output_file