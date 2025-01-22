def egcd(a: int, b: int):
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
    
    return x % b

def main():
    a = int(input("Enter value for a: "))
    b = int(input("Enter value for b: "))
    
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
    
if __name__ == '__main__':
    main()
