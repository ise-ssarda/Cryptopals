def xor_hex_strings (b, c): 
    d = b''
    for a in b:
        d += bytes([a^c])
    return(d)

def approx_score (text):
    char_freq = {
        'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442,
        'f': 0.0197881, 'g': 0.0158610, 'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033,
        'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302,
        'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357,
        'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984,
        'z': 0.0007836, ' ': 0.1918182
        }
    return sum([char_freq.get(chr(byte), 0) for byte in text.lower()])

def brute_force(b):
    decoded_text = []
    for c in range(256):
        t = xor_hex_strings(b, c)
        s = approx_score(t)
        info = {
            'text': t,
            'score': s,
            'character': chr(c)
            }
        decoded_text.append(info)
    return sorted(decoded_text, key = lambda x: x['score'], reverse=True)[0]

def main():
    cipher_text = open('4.txt').read().splitlines()
    maybe = []
    for hex_string in cipher_text:
        b = bytes.fromhex(hex_string)
        maybe.append(brute_force(b))
    best_score = sorted(maybe, key = lambda x: x['score'], reverse=True)[0]
    for info in best_score:
        print("{}: {}".format(info.title(), best_score[info]))

if __name__ == '__main__':
    main()
