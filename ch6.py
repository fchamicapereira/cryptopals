from Tools import Crypto
from Tools import Binary

data = ''

with open('./ch6.txt') as file:
    for line in file:
        data += line.rstrip()

binary = Crypto(data, 64)
keys = binary.decXOR()

binary.xor(Binary(keys[0], 128))
print(binary.data.toAscii())