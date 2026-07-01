from key_manager import generate_salt, derive_key


def main():

    password = input("Enter Password: ")

    salt = generate_salt()

    key = derive_key(password, salt)

    print()

    print("=" * 40)
    print("Secure Image Tool")
    print("=" * 40)

    print("Password :", password)
    print("Salt     :", salt)
    print("Key      :", key)

    print()

    print("Key Length:", len(key), "bytes")


if __name__ == "__main__":
    main()