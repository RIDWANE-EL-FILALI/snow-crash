# Level 00

**Objective:**  
Find the password for `flag00`.

**Analysis:**  
We searched in  the filesystem for files owned by `flag00`:

Among the results, we found a file `/usr/sbin/john` and `/rofs/usr/sbin/john` owned by `flag00`:
```
ls -la $(find / -user flag00 2>/dev/null)
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /rofs/usr/sbin/john
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
```

Inspecting the files revealed the following string: `cdiiddwpgswtg`

The text consisted entirely of lowercase letters, suggesting a substitution cipher. Given the uniform letter set, we suspected a **Caesar cipher**.

**Cracking Process:**  
We wrote a Python script to test all possible Caesar cipher shifts:

```python
import string

def caesar_cipher(cipher_text, shift):
    decrypted = ''
    for char in cipher_text:
        alphabet_index = ord(char) - ord('a')
        alphabet_index = (alphabet_index + number) % 26
        shifted_character = chr(ord('a') + alphabet_index)
        decrypted += shifted_character 
    return decrypted

cipher_text = "cdiiddwpgswtgt"

for shift in range(1, 25):
    print(f"shift {shift:2}: {caesar_cipher(cipher_text, shift)}")
```
From the 25 shifts we found the only meaninful string : `nottoohardhere`