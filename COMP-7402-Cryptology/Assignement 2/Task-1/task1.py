from typing import List
import unittest

BLOCK_SIZE = 64
SUB_KEY_SIZE = 56
KEY_SIZE = 64
KEY_SIZE_HEX = 16
NUM_OF_ROUNDS = 16

ENCRYPTION = 0
DECRYPTION = 1

# Initial Permutation (IP) Table
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Inverse Initial Permutation (IP-1) Table
IP_Inverse = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# E Bit-Selection Table
E_BOX = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation Table (Transposition)
P_BOX = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# Substation Table (Keyed Substitution)
S_BOX = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC_2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SIGNAL_SHIFTS = [1, 2, 9, 16]

res_key1 = ['c147b7f20e8659a2', 'e8659a2f0c61544', 'f0c6154445660417', '4566041764d7f086', '64d7f0860edf1e09', 'edf1e0909d88877', '9d88877c73c014c', 'c73c014cfca22a7c', 'fca22a7c4428a615', '4428a6153b7c11ac', '3b7c11aca785084e', 'a785084e268d842e', '268d842e06e3aacd', '6e3aacde8bdc6f0', 'e8bdc6f06bf7efc5', '6bf7efc546d0c86c']
res_key2 = ['c147b7f20e06dba2', 'e06dba291ab054c', '91ab054cd345013a', 'd345013a947c314d', '947c314d4e037854', '4e03785462e76d9f', '62e76d9f6ba059f7', '6ba059f7ef37e54e', 'ef37e54e6f5ecddc', '6f5ecddc9bf3d456', '9bf3d456ed4337be', 'ed4337be3e2c1920', '3e2c1920b1483801', 'b14838011df7f049', '1df7f04994e2e036', '94e2e036f63b884e']

res_plaintext1 = ['c147b7f20e8659a2', 'e8659a2f0c61544', 'f0c6154445660417', '4566041764d7f086', '64d7f0860edf1e09', 'edf1e0909d88877', '9d88877c73c014c', 'c73c014cfca22a7c', 'fca22a7c4428a615', '4428a6153b7c11ac', '3b7c11aca785084e', 'a785084e268d842e', '268d842e06e3aacd', '6e3aacde8bdc6f0', 'e8bdc6f06bf7efc5', '6bf7efc546d0c86c']
res_plaintext2 = ['c147b7f20e865922', 'e865922e2d6354d', 'e2d6354d4a6899d0', '4a6899d09ff12ec6', '9ff12ec672496fec', '72496fecb73768d9', 'b73768d90bcb003f', 'bcb003f0f4067e8', 'f4067e86977a0ab', '6977a0ab8dc092e7', '8dc092e74b6a4425', '4b6a44258452a0aa', '8452a0aac2d1a3d3', 'c2d1a3d3c95d9d54', 'c95d9d54ccc221e1', 'ccc221e164c3c8a1']

plaintext = plaintext1 = 'ed2b3d054a1fb68f'
plaintext2 = 'ed2b3d054a1fb68e'

key = key1 = '6977cf2a4c11e480'
key2 = '6977cf2a4c11e490'

round = []

def is_hex(value: str) -> bool:
    return all(c in '0123456789ABCDEFabcdef' for c in value)

def split_into_16_bit_words(hex_str: str):
    return [hex_str[i:i+16] for i in range(0, len(hex_str), 16)]

def pad_zero_bits(word: str) -> str:
    return word.zfill(16)

def hex_to_bin(hex_str: str) -> str:
    return f'{int(hex_str, 16):0{len(hex_str) * 4}b}'

def bin_to_hex(binary_str: str) -> str:
    return f'{int(binary_str, 2):x}'

def permute(block: str, table: List[int]) -> str:
    return ''.join(block[i-1] for i in table)

def xor(a: str, b: str):
    return f'{int(a, 2) ^ int(b, 2):0{len(a)}b}'

def bit_diff_count(hex1: str, hex2: str):
    bin1 = hex_to_bin(hex1)
    bin2 = hex_to_bin(hex2)
    
    # Calculate number of different bits (Hamming distance)
    diff_bits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    return diff_bits


def s_box(right_block: str) -> str:
    res = ''
    for i in range(8):
        sub_str = right_block[i * 6:i * 6 + 6]
        row = int(sub_str[0] + sub_str[-1], 2)
        column = int(sub_str[1:5], 2)
        res += f'{S_BOX[i][row][column]:04b}'
    return res 


# half_key is 28 bits long, n_shift is the number of shifts
def left_shift(half_key: str, n_shift: int) -> str: 
    return half_key[n_shift:] + half_key[:n_shift]


def key_scheduler(initial_key: str, operation: int) -> str:
    round_keys = []
    sub_key = permute(initial_key, PC1)         
    C0, D0 = sub_key[:SUB_KEY_SIZE // 2], sub_key[SUB_KEY_SIZE // 2:]

    for i in range(NUM_OF_ROUNDS):
        num_shifts = 2
        if (i + 1) in SIGNAL_SHIFTS:
            num_shifts = 1
        
        C0, D0 = left_shift(C0, num_shifts), left_shift(D0, num_shifts)
        round_key = permute(C0+D0, PC_2)

        round_keys.append(round_key)

    return round_keys if operation == ENCRYPTION else round_keys[::-1]


# right_block is 32-bits, and round key is 48 bits
def mangler_function(right_block: str, round_key: str):
    
    expansion_permutation = permute(right_block, E_BOX)

    xor_with_round_key = xor(expansion_permutation, round_key)

    s_box_output = s_box(xor_with_round_key)

    p_box_output = permute(s_box_output, P_BOX)
    
    return p_box_output

# block is 64 bits long, and round_keys is 48 bits
def feistel_rounds(block: str, round_keys: List[str]) -> str:
    left_half, right_half = block[:BLOCK_SIZE // 2], block[BLOCK_SIZE // 2:]
    
    for round_key in round_keys:
        temp = right_half
        right_half = xor(left_half, mangler_function(right_half, round_key))
        left_half = temp
        # round.append(bin_to_hex(left_half+right_half))
    
    return right_half + left_half


def des(plaintext: str, initial_key: str, operation: int):

    if len(initial_key) != KEY_SIZE_HEX or len(plaintext) == 0:
        return None
    
    if not (is_hex(plaintext) and is_hex(initial_key)):
        return None
    
    # Break plaintext into 16-character chunks
    plaintext_chunks = split_into_16_bit_words(plaintext)
    initial_key_bin = hex_to_bin(initial_key)
    
    cipher_text = ''
    round_keys = key_scheduler(initial_key_bin, operation)  # Key Scheduling
    
    for chunk in plaintext_chunks:
        plaintext_bin = hex_to_bin(pad_zero_bits(chunk))  # Pad if needed
        initial_permutation = permute(plaintext_bin, IP)  # Initial Permutation
        product_cipher = feistel_rounds(initial_permutation, round_keys)  # 16 rounds
        inverse_initial_permutation = permute(product_cipher, IP_Inverse)  # Inverse IP
        cipher_text += bin_to_hex(inverse_initial_permutation)

    return pad_zero_bits(cipher_text)


def main():
    plaintext = input('Enter plaintext (default: 02468aceeca86420): ').strip() or '02468aceeca86420'
    initial_key = input('Enter initial key (default: 0f1571c947d9e859): ').strip() or '0f1571c947d9e859'
    operation = input('Enter operation (0 for encryption, 1 for decryption, default: 0): ').strip()
    operation = int(operation) if operation.isdigit() else ENCRYPTION
    
    cipher_text = des(plaintext, initial_key, operation)
    print(f'\nCipher Text: {cipher_text}\n')

def task2():
    # print(round)
    ## SPAC
    print("\nSPAC - Strict Plaintext Avalanche Criterion")
    print(f"Plaintext 1: {plaintext1}")
    print(f"Plaintext 2: {plaintext2}")
    print(f"Key Used:    {key}\n")

    print("Round | Ciphertext 1          | Ciphertext 2          | Bit Diff")
    print("-------------------------------------------------------------")

    for i in range(NUM_OF_ROUNDS):
        SPAC = bit_diff_count(res_plaintext1[i], res_plaintext2[i])
        print(f"{i+1:<5} | {res_plaintext1[i]} | {res_plaintext2[i]} | {SPAC}")

    ## SKAC
    print("\nSKAC - Strict Key Avalanche Criterion")
    print(f"Plaintext:  {plaintext}")
    print(f"Key 1:      {key1}")
    print(f"Key 2:      {key2}\n")

    print("Round | Ciphertext 1          | Ciphertext 2          | Bit Diff")
    print("-------------------------------------------------------------")

    for i in range(NUM_OF_ROUNDS):
        SKAC = bit_diff_count(res_key1[i], res_key2[i])
        print(f"{i+1:<5} | {res_key1[i]} | {res_key2[i]} | {SKAC}")

class DESEncryptionTest(unittest.TestCase):

    def testcase_1(self):
        plaintext = '02468aceeca86420'
        key = '0f1571c947d9e859'
        expected_ciphertext = 'da02ce3a89ecac3b'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 1')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 1')

    def testcase_2(self):
        plaintext = '0123456789abcdef'
        key = '133457799bbcdff1'
        expected_ciphertext = '85e813540f0ab405'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 2')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 2')
        
    def testcase_3(self):
        plaintext = '1111111111111111'
        key = '1111111111111111'
        expected_ciphertext = 'f40379ab9e0ec533'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 3')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 3')

    def testcase_4(self):
        plaintext = '0000000000000000'
        key = '0000000000000000'
        expected_ciphertext = '8ca64de9c1b123a7'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 4')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 4')

    def testcase_5(self):
        plaintext = 'ffffffffffffffff'
        key = 'ffffffffffffffff'
        expected_ciphertext = '7359b2163e4edc58'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 5')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 5')

    def testcase_6(self):
        plaintext = '0123456789abcdef'
        key = 'ffffffffffffffff'
        expected_ciphertext = '6dce0dc9006556a3'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 6')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 6')

    def testcase_7(self):
        plaintext = '8000000000000000'
        key = '0101010101010101'
        expected_ciphertext = '95f8a5e5dd31d900'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 7')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 7')

    def testcase_8(self):
        plaintext = 'aaaaaaaaaaaaaaaa'
        key = '5555555555555555'
        expected_ciphertext = '343a09f9b2cb5cca'
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertEqual(result, expected_ciphertext, 'Encryption failed for test case 8')
        decrypted = des(result, key, DECRYPTION)
        self.assertEqual(decrypted, plaintext, 'Decryption failed for test case 8')
    
    def testcase_9(self):
        plaintext = ''
        key = ''
        
        result = des(plaintext, key, ENCRYPTION)
        self.assertIsNone(result, 'Encryption failed for test case 9')
        decrypted = des(result, key, DECRYPTION)
        self.assertIsNone(decrypted, 'Decryption failed for test case 9')

if __name__ == '__main__':
    main()
    task2()
    unittest.main()
