from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Random import random

def equal_parse (text):
    first = ''
    second = ''
    dic = {}
    c = 0
    text = text.decode('utf-8')
    for a in range (len(text)):
        if (text[a]=='='):
            c = 1
            continue
        elif (text[a]=='&'):
            c = 0
            dic[first] = second
            first = ''
            second = ''
            continue
        if (c==0):
            first = first + text[a]
        elif(c==1):
            second = second + text[a]
    dic[first] = second
    return (dic)

def equal_encode(dic):
    en = ''
    for a, b in dic.items():
        en = en+a+'='+b+'&'
    return (en[:-1])
    
          
def profile_for(email):
    dic = {}
    email = email.replace("&", "")
    email = email.replace("=", "")
    dic['email'] = email
    dic['uid'] = '10'
    dic['role'] = 'user'
    en = equal_encode(dic)
    return (encryption_oracle(en))

def ecb_encode(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return(cipher.encrypt(text))

def ecb_decode(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return(equal_parse(cipher.decrypt(text)))

def pad (text, BS):
    l = len(text)
    ps = BS - l%BS
    if ps==0: ps = BS
    p = (chr(ps)*ps).encode()
    return text+p

def encryption_oracle(text):
    BS = 16
    global key
    text = bytearray(text, 'utf-8')
    text = pad(text, BS)
    result = ecb_encode(text, key)
    return (result)

def bs (result):
    length = len(result)
    a = 1
    l = length
    while (l<=length):
        d = "A"*a
        l = len(encryption_oracle(d))
        a = a + 1
    return (l-length)

def create_account():
    result = profile_for("foo@bar.com")
    BS = bs(result)
    b1 = BS - len("email=")
    b2 = BS - len("&uid=10&role=")
    email = "A"*(b1+b2)
    re = profile_for(email)[0:2*BS]
    admin = "A"*b1+pad(bytearray("admin", 'utf-8'), BS).decode('utf-8')
    ra = profile_for(admin)[BS:2*BS]
    tada = re+ra
    return (tada)
    

key = Random.get_random_bytes(16)
print(ecb_decode(create_account(), key))
