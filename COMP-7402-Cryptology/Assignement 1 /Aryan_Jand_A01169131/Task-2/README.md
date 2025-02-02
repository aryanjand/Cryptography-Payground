# Modular Inverse Calculator with Extended Euclidean Algorithm

This Python script calculates the modular multiplicative inverse of two integers `a` and `b` using the Extended Euclidean Algorithm. It also includes a set of unit tests to verify the correctness of the implementation.

## Features

- **Extended Euclidean Algorithm**: Computes the greatest common divisor (gcd) of two integers `a` and `b` while also finding coefficients `x` and `y` such that:  
  `a * x + b * y = gcd(a, b)`.
- **Modular Inverse Calculation**: Determines the modular inverse of `a` modulo `b` if it exists, i.e., if `gcd(a, b) = 1`. If no inverse exists, the script will return `None`.

- **User Input**: Allows the user to enter values for `a` and `b` and displays the results of the modular inverse calculation.

- **Unit Tests**: Provides several test cases that verify the correctness of the algorithm for various input values.

## How it Works

The script has the following functions:

1. **`egcd(a, b)`**: Implements the Extended Euclidean Algorithm to compute `gcd(a, b)` and returns the coefficients `x` and `y` such that `a * x + b * y = gcd(a, b)`.

2. **`modInv(a, b)`**: Calculates the modular inverse of `a` modulo `b` using the result from `egcd`. If `gcd(a, b) != 1`, the inverse does not exist and `None` is returned.

3. **`calculateModularMultiplicativeInverse(a, b)`**: Accepts two integers `a` and `b`, calculates their modular inverse (if it exists), and prints the results to the console.

4. **`main()`**: A simple interface to accept user input for `a` and `b` and perform the modular inverse calculation.

## Running the Script

1. Clone or download the script.
2. Run the script:
   ```bash
   python task2.py
   ```

## Example Output

Enter value for a: 43
Enter value for b: 17

--- Calculation Results ---
Given values: a = 43, b = 17
gcd(43, 17) = 1
Integers x, y such that 43*x + 17*y = gcd(43, 17): x = 2, y = -5
Modular Inverse of 43 modulo 17 is: 38
