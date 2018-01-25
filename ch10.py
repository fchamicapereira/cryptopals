from Tools import Binary, Crypto

data = ''
key = Binary('YELLOW SUBMARINE', 128)

with open('./ch10.txt') as file:
    for line in file:
        data += line.rstrip()
    
data = Binary(data, 64)

IV = Binary('0'*32, 16)
c = Crypto(data)

c.decAES_CBC(key, IV)

print(c.toAscii())