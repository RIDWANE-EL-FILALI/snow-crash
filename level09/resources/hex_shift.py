hex_string = "66 34 6b 6d 6d 36 70 7c 3d 82 7f 70 82 6e 83 82 44 42 83 44 75 7b 7f 8c 89" # string containing hex bytes 

hex_bytes = hex_string.split(" ") # split the hex_string by space

shift = 0;
for byte in hex_bytes:
    decimal = int(byte, 16) - shift # converting hex byte to its decimal form and subsctract shift from it
    character = chr(decimal) # converting the decimal form to ascii representaion
    print(character, end="")
    shift += 1









