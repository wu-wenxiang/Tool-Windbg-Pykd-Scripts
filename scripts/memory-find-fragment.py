import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\memory-find-fragment%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

ret = util.runCmd(r'!address')
#pyLog.log(ret)
#pyLog.flush()

aList = []
reCmp = re.compile(r'^\+?\s+([0-9A-Fa-f]+)\s+([0-9A-Fa-f]+)\s+([0-9A-Fa-f]+)\s+(MEM_[A-Z]+\s+)?(MEM_[A-Z]+\s+)?(PAGE_[A-Z]+\s+)?(\S+)\s*(.+)\s*$')
for line in ret.split('\n'):
    reSearch = reCmp.search(line)
    if reSearch:
        #pyLog.log(line)
        tmpList = [i.strip() for i in reSearch.groups() if i]
        aList.append(tmpList)
        pyLog.log(tmpList)
pyLog.flush()

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

pyLog.close()
