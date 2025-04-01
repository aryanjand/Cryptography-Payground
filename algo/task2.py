import os
from abc import ABC, abstractmethod
from task1 import PseudoNumberGenerator
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, encrypted_text: bytes) -> bytes:
        pass


class Cryptography:

    def __init__(self, algorithm: str, key_size: int, mode: str):
        key_bytes = self._key_generator(key_size)
        cipher_mode = self._get_mode(mode)
        self.strategy = self.__get_strategy(algorithm, key_bytes, cipher_mode)

    def __get_strategy(self, algorithm: str, key: int, mode: tuple[bytes, CBC]):
        if algorithm.lower() == "aes":
            return AESStrategy(key, mode)
        elif algorithm.lower() == "des":
            raise ValueError("DES encryption algorithm not support yet.")

    def _key_generator(self, key_size: int):
        prng = PseudoNumberGenerator(key_size)
        key_int = prng.blum_blum_shub()
        return key_int.to_bytes(key_size // 8, "big")

    def _get_mode(self, mode: str):
        if mode.upper() == "CBC":
            iv = os.urandom(16)
            return (iv, modes.CBC(iv))
        else:
            raise ValueError("Only CBC mode is support.")


class AESStrategy(EncryptionStrategy):

    def __init__(self, key: bytes, mode: tuple[bytes, CBC]):
        super().__init__()
        self._key = key
        self._mode = mode

    def encrypt(self, plaintext: bytes, key: bytes = None) -> bytes:

        # Create Cipher
        iv, cbc_mode = self._mode
        key_to_use = key or self._key

        cipher = Cipher(algorithms.AES(key_to_use), cbc_mode)
        encryptor = cipher.encryptor()

        # Pad the plaintext to be a multiple of the AES block size (128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Encrypt the padded plaintext
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Return IV + ciphertext together
        return iv + ciphertext

    def decrypt(self, data: bytes, key: bytes = None) -> bytes:

        # Extract IV from the first 16 bytes
        iv = data[:16]
        ciphertext = data[16:]
        key_to_use = key or self._key

        # Create Cipher
        cipher = Cipher(algorithms.AES(key_to_use), modes.CBC(iv))
        decryptor = cipher.decryptor()

        # Decrypt
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the plaintext
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext


if __name__ == "__main__":
    # Creating a Cryptography object with AES algorithm, key size of 256, and CBC mode
    crypto_aes = Cryptography("aes", 256, "cbc")

    # Declaration of Independence in plaintext (long input)
    declaration_text = """
    IN CONGRESS, July 4, 1776.
    The unanimous Declaration of the thirteen united States of America,
    
    When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation.
    
    We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness. That to secure these rights, Governments are instituted among Men, deriving their just powers from the consent of the governed, That whenever any Form of Government becomes destructive of these ends, it is the Right of the People to alter or to abolish it, and to institute new Government, laying its foundation on such principles and organizing its powers in such form, as to them shall seem most likely to effect their Safety and Happiness.
    
    Prudence, indeed, will dictate that Governments long established should not be changed for light and transient causes; and accordingly all experience hath shewn that mankind are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing the forms to which they are accustomed. But when a long train of abuses and usurpations, pursuing invariably the same Object evinces a design to reduce them under absolute Despotism, it is their right, it is their duty, to throw off such Government, and to provide new Guards for their future security.
    """

    # Encrypting the recipe using AES encryption
    cipher_text = crypto_aes.strategy.encrypt(declaration_text.encode())

    # Decrypting the encrypted recipe back to plaintext
    decrypted_text = crypto_aes.strategy.decrypt(cipher_text)

    # Printing the cipher text (encrypted recipe) and the decrypted recipe
    print("Plaintext:\n", declaration_text)
    print("\nCipher Text (Encrypted Recipe):\n", cipher_text)
    print("\n\nDecrypted Text (Recipe After Decryption):\n", decrypted_text.decode())
