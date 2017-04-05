'''
Utils: 0.0.4
'''

import pykd
import re
from common_utils import *

initLog(r'C:\local\tmp\TTT-taskhost-get-addUrl.txt')

print('='*10 + ' Start ' + '='*10)

runCmd(r'bc *;g;g-')

#runCmd(r'bp rpcrt4!Invoke')
#runCmd(r'bp wininet!s_UrlCacheAddUrl')
runCmd(r'bp wininet!CCacheContainer::AddUrl')
runCmd(r'bp wininet!WxVerifySameDirectory')
#runCmd(r'bp esent!ErrorIOMgrIssueIO')

runCmdLog(r'bl', False)

while True:
    ret = runCmd(r'g')
    if ttt_test2end(ret):
        pyLog('='*10 + ' End ' + '='*10)
        break
    runCmd(r'.time')
    #if test2Time('54C4AC0000046'): # Abnormal: Out of wininet!CommitUrlCacheEntryW
    #if test2Time('CC79C000003A'): # Normal: Out of wininet!CommitUrlCacheEntryW
    #    break
    ret = runCmd(r'kP3')
    pyLog(ret)
    
    LOG_FILE.flush()

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

LOG_FILE.close()
