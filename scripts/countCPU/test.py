aList = [i.split(':')[-1] for i in open(r'test1.txt') if 'days' in i]
aList = [[int(j) for j in i.split('.')] for i in aList]
aList = [i*1000+j for i,j in aList]
print(len(aList), sum(aList))
bList = [i.split(':')[-1] for i in open(r'test2.txt') if 'days' in i]
bList = [[int(j) for j in i.split('.')] for i in bList]
bList = [i*1000+j for i,j in bList]
print(len(bList), sum(bList))

print((sum(bList) - sum(aList))/1000.0)
print((3*60+32)*4)
print(((sum(bList) - sum(aList))/1000.0) / ((3*60+32)*4))



cList = [i.split()[0].split(':')[1] for i in open(r'test1.txt') if 'days' in i]
aList = zip(cList, aList)
aDict = {}
for i,j in set(aList):
    aDict.setdefault(i, 0)
    aDict[i] = aDict[i] + j
#print(len(aDict), aDict)

cList = [i.split()[0].split(':')[1] for i in open(r'test2.txt') if 'days' in i]
bList = zip(cList, bList)
bDict = {}
for i,j in set(bList):
    bDict.setdefault(i, 0)
    bDict[i] = bDict[i] + j
#print(len(bDict), bDict)


cDict = {}
for k,v in bDict.items():
    aDict.setdefault(k, 0)
    cDict[k] = (v-aDict[k])/1000.0
for i in sorted(cDict, key=lambda x:cDict[x], reverse=True):
    print(i, cDict[i])

print(sum(cDict.values()))

