from crypto_engine import encrypt_file


def main():

    file_path = "test_images/1.jpg"

    password = input("Enter Password: ")

    encrypted_file = encrypt_file(
        file_path,
        password
    )

    print("\n========================================")
    print("Encryption Successful")
    print("========================================")

    print("Encrypted File:")
    print(encrypted_file)


if __name__ == "__main__":
    main()