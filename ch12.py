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

def __main__():
    print(Crypto.decECB(encryptionOracle))

if __name__ == "__main__":
    __main__()

