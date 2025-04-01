from random import SystemRandom
from math import erfc
from math import sqrt
from math import log
from math import fabs
from math import gcd

random = SystemRandom()


class NISTRandomTests:

    @staticmethod
    def monobit_test(binary_data: str, verbose=False):
        binary_data_str_length = len(binary_data)
        sn = 0

        for bit in binary_data:
            if bit == "0":
                sn -= 1
            else:
                sn += 1

        sObs = sn / sqrt(binary_data_str_length)
        # Compute p-Value
        p_value = erfc(sObs / sqrt(2))

        if verbose:
            print("Frequency Test (Monobit Test) DEBUG BEGIN:")
            print("\tLength of input:\t", binary_data_str_length)
            print("\t# of '0':\t\t\t", binary_data.count("0"))
            print("\t# of '1':\t\t\t", binary_data.count("1"))
            print("\tS(n):\t\t\t\t", sn)
            print("\tsObs:\t\t\t\t", sObs)
            print("\tf:\t\t\t\t\t", fabs(sObs) / sqrt(2))
            print("\tP-Value:\t\t\t", p_value)
            print("DEBUG END.")

        # return a p_value and randomness result
        return (p_value, (p_value >= 0.01))

    @staticmethod
    def run_test(binary_data: str, verbose=False):
        binary_data_str_length = len(binary_data)
        # Predefined tau
        threshold = 2 / sqrt(binary_data_str_length)
        vObs = 0

        # Compute the proportion of ones in the input sequence: π = Σjεj / n
        count_ones = binary_data.count("1")
        count_zeros = binary_data.count("0")
        pi = count_ones / binary_data_str_length

        if abs(pi - 0.5) >= threshold:
            return (0.0000, False)

        for item in range(1, binary_data_str_length):
            if binary_data[item] != binary_data[item - 1]:
                vObs += 1
        vObs += 1

        p_value = erfc(
            abs(vObs - 2 * binary_data_str_length * pi * (1 - pi))
            / (2 * sqrt(2 * binary_data_str_length) * pi * (1 - pi))
        )

        if verbose:
            print("Run Test DEBUG BEGIN:")
            print("\tLength of input:\t\t\t\t", binary_data_str_length)
            print("\tTau (2/sqrt(length of input)):\t", threshold)
            print("\t# of '1':\t\t\t\t\t\t", count_ones)
            print("\t# of '0':\t\t\t\t\t\t", count_zeros)
            print("\tPI (1 count / length of input):\t", pi)
            print("\tvObs:\t\t\t\t\t\t\t", vObs)
            print("\tP-Value:\t\t\t\t\t\t", p_value)
            print("DEBUG END.")

        return (p_value, (p_value > 0.01))

    @staticmethod
    def statistical_test(binary_data: str, verbose=False):
        binary_data_str_length = len(binary_data)
        table = {}

        def getPrecomputedValues(binary_data_str_length: int):
            precomputed_map = {
                387_840: (6, 640, 5.2177052, 2.954),
                904_960: (7, 1280, 6.1962507, 3.125),
                2_068_480: (8, 2560, 7.1836656, 3.238),
                4_654_080: (9, 5120, 8.1764248, 3.311),
                10_342_400: (10, 10240, 9.1723243, 3.356),
                22_753_280: (11, 20480, 10.170032, 3.384),
                49_643_520: (12, 40960, 11.168765, 3.401),
                107_560_960: (13, 81920, 12.168070, 3.410),
                231_669_760: (14, 163840, 13.167693, 3.416),
                496_435_200: (15, 327680, 14.167488, 3.419),
                1_059_061_760: (16, 655360, 15.167379, 3.421),
            }

            for key in sorted(precomputed_map.keys(), reverse=True):
                if binary_data_str_length >= key:
                    return key, *precomputed_map[key]

            return None, None, None, None, None

        pattern_size, L, Q, expected_value, variance = getPrecomputedValues(
            binary_data_str_length
        )

        if pattern_size is None or not (5 <= pattern_size <= 16):
            return (0, False)

        K = binary_data_str_length // L - Q

        if K <= 0:
            return (0, False)

        c = 0.7 - 0.8 / L + (4 + 32 / L) * pow(K, -3 / L) / 15
        sigma = c * sqrt(variance / K)

        initialization_segment = binary_data[0 : Q * L]
        test_segment = binary_data[Q * L : (Q + K) * L]

        for i in range(0, Q * L, L):
            block_id = i // L + 1
            block = str(initialization_segment[i : i + L])

            if block not in table or table[block] < block_id:
                table[block] = block_id

        sum = 0
        for i in range(0, K * L, L):
            block_id = Q + i // L + 1
            block = str(test_segment[i : i + L])
            diff = block_id - table.get(block, 0)
            sum += log(diff, 2)
            table[block] = block_id

        fn = sum / K
        p_value = erfc((fn - expected_value) / (sqrt(2) * sigma))

        if verbose:
            print("Statistical DEBUG BEGIN:")
            print(f"\tLength of input: {binary_data_str_length}")
            print(f"\tPattern Size (L): {L}")
            print(f"\tThreshold (c): {c}")
            print(f"\tSigma (sigma): {sigma}")
            print(f"\tExpected Value: {expected_value}")
            print(f"\tVariance: {variance}")
            print(f"\tP-Value: {p_value}")
            print("DEBUG END.")

        return (p_value, p_value >= 0.01)


class PrimeGenerator:
    # Checks divisibility against small primes
    def __is_divisible_by_small_primes(self, candidate: int) -> bool:
        SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        if candidate < 2:
            return False

        for prime in SMALL_PRIMES:
            if candidate % prime == 0:
                return False
        return True

    # Miller-Rabin primality test
    def __is_miller_rabin_passed(self, candidate: int, trials=56):
        max_divisions_by_two, even_component = 0, candidate - 1

        while even_component % 2 == 0:
            even_component >>= 1
            max_divisions_by_two += 1

        def trialComposite(round_tester):
            if pow(round_tester, even_component, candidate) == 1:
                return False
            for i in range(max_divisions_by_two):
                if pow(round_tester, 2**i * even_component, candidate) == candidate - 1:
                    return False
            return True

        # Run the Miller-Rabin test with n trials
        for _ in range(trials):
            round_tester = random.randrange(2, candidate)
            if trialComposite(round_tester):
                return False
        return True

    # Is a probabilistic test to check for primes
    def is_prime_check(self, candidate: int):
        return self.__is_divisible_by_small_primes(
            candidate
        ) and self.__is_miller_rabin_passed(candidate)

    # Generate a prime of size N
    def generate(self, bitSize: int):
        lower, upper = (
            2 ** (bitSize - 2),
            2 ** (bitSize - 1) - 1,
        )
        while True:
            # lower ensure the number is odd and step 2, ensure we only generate prime numbers
            p = random.randrange(lower | 1, upper, 2)
            if self.is_prime_check(p) and p % 4 == 3:
                return p


class PseudoNumberGenerator:
    def __init__(self, bit_size: int, is_prime=False):
        self.__is_prime = is_prime
        self.__bit_size = bit_size
        self.__prime_generator = PrimeGenerator()

    def blum_blum_shub(self):
        MAX_ITERATIONS = 1000
        bit_size = self.__bit_size
        while True:
            prime_number_generator = self.__prime_generator.generate
            p, q = prime_number_generator(bit_size), prime_number_generator(bit_size)
            while p == q:
                p = prime_number_generator(bit_size)

            M = p * q
            seed = random.randint(2, 2 ** (bit_size // 2))

            while gcd(M, seed) != 1:
                seed = random.randint(2, 2 ** (bit_size // 2))

            # Generate sequence using BBS
            x = seed
            for _ in range(MAX_ITERATIONS):
                x = (x**2) % M
                if not self.__is_prime:
                    return x
                if self.__prime_generator.is_prime_check(x):
                    return x

    def liner_congruential(self):
        pass


if __name__ == "__main__":
    size_of_num = 1024  # Bit size of random number
    prng = PseudoNumberGenerator(size_of_num)
    NIST_tests = NISTRandomTests()

    monobit_pass = 0
    run_test_pass = 0
    statistical_test_pass = 0
    total_tests = 10

    for i in range(total_tests):
        random_prime_number = prng.blum_blum_shub()
        prime_number_binary = bin(random_prime_number)[2:]

        print(f"Random Number {i + 1}: ", random_prime_number)

        monobit_result = NIST_tests.monobit_test(prime_number_binary)
        run_test_result = NIST_tests.run_test(prime_number_binary)
        statistical_test_result = NIST_tests.statistical_test(prime_number_binary)

        if monobit_result[1]:
            monobit_pass += 1
        if run_test_result[1]:
            run_test_pass += 1
        if statistical_test_result[1]:
            statistical_test_pass += 1

    print("\nResults after 10 iterations:")
    print(
        f"Monobit Test Passed: {monobit_pass}/{total_tests} ({monobit_pass/total_tests*100:.2f}%)"
    )
    print(
        f"Run Test Passed: {run_test_pass}/{total_tests} ({run_test_pass/total_tests*100:.2f}%)"
    )
    print(
        f"Statistical Test Passed: {statistical_test_pass}/{total_tests} ({statistical_test_pass/total_tests*100:.2f}%)"
    )
