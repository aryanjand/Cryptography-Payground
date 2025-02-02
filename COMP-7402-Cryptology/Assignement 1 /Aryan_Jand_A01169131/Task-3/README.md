# Playfair Cipher Encryption

This Python script implements the Playfair cipher encryption method. The Playfair cipher is a digraph substitution cipher that encrypts pairs of letters using a 5x5 matrix of letters derived from a keyword.

## Features

- **Playfair Cipher Algorithm**: Encrypts messages using the Playfair cipher technique. The algorithm processes the message by creating digraphs (pairs of letters) and applying the cipher rules to generate the encrypted output.

- **Dynamic 5x5 Matrix**: The matrix is generated based on the provided keyword. The alphabet is modified by removing the letter 'J' (which is treated as 'I'), and then filling the matrix with the keyword letters (without duplicates) followed by the remaining letters of the alphabet.

- **User Input**: The script accepts user input for the keyword and plaintext message, and it prints the encrypted message.

- **Unit Tests**: Includes multiple test cases to verify the correctness of the cipher encryption and edge case handling.

## How it Works

The script consists of several key functions:

1. **`digraphs(plaintext)`**: Prepares the plaintext by:

   - Removing spaces and punctuation.
   - Converting all letters to uppercase.
   - Replacing 'J' with 'I'.
   - Dividing the text into digraphs (pairs of letters), and inserting filler 'X' when a pair consists of identical letters or if the total length is odd.

2. **`create_matrix(keyword)`**: Generates a 5x5 matrix used for encryption. The matrix is populated with letters from the provided keyword (with duplicates removed) followed by the remaining unused letters of the alphabet.

3. **`playfair_cipher(keyword, plaintext)`**: Encrypts the given plaintext using the Playfair cipher. It uses the matrix and digraphs generated earlier and applies the Playfair cipher rules to encrypt the message.

4. **`main()`**: A simple user interface to input the keyword and plaintext message and prints the encrypted message.

## Running the Script

1. Clone or download the script.
2. Run the script:
   ```bash
   python task3.py
   ```

## Example Output

**Input:**

```bash
Enter the key for the Playfair cipher: ballon
Enter the message to encrypt: world
```

Encrypted message:
YASAEW
