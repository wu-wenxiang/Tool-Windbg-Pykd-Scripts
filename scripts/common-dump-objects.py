import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\common-dump-objects%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

ret = util.runCmd(r'!sos.DumpHeap /d -mt 00007ffd61879bc0')
pyLog.log(ret)
pyLog.flush()


aList = []
reCmp = re.compile(r'^([0-9a-fA-F]{16})\s+[0-9a-fA-F]{16}\s+[0-9a-fA-F]+\s*$')
for line in ret.split('\n'):
    reSearch = reCmp.search(line)
    if reSearch:
        #pyLog.log(line)
        tmpList = [i.strip() for i in reSearch.groups() if i]
        aList.append(tmpList)
        pyLog.log(tmpList)
pyLog.flush()

for i in aList:
    util.runCmd(r'!mex.do2 %s' % i[0])
'''
# Check integrated
startList = [i[0] for i in aList][1:]
endList = [i[1] for i in aList][:-1]
if startList != endList:
    pyLog.log(startList)
    pyLog.log(endList)
    pyLog.log('Address dump not integrated!')
    exit()

bList = []
for i,j in enumerate(aList):
    if (j[-2].lower() != 'free') and (int(j[2], 16) <= 0xffff) \
       and ((i==0) or (aList[i-1][-2].lower() == 'free')) \
       and ((i==len(aList)-1) or (aList[i+1][-2].lower() == 'free')):
        freeStart = ''
        if i>0:
            freeStart = aList[i-1][0]
        freeEnd = ''
        if i<(len(aList)-1):
            freeEnd = aList[i+1][1]
        bList.append(j+[freeStart, freeEnd])

pyLog.log('\n'+'='*10+'\n')
for i in bList:
    pyLog.log(i)
pyLog.log('\n'+'='*10+'\n')
pyLog.log('length = %s' % len(bList))

'''

pyLog.close()
