from Tools import Binary, Crypto

randomKey = Binary().random(8*16)

def parseParams(params):
    result = {}
    pairs = params.split('&')

    for pair in pairs:
        content = pair.split('=')
        result[content[0]] = content[1]
    
    return result

def profile_for(email):
    email = email.replace('&','')
    email = email.replace('=','')
    return 'email={}&uid={}&role=user'.format(email, 10)

def createProfileAndProvide(email):
    if isinstance(email, Binary):
        email = email.toAscii()

    profile = profile_for(email)
    c =  Crypto(Binary(profile, 128))
    c.encAES_ECB(randomKey)

    cipher = c.data
    return cipher

def decryptProfile(profile):
    c = Crypto(profile.toHex(), 16)
    c.decAES_ECB(randomKey)
    parsedProfile = parseParams(c.toAscii())
    print(parsedProfile)

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

blockSize = getBlockSize(createProfileAndProvide)

email = 'foo@bar'

word = Binary('-' * (int(blockSize/8) - len('email=')) + 'admin', 128).pkcs_7(2*blockSize - len('email=') * 8)
admin = createProfileAndProvide(word.toAscii())[blockSize:2*blockSize]

counter = 0
baseLen = len(createProfileAndProvide(email))

for extraBytes in range(1, int(blockSize / 8)):
    if len(createProfileAndProvide(email + ' ' * extraBytes)) > baseLen:
        pad = extraBytes + 3
        break

userCipher = createProfileAndProvide(email + pad * ' ')
adminCipher = Binary(userCipher[:-blockSize] + admin)

decryptProfile(adminCipher)
    
