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


def main():
    cipher_text = open('8.txt').read().splitlines()
    maybe = []
    for hex_string in cipher_text:
        b = bytes.fromhex(hex_string)
        if dup(chunky(b)): maybe.append(hex_string)
    print(maybe)

if __name__ == '__main__':
    main()

