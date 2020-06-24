block = "YELLOW SUBMARINE"
ps = 20
l = len(block)
p = ps - l%ps
for a in range(p):
    block = block + "\\x{:02x}".format(p) 
print(block)
