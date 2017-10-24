import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\memory-stack.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

ret = util.runCmd(r'~')
pyLog.log(ret)
pyLog.flush()


reCmp = re.compile(r'^\s*\S?\s+(\d+)\s+')
addrList = [int(reCmp.search(line).groups()[0]) for line in ret.split('\n') if reCmp.search(line)]
pyLog.log(addrList)
pyLog.flush()

sizeList = []
reCmp = re.compile(r'^\s*(\S+):\s+(\S+)\b')
for i in addrList:
    pyLog.log('===> %s' % i)
    ret = util.runCmd(r'~%ss;!teb' % (i,))
    aDict = {}
    for line in ret.split('\n'):
        reSearch = reCmp.search(line)
        if reSearch:
            k, v = reSearch.groups()
            aDict[k] = int(v, 16)
    pyLog.log(aDict)
    stackSize = aDict['StackBase']-aDict['StackLimit']
    sizeList.append(stackSize)
    pyLog.flush()

pyLog.log(sizeList)
pyLog.log(sum(sizeList))
pyLog.log('StackSize = %f M' % (sum(sizeList)/1024.0/1024))
pyLog.close()
