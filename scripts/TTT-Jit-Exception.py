import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\TTT-Jit-Exception.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)
#util.runCmd(r'bc *;g')
#util.runCmd(r'bp 2e04da88')
#util.runCmd(r'bp 354ef4d8')

util.runCmdLog(r'bl', False)
util.runCmd(r'bd *;g-;be *')

util.runCmd(r'!idna.tt 3D0500000115')
while True:
    ret = util.runCmd(r'p-;!mex.grep _message !mex.DisplayObj 0x1bc3f08c')
    util.runCmd(r'.time')
    if 'Bad binary signature' not in ret:
        break
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break
    
    #ret = util.runCmd(r'kP3')
    pyLog.log(ret)
    
    pyLog.flush()


pyLog.close()
