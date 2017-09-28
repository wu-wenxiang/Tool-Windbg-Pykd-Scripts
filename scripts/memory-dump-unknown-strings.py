import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\memory-dump-unknown-strings.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

ret = util.runCmd(r'!mex.grep MEM_COMMIT !address /f:Unk')
#pyLog.log(ret)
#pyLog.flush()

reCmp = re.compile(r'^\s+0\D([0-9a-fA-F]+)\s+0\D([0-9a-fA-F]+)\s+0\D([0-9a-fA-F]+)\s+')
addrList = [reCmp.search(line).groups() for line in ret.split('\n') if reCmp.search(line)]
unkSize = sum([int(i[2], 16) for i in addrList])/1024.0/1024.0
pyLog.log('Unknown Size = %.2f M' % unkSize)
pyLog.flush()

for addrStart, addrEnd, _len in addrList:
    ret = util.runCmd(r'!mex.strings %s %s' % (addrStart, addrEnd))
    if not ret:
        continue
    for line in ret.split('\n'):
        pyLog.log2File(line)
    pyLog.flush()

pyLog.close()
