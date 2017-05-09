import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\TTT-regsvr32-crash.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)
util.runCmd(r'bc *;g')

util.runCmd(r'bp regsvr32!wWinMain')
util.runCmd(r'bp coquerymgr_dll!InternalDllMain')
util.runCmd(r'bp mfc100d!AfxWinInit')
util.runCmd(r'bp mfc100d!AfxGetResourceHandle')
util.runCmd(r'bp mfc100d!AfxAssertFailedLine')
util.runCmd(r'bp mfc71d!AfxWinInit')
util.runCmd(r'bp mfc71d!AfxGetResourceHandle')
util.runCmd(r'bp mfc71d!AfxAssertFailedLine')

util.runCmdLog(r'bl', False)
util.runCmd(r'bd *;g-;be *')

while True:
    ret = util.runCmd(r'g')
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break
    util.runCmd(r'.time')
    
    ret = util.runCmd(r'kP3')
    pyLog.log(ret)
    
    pyLog.flush()


pyLog.close()
