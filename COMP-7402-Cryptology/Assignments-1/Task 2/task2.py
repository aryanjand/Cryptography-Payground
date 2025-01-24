import unittest

def egcd(a: int, b: int):
    if b < a:
        a, b = b, a

    x0, x1 = 1, 0 
    y0, y1 = 0, 1

    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0

def modInv(a: int, b: int):
    gcd, x, _ = egcd(a, b)
    if gcd != 1:
        return None
    return x % a

def calculateModularMultiplicativeInverse(a: int, b: int):
    # 1. Integer a is going to be the modulus
    # 2. A non-negative integer b that is less than a

    print("\n--- Calculation Results ---")
    print(f"Given values: a = {a}, b = {b}")

    gcd, x, y = egcd(a, b)
    print(f"gcd({a}, {b}) = {gcd}")
    print(f"Integers x, y such that {a}*x + {b}*y = gcd({a}, {b}): x = {x}, y = {y}")
    
    result = modInv(a, b)
    if result is not None:
        print(f"Modular Inverse of {a} modulo {b} is: {result}")
    else:
        print(f"Modular Inverse does not exist for a = {a} and b = {b} (gcd(a, b) != 1)")
    
    return gcd, x, y

def main():
    a = int(input("Enter value for a: "))
    b = int(input("Enter value for b: "))
    calculateModularMultiplicativeInverse(a, b)
    

class TestExtendedEuclideanAlgorithm(unittest.TestCase):

    def testcase_1(self):
        a, b = 43, 17
        gcd, x, y = egcd(a, b)
        self.assertEqual(gcd, 1)
        self.assertEqual(a * y + b * x, gcd)
        result = modInv(a, b)
        self.assertEqual(result, 38)

    def testcase_2(self):
        a, b = 12, 8
        gcd, x, y = egcd(a, b)
        self.assertEqual(gcd, 4)
        self.assertEqual(a * y + b * x, gcd)
        result = modInv(a, b)
        self.assertIsNone(result)

    def testcase_3(self):
        a, b = 43, 1
        gcd, x, y = egcd(a, b)
        self.assertEqual(gcd, 1)
        self.assertEqual(a * y + b * x, gcd)
        result = modInv(a, b)
        self.assertEqual(result, 1)

    def testcase_4(self):
        a, b = 123456789, 98765432
        gcd, x, y = egcd(a, b)
        self.assertEqual(gcd, 1)
        self.assertEqual(a * y + b * x, gcd)  
        result = modInv(a, b)
        self.assertEqual(result, 92592593)

    def testcase_5(self):
        a, b = 25, 25
        gcd, x, y = egcd(a, b)
        self.assertEqual(gcd, 25)
        self.assertEqual(a * y + b * x, gcd)
        result = modInv(a, b)
        self.assertIsNone(result) 



if __name__ == '__main__':
    main()
    unittest.main()
