from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import base64

def xor (b, c): 
    d = b''
    for a1, a2 in zip (b, c):
        d += bytes([a1^a2])
    return(d)

def ecb_decode(text):
    key = b'YELLOW SUBMARINE'
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.decrypt(text))

BS = 16
cipher_text = open('10.txt').read()
text = base64.b64decode(cipher_text)
IV = bytes("0"*BS, 'utf-8')                               
de = bytearray(len(text))
pt = IV
for a in range (0, len(text), BS):
    de[a:a+BS] = xor(pt, ecb_decode(text[a:a+BS]))
    pt = text[a:a+BS]
print (de.decode('utf-8'))
    
