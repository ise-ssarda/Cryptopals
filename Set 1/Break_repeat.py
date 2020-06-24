import binascii
import base64

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

def score (string):
    decoded_text = []
    for c in range(256):
        t = xor_hex_strings(string, c)
        s = approx_score(t)
        info = {
            'text': t,
            'score': s,
            'character': chr(c)
            }
        decoded_text.append(info)
        
    best_score = sorted(decoded_text, key = lambda x: x['score'], reverse=True)[0]
    return (best_score)

def hamming_distance (b, c): 
    count = 0
    for a in range(len(b)):
        if (b[a]!=c[a]):
            count = count + 1
    return(count)

def find_keysize(text):
    norm_dis = []
    for d in range(2, 41):
        dis = []
        chunks = [text[a:a+d] for a in range(0, len(text), d)]
        while (len(chunks)>2):
            first = chunks[0]
            second = chunks[1]
            dis.append(hamming_distance(first, second)/d)
            chunks.remove(chunks[0])
            chunks.remove(chunks[1])
        ks = {'key': d, 'dist': sum(dis)/len(dis)}
        norm_dis.append(ks)
    return(sorted(norm_dis, key = lambda x:x['dist'])[0:4])

def brk(text, ks):
    key = ''
    blks = []
    for a in range(1):
        block = b''
        for b in range (0, len(text), ks[a]['key']):
            block = text[b:b+ks[a]['key']]
            blks.append(block)
        block = b''
        for b in range (ks[a]['key']):
            for c in range (len(blks)):
                block = block + blks[c][b:b+1]
            key = key + score(block)['character']
            block = b''
    return (key)


def main():
    cipher_text = open('6.txt').read()
    text = base64.b64decode(cipher_text)
    ks = find_keysize(text)
    key = brk(text, ks)
    l1 = len(text)
    rkey1 = (key * (l1//len(key)+ 1))[:l1]
    k1 = bytes(rkey1, 'utf-8')
    c1 = b''
    for a1, a2 in zip (text, k1):
        c1 += bytes([a1^a2])
    print(c1)
 
if __name__ == '__main__':
    main()
