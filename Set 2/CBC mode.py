from Cryptodome.Cipher import AES
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

def ecb_encode(text):
    key = b'YELLOW SUBMARINE'
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.encrypt(text))

def cbc_decode(text, IV, BS):
    de = bytearray(len(text))
    pt = IV
    for a in range (0, len(text), BS):
        de[a:a+BS] = xor(pt, ecb_decode(text[a:a+BS]))
        pt = text[a:a+BS]
    return(de.decode('utf-8'))

def cbc_encode(text, IV, BS):
    sot = bytearray(text, 'utf-8')
    pt = IV
    en = bytearray(len(sot))
    for a in range (0, len(sot), BS):
        en[a:a+BS] = ecb_encode(xor(sot[a:a+BS], pt))
        pt = en[a:a+BS]


BS = 16
cipher_text = open('10.txt').read()
text = base64.b64decode(cipher_text)
IV = bytes("0"*BS, 'utf-8')                               
so = cbc_decode(text, IV, BS)
print (so)
