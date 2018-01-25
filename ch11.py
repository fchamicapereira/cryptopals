from Tools import Binary, Crypto

def encryptionOracle(data):
    randomKey = Binary.random(8*16)

    c = Crypto(data)
    c.encAES_ECB(randomKey)

    print(c.toHex())

data = Binary('This is an example', 128)

print(data.toAscii())
print(data.toHex())
encryptionOracle(data)