'''
Utils: 0.1.1
'''

import pykd
import re
from common_utils import *
    
pyLog = PyLog(r'C:\local\tmp\TTT-taskhost-get-addUrl.txt')
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)
util.runCmd(r'bc *;g;g-')

#util.runCmd(r'bp rpcrt4!Invoke')
#util.runCmd(r'bp wininet!s_UrlCacheAddUrl')
util.runCmd(r'bp wininet!CCacheContainer::AddUrl')
util.runCmd(r'bp wininet!WxVerifySameDirectory')
#util.runCmd(r'bp esent!ErrorIOMgrIssueIO')

util.runCmdLog(r'bl', False)

while True:
    ret = util.runCmd(r'g')
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break
    util.runCmd(r'.time')
    
    ret = util.runCmd(r'kP3')
    pyLog.log(ret)
    
    pyLog.flush()

'''
#bpList = [r'bp rpcrt4!Invoke', 'bp wininet!s_UrlCacheAddUrl', r'bp wininet!CCacheContainer::AddUrl', r'bp esent!ErrorIOMgrIssueIO']
bpList = [r'bp wininet!CCacheContainer::AddUrl']
for bpStr in bpList:
    runCmd(r'bc *;g;g-')
    runCmd(bpStr)
    runCmdLog(r'bl', False)
    while True:
        ret = runCmd(r'g')
        if ttt_test2end(ret):
            pyLog('='*10 + ' End ' + '='*10)
            break
        runCmd(r'.time')
        runCmdLog(r'kL3', False)
        
        runCmd(r'bd *;pt')
        ret = runCmd(r'r')
        pyLog(ret)
        
        LOG_FILE.flush()

        runCmd(r'be *')

  2 Time Travel Position: 258A40000268
 41 Time Travel Position: 258A4000029D 
 80 Time Travel Position: 258A40000740
 86 Time Travel Position: 25954000008F
 47 Time Travel Position: 25954000009D
  8 Time Travel Position: 2595400000A3
  
 22 Time Travel Position: 73B880000268
 60 Time Travel Position: 73B88000029D
 99 Time Travel Position: 73B88000054E
105 Time Travel Position: 73F34000008F
 66 Time Travel Position: 73F34000009D 
 28 Time Travel Position: 73F3400000A3

'''

pyLog.close()
