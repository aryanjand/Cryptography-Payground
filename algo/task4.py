from task2 import Cryptography
from task3and5 import RSAPublicCryptography


def save_to_file(filename, data):
    """Save encrypted or decrypted data to a file."""
    with open(filename, "wb") as file:
        file.write(data)


if __name__ == "__main__":
    # Generate AES key
    crypto_aes = Cryptography("aes", 256, "cbc")
    crypto_rsa = RSAPublicCryptography()

    aes_key = int.from_bytes(crypto_aes.strategy._key)
    print("AES Key generated successfully.")

    # Generate RSA keys
    publicKey, privateKey = crypto_rsa.keys_generator()
    print("RSA Keys generated successfully.")

    # Encrypt AES key with RSA
    encrypted_key = crypto_rsa.encrypt(publicKey, aes_key)
    print("AES Key encrypted successfully.")

    # Read file data
    input_file = "./graphics-pixels-art.bmp"
    with open(input_file, "rb") as file:
        file_data = file.read()

    # Encrypt file data with AES
    encrypted_data = crypto_aes.strategy.encrypt(file_data)
    print("File encrypted successfully.")
    save_to_file("encrypted_file.bmp", encrypted_data)

    # Decrypt AES key
    decrypted_aes_key = crypto_rsa.decrypt(privateKey, encrypted_key)
    print("AES Key decrypted successfully.")

    # Decrypt file data
    decrypted_data = crypto_aes.strategy.decrypt(encrypted_data)
    print("File decrypted successfully.")
    save_to_file("decrypted_file.bmp", decrypted_data)

    print("Encryption and decryption process completed.")
