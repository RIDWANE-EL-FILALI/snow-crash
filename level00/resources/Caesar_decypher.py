import string

def caesar_cypher(cypher_text, shit):
    decrypted = ''
    for char in cypher_text:
        if char in string.ascii_lowercase:
            decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted += char
    return decrypted


cypher_text = "cdiiddwpgswtgt"

print("Trying all the shifts possible for caesar cypher :", cypher_text);
for shift in range(1, 26):
    decrypted = caesar_cypher(cypher_text, shift)
    print("shift {:2}: {}".format(shift, decrypted))
