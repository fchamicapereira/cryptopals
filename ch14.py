from ch12 import encryptionOracle
from Tools import Binary, Crypto
import random

randomPrefix = Binary().random(random.randrange(0, 30*8, 8))

def wrapper(data):
    return encryptionOracle(randomPrefix + data)

print(Crypto.decECB(wrapper))