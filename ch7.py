from Tools import Crypto
from Tools import Binary

data = ''
key = Binary('YELLOW SUBMARINE', 128)

with open('./ch7.txt') as file:
    for line in file:
        data += line.rstrip()

binary = Crypto(Binary(data, 64))

binary.decAES_ECB(key)

print(binary.toAscii())