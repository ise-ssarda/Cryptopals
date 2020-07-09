string = b'F14ADBDA019D6DB7EFD91546E3FF84449BCB\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E'
ps = string[-1]
for a in range(ps):
    if(string[-(a+1)]!=ps):
        raise Exception("Boo")
print(string[:-ps].decode('utf-8'))
