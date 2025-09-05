# 📜 Level00 Writeup

## Level Overview

**Category:** Password / Cipher Cracking

**Description:**  
The challenge requires finding the password for `flag00`. During the filesystem investigation, we discovered files owned by `flag00`:

```bash
ls -la $(find / -user flag00 2>/dev/null)
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /rofs/usr/sbin/john
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
```
Inspecting these files revealed a string:
```
cdiiddwpgswtg
```

## Analysis
### **Why it is not a hashed password**

1. Length: 13 characters. Standard hashes like MD5 (32), SHA-1 (40), SHA-256 (64), or bcrypt (60) are much longer.

2. Character set: Only lowercase letters. Standard hashes use hexadecimal (`0-9, a-f`) or Base64 `(A-Z, a-z, 0-9, +, /, =)`.

3. Letter repetition: Characters repeat (`i` appears 3x, `d` twice), indicating structure, unlike fully random hashes.

✅ Conclusion: Not a standard hashed password.

### **Why it is not modern encryption**

1. Character set restriction: Only lowercase letters; modern encryption outputs usually include uppercase, digits, and symbols when Base64-encoded.

2. Length: Too short for modern encryption outputs, which include padding.

3. Structured repetition: Suggests a simple, classical cipher rather than a randomized ciphertext.

✅ Conclusion: Not modern encryption.

### **Likely candidates: Classical Ciphers**

Based on the analysis, the string is most likely a classical letter-based cipher:

| Cipher Type         | Reasoning                                                    |
| ------------------- | ------------------------------------------------------------ |
| Caesar / ROT-n      | Simple shifts; consistent lowercase letters; repetition fits |
| Vigenère            | Repeating key may cause letter patterns                      |
| Simple substitution | Each letter maps to another; repetition patterns remain      |
| Transposition       | Rearranges letters but preserves the character set           |

### Cracking Process

We suspected a Caesar cipher due to the structure and letter set. A Python script was written to try all possible shifts:

```python
import string

def caesar_cipher(cipher_text, shift):
    decrypted = ''
    for char in cipher_text:
        alphabet_index = ord(char) - ord('a')
        alphabet_index = (alphabet_index + shift) % 26
        decrypted += chr(ord('a') + alphabet_index)
    return decrypted

cipher_text = "cdiiddwpgswtg"

for shift in range(1, 26):
    print(f"shift {shift:2}: {caesar_cipher(cipher_text, shift)}")
```
From testing all 25 shifts, the only meaningful plaintext produced was:
```
************* 
```

## Conclusion

The string `"cdiiddwpgswtg"` was not a hashed password nor modern encryption, but a Caesar cipher. By performing a full shift analysis, we successfully decrypted the password:

**Flag / Password:**
```
*************
```
