import re

reCmp = re.compile(r'^\s*(.+?)\s+(\d+)\s+\d+\s*$')

class HeapObj(dict):
    def __init__(self, filepath):
        kvList = [reCmp.search(line).groups() for line in open(filepath) if reCmp.search(line)]
        for k,v in kvList:
            self[k.strip()] = (int(v.strip()), '')
    def __sub__(self, heap):
        return diffHeap(self, heap)

def diffHeap(aHeap, bHeap):
    retDict = {}
    for k,v in aHeap.items():
        diffNum = v[0]-bHeap.get(k, (0, ''))[0]
        if diffNum > 0:
            retDict[k] = (diffNum, '%s-%s' % (v[0], bHeap.get(k, (0, ''))[0]))
    return retDict

def dumpDiff(diffDict, msg):
    print('-'*10, msg, '-'*10)
    for i in sorted(diffDict, key=lambda x:diffDict[x][0], reverse=True):
        print(i, diffDict[i][0], diffDict[i][1])
    print('\n')

heap1 = HeapObj(r'C:\local\tmp\heap-object-1.txt')
heap2 = HeapObj(r'C:\local\tmp\heap-object-2.txt')

dumpDiff(heap2-heap1, 'diff')
