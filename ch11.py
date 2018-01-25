from Tools import Binary, Crypto
import random

def encryptionOracle(data):
    randomKey = Binary.random(8*16)
    addBefore = Binary.random(random.randrange(5,11)*8)
    addAfter = Binary.random(random.randrange(5,11)*8)
    data = addBefore + data + addAfter
    IV = Binary.random(8*16)

    c = Crypto(data)

    if random.randrange(2):
        c.encAES_ECB(randomKey)
        mode = 'ECB'
    else:
        c.encAES_CBC(randomKey, IV)
        mode = 'CBC'

    return (mode, c.data)

def detectMode(cipher):
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
        return 'CBC'
    return 'ECB'

data = Binary('A'*16*10, 128)
nTests = 25
count = 0

for i in range(nTests):
    cipher = encryptionOracle(data)
    passed = False
    detectedMode = detectMode(cipher[1])

    if detectedMode == cipher[0]:
        passed = True
        count += 1

    print('({:>2}/{}) Used: {} Detected: {} --> Passed: {}'.format(i+1, nTests, cipher[0], detectedMode, passed))

print('Passed {:.0f}% of tests'.format(100*float(count) / nTests))