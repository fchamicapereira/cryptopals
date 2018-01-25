from Tools import Binary

b = Binary('YELLOW SUBMARINE', 128)
padded = b.pkcs_7(21*8)

print('Before padding: {}'.format(b.toHex()))
print('After padding:  {}'.format(padded.toHex()))