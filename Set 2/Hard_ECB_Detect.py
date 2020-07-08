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

def ecb_decode(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.decrypt(text))

def chunky(pot, BS):
    chunks = [pot[a:a+BS].hex() for a in range(0, len(pot), BS)]
    return (chunks)

def dup(chunks):
    um = set()
    for chunk in chunks:
        if chunk in um:
            return True
        else:
            um.add(chunk)
    return False

def detect_ecb(res, BS):
    if dup(chunky(res, BS)): return True
    return False

def pad (text, BS):
    l = len(text)
    ps = BS - l%BS
    if ps==0: ps = BS
    p = (chr(ps)*ps).encode()
    return text+p

def bs (result):
    length = len(result)
    a = 1
    l = length
    while (l<=length):
        d = bytearray("A"*a, 'utf-8')
        l = len(encryption_oracle(d))
        a = a + 1
    return (l-length)

def dictionary(act, ipt, BS, c, blk):
    dic = {}
    moo = act[0: c*BS]
    for a in range (127):
        text = ipt+bytearray(blk+chr(a), 'utf-8')
        rt = encryption_oracle(text)[0:c*BS]
        if (moo == rt):
            return (chr(a))

def bytes_prefix(BS):
    text = bytearray("", 'utf-8')
    result = encryption_oracle(text)
    text = bytearray("A", 'utf-8')
    while(result[0:BS]!=encryption_oracle(text)[0:BS]):
        result = encryption_oracle(text)
        text = text + bytearray("A", 'utf-8')
    return text[:-1].decode('utf-8')

def encryption_oracle(text):
    BS = 16
    global key
    global prefix
    global string
    text = prefix + text + string
    text = pad(text, BS)
    result = ecb_encode(text, key)
    return (result)

def decryption_oracle(result, text):
    BS = bs(result)
    val = len(result)-len(text)-BS
    c = 2
    blk = ''
    B = BS
    txt = ''
    if (detect_ecb(result, BS)):
        pre = bytes_prefix(BS)
        while (len(blk)<val-1):
            ipt = bytearray(pre+"A"*(B-1), 'utf-8')
            nc = dictionary(encryption_oracle(ipt), ipt, BS, c, blk)
            blk = blk + nc
            B = B-1
            if (B == 0):
                c = c+1
                B = BS
    return (blk)


key = Random.get_random_bytes(16)
prefix = Random.get_random_bytes(random.randint(1, 16))
string = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK")
cipher_text = open('12.txt').read()
text = bytearray(cipher_text, 'utf-8')
result = encryption_oracle(text)
print(decryption_oracle(result, text))
