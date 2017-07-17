import pykd
import re
from common.v_0_1_1.common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\TTT-httpai-Set.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)
util.runCmd(r'bc *;g')

util.runCmd(r'bp httpapi!HttpSetServerSessionProperty')
util.runCmd(r'bp kernelbase!HttpSetServerSessionProperty')

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
