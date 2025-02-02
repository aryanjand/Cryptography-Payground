import unittest

def digraphs(plaintext: str):
    # 4.  Remove spaces and punctuation
    condensed_text = plaintext.upper().replace('J', 'I')
    condensed_text = ''.join([char for char in condensed_text if char.isalpha()])

    text_with_filler = ''
    for i in range(len(condensed_text)):
        text_with_filler += condensed_text[i]

        if i < len(condensed_text) - 1 and condensed_text[i] == condensed_text[i + 1] and len(text_with_filler) % 2 != 0:
            text_with_filler += 'X'
    
    if len(text_with_filler) % 2 != 0:
        text_with_filler += 'X'

    res = [text_with_filler[i : i+2] for i in range(0, len(text_with_filler), 2)]
    
    return res

def create_matrix(keyword: str): 
    ROWS = COLS = 5
    a_to_z = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'J']

    matrix = [['' for _ in range(COLS)] for _ in range(ROWS)]
    keyword = keyword.upper().replace('J', 'I')
    new_keyword = ''

    for char in keyword:
        # 3. Remove duplicate from the keyword
        # 4. Remove spaces and punctuation
        if char.isalpha() and char not in new_keyword:
                new_keyword += char

    for char in a_to_z:
        if char not in new_keyword:
            new_keyword += char

    i = 0
    for r in range(ROWS):
        for c in range(COLS):
            matrix[r][c] = new_keyword[i]
            i += 1

    return matrix

def playfair_cipher(keyword: str, plaintext: str):
    if (keyword == None or plaintext == None):
        return None
    
    # 2. create 5x5 matrix
    ROWS = COLS = 5
    matrix = create_matrix(keyword)
    digraphs_list = digraphs(plaintext)
    r1 = r2 = c1 = c2 = None
    res = ''

    for digraph in digraphs_list:
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == digraph[0]:
                    r1, c1 = r, c
                if matrix[r][c] == digraph[1]:
                    r2, c2 = r, c
        if r1 == r2:
            res += matrix[r1][(c1 + 1) % COLS]
            res += matrix[r2][(c2 + 1) % COLS]
        elif c1 == c2:
            res += matrix[(r1 + 1) % ROWS][c1]
            res += matrix[(r2 + 1) % ROWS][c2]
        else:
            res += matrix[r1][c2]
            res += matrix[r2][c1]

    return res

def main():
    key = input('Enter the key for the Playfair cipher: ')
    message = input('Enter the message to encrypt: ')

    print('Encrypted message:')
    print(playfair_cipher(key, message))


class TestPlayfairCipher(unittest.TestCase):

    def testcase_1(self):
        key = ''
        message = ''
        res = playfair_cipher(key, message)
        expected_output = ''
        self.assertEqual(res, expected_output)
    
    def testcase_2(self):
        key = ''
        message = 'hello'
        res = playfair_cipher(key, message)
        expected_output = 'KCNVMP'  
        self.assertEqual(res, expected_output)
    
    def testcase_3(self):
        key = 'ballon'
        message = 'world'
        res = playfair_cipher(key, message)
        expected_output = 'YASAEW'
        self.assertEqual(res, expected_output)
    
    def testcase_4(self):
        key = 'MONARCHY monarchy'
        message = 'mosque'
        res = playfair_cipher(key, message)
        expected_output = 'ONTSML'  
        self.assertEqual(res, expected_output)
    
    def testcase_5(self):
        key = 'kingdom'
        message = 'hello world'
        res = playfair_cipher(key, message)
        expected_output = 'LFHYEBVMTFNZ'  
        self.assertEqual(res, expected_output)

    def testcase_6(self):
        key = 'playfair'
        message = 'jjj'
        res = playfair_cipher(key, message)
        expected_output = 'CUCUCU'  
        self.assertEqual(res, expected_output)
    
    def testcase_7(self):
        key = None
        message = 'message'
        res = playfair_cipher(key, message)
        self.assertIsNone(res)

    def testcase_8(self):
        key = 'keyword'
        message = None
        res = playfair_cipher(key, message)  
        self.assertIsNone(res)

if __name__ == '__main__':
    main()
    unittest.main()
