block = b'YELLOW SUBMARINE'
BS = 20
l = len(block)
ps = BS - l%BS
if ps==0: ps = BS
p = (chr(ps)*ps).encode()
print(block+p)
