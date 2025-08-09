
# level 00
in this level just like any other ctf
we ran a search for the files owned by the user flag00

using

```
ls -la $(find / -user flag00 2>/dev/null)
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /rofs/usr/sbin/john
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
```

normal search for files owned by that specific user

after trying the key we got. the key was denied and after a certain time searching we found out that the key was encrypted using caecar cypher since all the characters where intact and readable

```
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
```

reshift the characters backward from 1 to 25 testing and found the right one in the 15th shift
