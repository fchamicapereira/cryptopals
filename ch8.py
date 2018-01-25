from Tools import Binary

with open('./ch8.txt') as file:
    lineCounter = 0
    for line in file:
        lineCounter += 1
        line = line.rstrip()
        data = Binary(line, 16)
        repeatedGroups = 0
        
        step = 8 * 16 # 16 bytes

        for i in range(0, len(data) - step, step):
            group = data[i:i+step]
            for ii in range(i + step, len(data) - step, step):
                anotherGroup = data[ii:ii+step]
                if group == anotherGroup:
                    repeatedGroups += 1

        if repeatedGroups > 0:
            print('Number: {}\nLine: {}\nRepeated:{}'.format(lineCounter, data.toHex(), repeatedGroups))
