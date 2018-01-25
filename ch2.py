from Tools import Binary

b1 = Binary('1c0111001f010100061a024b53535009181c', 16)
b2 = Binary('686974207468652062756c6c277320657965', 16)
expected = Binary('746865206b696420646f6e277420706c6179', 16)

if expected == b1 ^ b2:
    print('Passed!')
else:
    print('Expected:', expected)
    print('Got:', b1^b2)