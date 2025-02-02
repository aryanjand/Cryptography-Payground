# DES Encryption and Avalanche Criterion Analysis

This project implements the **Data Encryption Standard (DES)** algorithm in Python, providing encryption and decryption functionalities along with an analysis of the **Strict Plaintext Avalanche Criterion (SPAC)** and **Strict Key Avalanche Criterion (SKAC)**.

## Features

- **DES Encryption & Decryption**: Implements the Feistel network-based DES algorithm.
- **Hexadecimal and Binary Operations**: Converts between hex and binary, performs XOR, and applies bit permutations.
- **Avalanche Criterion Analysis**: Evaluates how small changes in plaintext or key affect ciphertext.
- **Unit Testing**: Includes multiple test cases to validate DES encryption and decryption.

## Prerequisites

Ensure you have **Python 3.13** installed on your system.

## Installation

Clone this repository and navigate to the project folder:

No additional dependencies are required beyond Python’s standard library.

## Usage

Run the DES encryption program with default or user-provided values:

```sh
python task1.py
```

### Example Usage

```
Enter plaintext (default: 02468aceeca86420):
Enter initial key (default: 0f1571c947d9e859):
Enter operation (0 for encryption, 1 for decryption, default: 0):

Cipher Text: da02ce3a89ecac3b
```

## Code Breakdown

### DES Algorithm

The DES algorithm follows a **Feistel cipher** structure with 16 rounds of encryption. It utilizes **bitwise permutations**, **substitutions**, and **XOR operations** to transform plaintext into ciphertext. The process includes:

- **Key Scheduling**: Generates 16 round keys using permutation and shifting.
- **Feistel Rounds**: Applies XOR, expansion, S-box substitutions, and P-box permutations.
- **Initial and Final Permutation**: Uses predefined tables to scramble bits.
- **Mangler Function**: Implements the core transformations in each round.

### Avalanche Analysis

- **SPAC (Strict Plaintext Avalanche Criterion)**: Measures ciphertext changes due to small plaintext modifications.
- **SKAC (Strict Key Avalanche Criterion)**: Measures ciphertext changes due to small key modifications.

## Unit Tests

Run unit tests using:

```sh
python -m unittest task1.py
```

### Test Cases

- **Basic Encryption/Decryption Tests**
- **Edge Cases (All 0s, All 1s, Alternating Bits, Empty Strings)**

## License

This project is licensed under the **MIT License**.

## Author

Developed by **Aryan Jand**.
