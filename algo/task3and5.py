import time
from math import gcd
from task2 import Cryptography
from random import SystemRandom
from task1 import PseudoNumberGenerator


random = SystemRandom()


class RSAPublicCryptography:

    def keys_generator(self):
        """
        Returns: A tuple containing two elements:
                - public_key (tuple): The public key (e, n).
                - private_key (tuple): The private key (d, n).
        """
        prng = PseudoNumberGenerator(1024, is_prime=True)
        p, q = prng.blum_blum_shub(), prng.blum_blum_shub()

        while p == q:
            p = prng.blum_blum_shub()

        self._p = p
        self._q = q

        n = p * q
        phiN = (p - 1) * (q - 1)

        # Select e to be 1 < e < phiN
        e = random.randint(2, phiN - 1)
        while gcd(e, phiN) != 1:
            e = random.randint(2, phiN - 1)

        d = pow(e, -1, phiN)  # modular multiplicative inverse

        return (e, n), (d, n)

    def encrypt(self, keyPairs: tuple, message: int) -> int:
        e, n = keyPairs
        if message >= n:
            ValueError("Message can't be longer than N")
        return self._pow(message, e, n)
        # return message**e % n
        # return pow(message, e, n)

    def decrypt(self, keyPairs: tuple, message: int, crt=False) -> int:
        d, n = keyPairs
        if message >= n:
            ValueError("Message can't be longer than N")
        if crt is True:
            dp = d % (self._p - 1)
            dq = d % (self._q - 1)
            q_inv = pow(self._q, -1, self._p)  # modular multiplicative inverse

            m1 = self._pow(message, dp, self._p)
            m2 = self._pow(message, dq, self._q)
            h = (q_inv * (m1 - m2)) % self._p
            return m2 + h * self._q
        else:
            return self._pow(message, d, n)
            # return message**d % n
            # return pow(message, d, n)

    def _pow(self, base: int, exponent: int, modulus: int):
        if modulus == 1:
            return 0
        result = 1
        base = base % modulus
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus
        return result


if __name__ == "__main__":
    crypto_aes = Cryptography("aes", 256, "cbc")
    crypto_rsa = RSAPublicCryptography()

    aes_256_key = int.from_bytes(crypto_aes.strategy._key, "big")

    public_key, private_key = crypto_rsa.keys_generator()

    print("\n" + "=" * 100)
    print("🔑 AES Key (Message):")
    print(aes_256_key)
    print("=" * 100 + "\n")

    time.sleep(2)

    cipher = crypto_rsa.encrypt(public_key, aes_256_key)

    # Measure time for decryption without CRT
    start_time = time.time()
    decrypted_key_no_crt = crypto_rsa.decrypt(private_key, cipher)
    time_no_crt = time.time() - start_time

    # Measure time for decryption with CRT
    start_time = time.time()
    decrypted_key_with_crt = crypto_rsa.decrypt(private_key, cipher, crt=True)
    time_with_crt = time.time() - start_time

    print("\n" + "=" * 100)
    print("🛡️  Encrypted AES Key:")
    print(cipher)
    print("=" * 100 + "\n")

    print("\n" + "=" * 100)
    print("🔓 Decrypted AES Key (Without CRT):")
    print(decrypted_key_no_crt)
    print("=" * 100 + "\n")

    print("\n" + "=" * 100)
    print("🔓 Decrypted AES Key (With CRT):")
    print(decrypted_key_with_crt)
    print("=" * 100 + "\n")

    # Print time taken for decryption
    print("\n" + "=" * 100)
    print(f"⏱️ Time taken for decryption without CRT: {time_no_crt:.6f} seconds")
    print(f"⏱️ Time taken for decryption with CRT: {time_with_crt:.6f} seconds")
    print("=" * 100 + "\n")
