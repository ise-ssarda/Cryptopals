from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Random import random
import base64

def xor (b, c): 
    d = b''
    for a1, a2 in zip (b, c):
        d += bytes([a1^a2])
    return(d)

def ecb_encode(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.encrypt(text))

def cbc_encode(text, IV, BS, key):
    pt = IV
    en = bytearray(len(text))
    for a in range (0, len(text), BS):
        en[a:a+BS] = ecb_encode(xor(text[a:a+BS], pt), key)
        pt = en[a:a+BS]
    return (en)

def chunky(pot):
    chunks = [pot[a:a+16].hex() for a in range(0, len(pot), 16)]
    return (chunks)

def dup(chunks):
    um = set()
    for chunk in chunks:
        if chunk in um:
            return True
        else:
            um.add(chunk)
    return False

def pad (text, BS):
    l = len(text)
    ps = BS - l%BS
    if ps==0: ps = BS
    p = (chr(ps)*ps).encode()
    return text+p

def detect_ecb(res):
    if dup(chunky(res)): print ('Yay')

def encryption_oracle(text, BS):
    key = Random.get_random_bytes(BS)
    c = random.randint(1, 2)
    count = random.randint(5, 10)
    bts = Random.get_random_bytes(count)
    bts1 = Random.get_random_bytes(16 - count)
    text = bts + text + bts1
    if (c==1):
        result = ecb_encode(text, key)
    elif (c==2):
        IV = Random.get_random_bytes(16)
        result = cbc_encode(text, IV, BS, key)
    detect_ecb(result)
    print (c)
    return (result)


BS = 16
cipher_text = open('11.2.txt').read()
text = bytearray(cipher_text, 'utf-8')
text = pad(text, BS)
print(encryption_oracle(text, BS))
