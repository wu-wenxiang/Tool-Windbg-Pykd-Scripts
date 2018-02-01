import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\TTT-fragment-bp-go%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

util.runCmd(r'bc *;g-')
fragmentDict = {line.split()[0]:line.split() for line in open(r'C:\Users\wenw\Desktop\dump&TTT\fragment-diff-2.txt') if line}
for i in fragmentDict:
    util.runCmd(r'ba w4 %s' % i)
    
ret = util.runCmd(r'bl')
for i in ret.split('\n'):
    pyLog.log(i)
bpList = [i.split() for i in ret.split('\n') if i.strip()]
bpDict = {int(i[0]):i[4] for i in bpList}
for i in sorted(bpDict, key=lambda x:int(x)):
    pyLog.log("%s => %s" %(i, bpDict[i]))

reCmp = re.compile(r'^\s*Breakpoint\s+(\d+)\s+hit\s*$')
while True:
    ret = util.runCmd(r'g;.time;kL;kP;')
    pyLog.log(ret)
    bpNum = -1
    for line in ret.split('\n'):
        reSearch = reCmp.search(line)
        if reSearch:
            bpNum = int(reSearch.groups()[0])
            break
    if bpNum > -1:
        fragmentAddress = bpDict[bpNum]
        if fragmentAddress not in fragmentDict:
            fragmentAddress = fragmentAddress.lstrip('0')
        freeStart = fragmentDict[fragmentAddress][-2]
        freeEnd = fragmentDict[fragmentAddress][-1]
        util.runCmdLog(r'dc %s;dc %s;dc %s' % (freeStart, fragmentAddress, freeEnd))
        
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break    
    pyLog.flush()


pyLog.close()
