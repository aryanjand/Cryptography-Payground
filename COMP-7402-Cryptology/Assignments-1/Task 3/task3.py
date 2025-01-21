def digraphs(plaintext: str):
    condensed_text = plaintext.upper().replace(' ', '')
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


def playfair_cipher(keyword: str, plaintext: str):
    matrix = [['' for _ in range(5)] for _ in range(5)]
    digraphs_list = digraphs(plaintext)

    print(digraphs_list)
    pass

def main():
    pass

if __name__ == '__main__':
    main()
