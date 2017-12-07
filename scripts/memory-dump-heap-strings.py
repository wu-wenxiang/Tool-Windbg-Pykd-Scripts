import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\memory-dump-heap-strings.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

ret = util.runCmd(r'!heap')
pyLog.log(ret)
pyLog.flush()


reCmp = re.compile(r'^(\s*\d+:)?\s+([0-9a-fA-F]+)\s+')
addrList = [reCmp.search(line).groups()[1] for line in ret.split('\n') if reCmp.search(line)]
pyLog.log(addrList)
pyLog.flush()

reSegmentAt = re.compile(r'^\s*Segment at')

heapSize = 0
for addr in addrList:
    pyLog.log('='*20 + addr + '='*20)
    pyLog.flush()
    
    ret = util.runCmd(r'!heap {0}'.format(addr))
    segList = [line.split() for line in ret.split('\n') if reSegmentAt.search(line)]
    segList = [(i[2], i[4]) for i in segList]
    pyLog.log(segList)
    tmpHeapSize = sum([int(j, 16)-int(i,16) for i,j in segList])/1024.0/1024.0
    pyLog.log('HeapSize = %.2f M' % tmpHeapSize)
    heapSize += tmpHeapSize
    pyLog.flush()

    for i, j in segList:
        ret = util.runCmd(r'!mex.strings %s %s' % (i, j))
        if not ret:
            continue
        for line in ret.split('\n'):
            pyLog.log2File(line)
    pyLog.flush()

pyLog.log('Heap Size = %.2f M' % heapSize)

pyLog.close()
