import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\memory-dump-heap-strings.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

ret = util.runCmd(r'!heap')
pyLog.log(ret)
pyLog.flush()


reCmp = re.compile(r'^\s+([0-9a-fA-F]+)\s+NT\s+Heap\s*$')
addrList = [reCmp.search(line).groups()[0] for line in ret.split('\n') if reCmp.search(line)]
pyLog.log(addrList)
pyLog.flush()

reSegmentAt = re.compile(r'^\s*Segment at')

for addr in addrList:
    pyLog.log('='*20 + addr + '='*20)
    pyLog.flush()
    
    ret = util.runCmd(r'!heap {0}'.format(addr))
    segList = [line.split() for line in ret.split('\n') if reSegmentAt.search(line)]
    segList = [(i[2], i[4]) for i in segList]
    pyLog.log(segList)
    pyLog.flush()

    for i, j in segList:
        ret = util.runCmd(r'!mex.strings %s %s' % (i, j))
        if not ret:
            continue
        for line in ret.split('\n'):
            pyLog.log2File(line)
    pyLog.flush()

pyLog.close()
