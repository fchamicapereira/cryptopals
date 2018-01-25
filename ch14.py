from ch12 import encryptionOracle
from Tools import Binary
import random

randomPrefix = Binary().random(random.randrange(0, 30*8, 8))

def wrapper(data):
    return encryptionOracle(randomPrefix + data)

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

def decECB(oracle):
    blockSize = getBlockSize(oracle)
    nblocks = int(len(oracle(Binary())) / blockSize)
    in_a_row = 10
    proceed = True

    # find the prefix size
    print('Finding the random prefix size...')
    word = Binary('A' * (in_a_row * int(blockSize / 8) - 1), 128)

    while proceed:
        word += Binary('A', 128)
        cipher = oracle(word)
        blocks = [cipher[i:i + blockSize] for i in range(0, len(cipher), blockSize)]

        for i in range(len(blocks) - 1):
            blockCount = 1

            for ii in range(i + 1, len(blocks)):
                if blocks[i] == blocks[ii]:
                    blockCount += 1
                else:
                    break

            if blockCount == in_a_row:
                proceed = False
                prefixSize = (i + in_a_row) * blockSize - len(word)
                break

    if prefixSize % blockSize != 0:
        remainder = int((blockSize - (prefixSize % blockSize)) / 8)
    else:
        remainder = 0


    prefixPad = Binary('P' * remainder, 128)
    start = prefixSize + len(prefixPad)
    print('Prefix size: {:.0f} bytes\nPad: {}'.format(prefixSize / 8, prefixPad.toAscii()))
    
    plainText = ''

    wordCiphers = []
    for wordSize in range(int(blockSize / 8) - 1, -1, -1):
        word = prefixPad + Binary('A' * wordSize, 128)
        wordCiphers.append((word, wordSize, oracle(word)))

    for block in range(int(start / blockSize), nblocks):
        for cipher in wordCiphers:

            blockPosition = block * blockSize
            blockCipher = cipher[2][blockPosition:blockPosition + blockSize]
            known = cipher[0] + Binary(plainText, 128)

            found = False
            for newChar in range(127, -1, -1):

                cipherWithNewChar = oracle(known + Binary(chr(newChar), 128))

                if blockCipher == cipherWithNewChar[blockPosition:blockPosition + blockSize]:
                    plainText += chr(newChar)
                    print('Block {:>2} Digit {:>2}: {}'.format(block + 1, int(blockSize / 8 - cipher[1]), chr(newChar)))
                    found = True
                    break
            
            if not found and block + 1 < nblocks:
                print('New char not found. Exiting')
                exit()
            elif not found:
                return plainText

print(decECB(wrapper))