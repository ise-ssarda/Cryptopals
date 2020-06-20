string1 = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
key = "ICE"
l1 = len(string1)
rkey1 = (key * (l1//len(key)+ 1))[:l1]
b1 = bytes(string1, 'utf-8')
k1 = bytes(rkey1, 'utf-8')
c1 = b''
for a1, a2 in zip (b1, k1):
    c1 += bytes([a1^a2])
c1 = c1.hex()
print(c1)
