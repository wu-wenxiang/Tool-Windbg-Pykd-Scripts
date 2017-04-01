'''
Utils: 0.0.3
'''

import pykd
import re
from common_utils import *

print('='*10 + ' Start ' + '='*10)
runCmd(r'bc *;g-')

#runCmd(r'!idna.tt 4AF680000013') # Abnormal: before wininet!WriteProxySettings

runCmd(r'bp msi!PostAssemblyError')
runCmd(r'bp clr!StrongNameSignatureVerification')
runCmd(r'bp clr!UnloadAssembly')
runCmd(r'bp msi!CMsiExecute::Rollback')
runCmd(r'bp clr!CAssemblyCacheItem::LegacyCommit')
#runCmd(r'bp clr!StrongNameIsValidPublicKey')
runCmd(r'bp 000007fe`ec9b2068')
runCmd(r'bp 000007fe`ec722b50')
'''
x kernel32!*Reg*ValueExW
'''
#runCmd(r'bp 7642d507;bp 7648900d')
#runCmd(r'bp 7642990c;bp 76489000')
#runCmd(r'bp wininet!ReadProxySettings')
runCmdLog(r'bl', False)

while True:
    ret = runCmd(r'g')
    if ttt_test2end(ret):
        pyLog('='*10 + ' End ' + '='*10)
        break
    runCmd(r'.time')
    runCmdLog(r'kL3', False)
    #if ttt_test2Time('54C4AC0000046'): # Abnormal: Out of wininet!CommitUrlCacheEntryW
    #if ttt_test2Time('CC79C000003A'): # Normal: Out of wininet!CommitUrlCacheEntryW
    #    break
    ret = runCmd(r'kP3')
    '''
    for line in ret.split('\n'):
        if ' tagProxySettings * ' in line:
            aList = line.split()
            cmd = 'dt %s %s' % (aList[1], aList[5].strip('),'))
            runCmd(cmd)
    '''
    #if 'ieframe!CDownloadSecurity::_SendSecurityErrorMessage' in ret:
    #    break
    LOG_FILE.flush()

LOG_FILE.close()
