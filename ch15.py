from Tools import Crypto, Binary

b = Binary('ICE ICE BABY', 128)

print(Binary(Crypto.removePadding(b + Binary('04040404', 16))).toAscii())

try:
    Crypto.removePadding(b + Binary('05050505', 16))
except:
    print('Caught exception')

try:
    Crypto.removePadding(b + Binary('01020304', 16))
except:
    print('Caught exception')

print('Passed!')