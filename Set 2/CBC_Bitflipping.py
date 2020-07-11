from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64

def xor (b, c): 
    d = b''
    for a1, a2 in zip (b, c):
        d += bytes([a1^a2])
    return(d)

def ecb_decode(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.decrypt(text))

def ecb_encode(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.encrypt(text))

def pad (text):
    global BS
    l = len(text)
    ps = BS - l%BS
    if ps==0: ps = BS
    p = (chr(ps)*ps).encode()
    return text+p

def padding_val(string):
    ps = string[-1]
    for a in range(ps):
        if(string[-(a+1)]!=ps):
            raise Exception("Boo")
    return (string[:-ps])

def cbc_decode(text):
    global IV
    global BS
    global key
    de = bytearray(len(text))
    pt = IV
    for a in range (0, len(text), BS):
        de[a:a+BS] = xor(pt, ecb_decode(text[a:a+BS], key))
        pt = text[a:a+BS]
    de = padding_val(de)
    return(de)

def cbc_encode(text):
    global IV
    global BS
    global key
    pt = IV
    en = bytearray(len(text))
    for a in range (0, len(text), BS):
        en[a:a+BS] = ecb_encode(xor(text[a:a+BS], pt), key)
        pt = en[a:a+BS]
    return (en)

def func1 (string):
    string = string.replace(";", "%3b").replace("=", "%3d")
    s1 = "comment1=cooking%20MCs;userdata="
    s2 = ";comment2=%20like%20a%20pound%20of%20bacon"
    ns = s1 + string + s2
    ipt = pad(bytearray(ns, 'utf-8'))
    result = cbc_encode(ipt)
    return result

def func2 (result):
    text = cbc_decode(result)
    pos = text.find(b';admin=true;')
    if(pos==-1): return False
    return True

def bs (result):
    length = len(result)
    a = 1
    l = length
    while (l<=length):
        d = "A"*a
        l = len(func1(d))
        a = a + 1
    return (l-length)


def brk():
    result = func1("")
    BS = bs(result)
    pre = 32
    inp = "A"*((pre%BS)+BS) + "AadminAtrue" 
    result1 = func1(inp)
    result1[pre] = result1[pre]^ord("A")^ord(";")
    result1[pre+6] = result1[pre+6]^ord("A")^ord("=")
    print(func2(result1))


BS = 16
key = b'YELLOW SUBMARINE'
IV = Random.get_random_bytes(BS)
brk()
