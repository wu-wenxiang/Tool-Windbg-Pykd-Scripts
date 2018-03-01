import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\TTT-fragment-bp-go-2%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

util.runCmd(r'bc *;g-')
#for i in fragmentDict:
#    util.runCmd(r'ba w4 %s' % i)
#dc 3f605000;dc 3f610000;dc 3f615000

util.runCmdLog(r'dc 417a5000;dc 417b0000;dc 417b1000')

util.runCmd(r'ba w4 417a5000')
util.runCmd(r'ba w4 417b0000')
util.runCmd(r'ba w4 417b1000')
    
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
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break    
    #pyLog.log(ret)
    
    bpNum = -1
    for line in ret.split('\n'):
        reSearch = reCmp.search(line)
        if reSearch:
            bpNum = int(reSearch.groups()[0])
            break
    util.runCmdLog(r'dc 417a5000;dc 417b0000;dc 417b1000')
    util.runCmdLog(r'p;kL;kP')
    util.runCmdLog(r'dc 417a5000;dc 417b0000;dc 417b1000')
        
    pyLog.flush()


pyLog.close()
