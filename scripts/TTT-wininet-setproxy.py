'''
Utils: 0.0.1
'''

import pykd
import re
from common_utils import *

runCmd(r'bc *;g-', False, False)

#runCmd(r'!idna.tt 4AF680000013') # Abnormal: before wininet!WriteProxySettings

#runCmd(r'bp wininet!WriteLegacyProxyInfo', False, False)
#runCmd(r'bp wininet!ReadLegacyProxyInfo', False, False)
#runCmd(r'bp wininet!ChangeGlobalSettings', False, False)
runCmd(r'bp wininet!WriteProxySettings', False, False)
'''
x kernel32!*Reg*ValueExW
'''
#runCmd(r'bp 7642d507;bp 7648900d', False, False)
#runCmd(r'bp 7642990c;bp 76489000', False, False)
#runCmd(r'bp wininet!ReadProxySettings', False, False)
runCmd(r'bl', False)

while True:
    ret = runCmd(r'g', False, False)
    if ttt_test2end(ret):
        pyLog('='*10 + ' End ' + '='*10)
        break
    runCmd(r'.time', False, False)
    runCmd(r'kL3', False)
    #if ttt_test2Time('54C4AC0000046'): # Abnormal: Out of wininet!CommitUrlCacheEntryW
    #if ttt_test2Time('CC79C000003A'): # Normal: Out of wininet!CommitUrlCacheEntryW
    #    break
    ret = runCmd(r'kP1', False, False)
    for line in ret.split('\n'):
        if ' tagProxySettings * ' in line:
            aList = line.split()
            cmd = 'dt %s %s' % (aList[1], aList[5].strip('),'))
            runCmd(cmd)
    #if 'ieframe!CDownloadSecurity::_SendSecurityErrorMessage' in ret:
    #    break
    LOG_FILE.flush()

LOG_FILE.close()
