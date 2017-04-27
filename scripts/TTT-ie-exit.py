'''
Utils: 0.1.1
'''

import pykd
import re
from common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\TTT-ie-exit.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)
util.runCmd(r'bc *;g')

util.runCmd(r'bp msvcrt!exit')

util.runCmdLog(r'bd *;g-;be *;bl', False)

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
