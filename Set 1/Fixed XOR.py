hex_string1 = "1c0111001f010100061a024b53535009181c"
b1 = bytes.fromhex(hex_string1)
hex_string2 = "686974207468652062756c6c277320657965"
b2 = bytes.fromhex(hex_string2)
c = b''
for a1, a2 in zip (b1, b2):
    c += bytes([a1^a2])
c = c.hex()
print(c)
