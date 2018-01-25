from Tools import Binary, Crypto
import random

def encryptionOracle(data):
    print('Plaintext: {}'.format(data.toHex()))
    randomKey = Binary.random(8*16)

    print('Key:       {}'.format(randomKey.toHex()))
    
    addBefore = Binary.random(random.randrange(5,11)*8)
    addAfter = Binary.random(random.randrange(5,11)*8)

    print('Before:    {}\nAfter:     {}'.format(addBefore.toHex(), addAfter.toHex()))

    data = addBefore + data + addAfter

    print('Plaintext: {}'.format(data.toHex()))

    IV = Binary.random(8*16)

    c = Crypto(data)

    if random.randrange(2):
        c.encAES_ECB(randomKey)
        mode = 'ECB'
    else:
        print('IV:        {}'.format(IV.toHex()))
        c.encAES_CBC(randomKey, IV)
        mode = 'CBC'

    return (mode, c.data)

def detectECB(cipher):
    blocks = [Binary(cipher[x:x+8*16]) for x in range(0, len(cipher), 8*16)]
    repeated = 0

    i = 0
    while i < len(blocks) - 1:
        ii = i + 1
        while ii < len(blocks):
            if blocks[i] == blocks[ii]:
                blocks = blocks[:ii] + blocks[ii+1:len(blocks)]
                repeated += 1
                ii -= 1
            ii += 1
        i += 1

    if not repeated:
        return False
    return True

data = Binary('A'*16*10, 128)

cipher = encryptionOracle(data)
print('Mode:      {}\nCipher:    {}'.format(cipher[0], cipher[1].toHex()))
if detectECB(cipher[1]):
    print('====ECB detected====')
else:
    print('====CBC detected=====')