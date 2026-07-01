from crypto_engine import encrypt_file, decrypt_file


def main():

    print("=" * 40)
    print(" Secure Image Tool ")
    print("=" * 40)

    print("1. Encrypt Image")
    print("2. Decrypt Image")

    choice = input("\nEnter choice: ")

    password = input("Enter Password: ")

    if choice == "1":

        file_path = "test_images/1.jpg"

        encrypted_file = encrypt_file(
            file_path,
            password
        )

        print("\nEncryption Successful!")
        print(encrypted_file)

    elif choice == "2":

        file_path = "encrypted/1.enc"

        decrypted_file = decrypt_file(
            file_path,
            password
        )

        print("\nDecryption Successful!")
        print(decrypted_file)

    else:

        print("Invalid choice.")


if __name__ == "__main__":
    main()