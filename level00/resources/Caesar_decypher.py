import string

def caesar_cipher(cipher_text, shift):
    decrypted = ''
    for char in cipher_text:
        alphabet_index = ord(char) - ord('a')
        alphabet_index = (alphabet_index + shift) % 26
        shifted_character = chr(ord('a') + alphabet_index)
        decrypted += shifted_character 
    return decrypted

cipher_text = "cdiiddwpgswtgt"

for shift in range(1, 26):
    print(f"shift {shift:2}: {caesar_cipher(cipher_text, shift)}")