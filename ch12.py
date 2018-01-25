from Tools import Binary, Crypto
import random

# constant random key
randomKey = Binary.random(8*16)

def encryptionOracle(data):
    extraData = Binary('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK', 64)
    data = data + extraData

    c = Crypto(data)

    c.encAES_ECB(randomKey)
    return c.data

def getBlockSize(oracle):
    startCounting = -1
    extraBytes = 1
    baseLength = len(oracle(Binary()))

    while 1:
        newLength = len(oracle(Binary('A'*extraBytes, 128)))

        if newLength > baseLength and startCounting == -1:
            startCounting = extraBytes
        
        elif newLength > baseLength:
            return newLength - baseLength

        extraBytes += 1

def detectMode(oracle):
    cipher = oracle(Binary('A'*16*10, 128))
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

def decECB(oracle):
    blockSize = getBlockSize(oracle)
    nblocks = int(len(oracle(Binary())) / blockSize)
    
    if detectMode(oracle) != 'ECB':
        print('Not ECB. Exiting')
        return

    plainText = ''

    wordCiphers = []
    for wordSize in range(int(blockSize / 8) - 1, -1, -1):
        word = Binary('A' * wordSize, 128)
        wordCiphers.append((word, wordSize, oracle(word)))

    for block in range(nblocks):
        for cipher in wordCiphers:
            blockCipher = cipher[2][block * blockSize:block * blockSize + blockSize]
            known = cipher[0] + Binary(plainText, 128)

            found = False
            for newChar in range(127, -1, -1):
                cipherWithNewChar = oracle(known + Binary(chr(newChar), 128))
                if blockCipher == cipherWithNewChar[block * blockSize:block * blockSize + blockSize]:
                    plainText += chr(newChar)
                    print('Block {:>2} Digit {:>2}: {}'.format(block+1, int(blockSize / 8 - cipher[1]), chr(newChar)))
                    found = True
                    break
            
            if not found and block + 1 < nblocks:
                print('New char not found. Exiting')
                exit()
            elif not found:
                return plainText

def __main__():
    print(decECB(encryptionOracle))

if __name__ == "__main__":
    __main__()

