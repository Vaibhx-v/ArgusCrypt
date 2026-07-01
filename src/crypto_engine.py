import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from key_manager import generate_salt, derive_key
from file_handler import read_file, write_file


def encrypt_file(file_path, password):
    """
    Encrypts a file using AES-256-GCM.
    """

    # Read image
    data, path = read_file(file_path)

    # Generate salt and key
    salt = generate_salt()
    key = derive_key(password, salt)

    # AES-GCM object
    aes = AESGCM(key)

    # Generate nonce
    nonce = os.urandom(12)

    # Encrypt data
    encrypted_data = aes.encrypt(
        nonce,
        data,
        None
    )

    # ---------- Custom File Format ----------

    magic = b"SIFT"

    version = bytes([1])

    extension = path.suffix.encode()

    extension_length = bytes([len(extension)])

    final_data = (
        magic
        + version
        + extension_length
        + extension
        + salt
        + nonce
        + encrypted_data
    )

    output_file = f"encrypted/{path.stem}.enc"

    write_file(output_file, final_data)

    return output_file


def decrypt_file(file_path, password):
    """
    Decrypts a SIFT encrypted file.
    """

    # Read encrypted file
    encrypted_data, path = read_file(file_path)

    # Verify magic header
    if encrypted_data[:4] != b"SIFT":
        raise ValueError("Invalid encrypted file.")

    # Read version
    version = encrypted_data[4]

    if version != 1:
        raise ValueError("Unsupported file version.")

    # Read extension length
    extension_length = encrypted_data[5]

    # Read extension
    start = 6
    end = start + extension_length

    extension = encrypted_data[start:end].decode()

    # Read salt
    salt_start = end
    salt_end = salt_start + 16

    salt = encrypted_data[salt_start:salt_end]

    # Read nonce
    nonce_start = salt_end
    nonce_end = nonce_start + 12

    nonce = encrypted_data[nonce_start:nonce_end]

    # Remaining data is ciphertext
    ciphertext = encrypted_data[nonce_end:]

    # Derive key
    key = derive_key(password, salt)

    # AES object
    aes = AESGCM(key)

    # Decrypt
    decrypted_data = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    # Restore filename
    output_file = (
        f"decrypted/{path.stem}_decrypted{extension}"
    )

    # Save image
    write_file(
        output_file,
        decrypted_data
    )

    return output_file