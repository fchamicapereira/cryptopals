from Tools import Crypto

with open('./ch4.txt') as file:
    bestResult = (0, '', '')
    i = 1
    
    for line in file:
        d = Crypto(line.rstrip(), 16)
        result = d.decSingleCharXOR()
        
        if result[0] > bestResult[0]:
            bestResult = result
        i+=1

print(bestResult[2])