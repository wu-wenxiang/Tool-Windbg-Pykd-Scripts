import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\TTT-monitor-register.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

#util.runCmd(r'bc *;g')
#util.runCmdLog(r'bl', False)
#util.runCmd(r'bd *;g-;be *')
util.runCmd(r'bc *;g-')

util.runCmd(r'!idna.tt 1B3E00000551')
ret = util.runCmd(r'rF')
pyLog.log(ret)

while True:
    ret = util.runCmd(r'p;rF')
    pyLog.log(ret)
    if 'fpcw=1372' in ret:
        break
    util.runCmd(r'.time')
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break    
    pyLog.flush()


pyLog.close()
