from Cryptodome.Cipher import AES
import base64
cipher_text = open('7.txt').read()
text = base64.b64decode(cipher_text)
key = b'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB)
de = cipher.decrypt(text)
print(de)
