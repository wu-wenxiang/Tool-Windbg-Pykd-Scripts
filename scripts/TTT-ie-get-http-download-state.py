import pykd
import re
from common.v_0_0_3.common_utils import *

print('='*10 + ' Start ' + '='*10)
runCmd(r'bc *;g')

#runCmd(r'!idna.tt 4159E80000018') # Abnormal:ieframe!CDownloadWindowItem::_SetState
#runCmd(r'!idna.tt 54BF700000644') # Abnormal:wininet!CommitUrlCacheEntryW
#runCmd(r'!idna.tt CC66400005FC') # Normal: wininet!CommitUrlCacheEntryW

runCmd(r'bp ieframe!CDownloadSecurity::_SendSecurityErrorMessage')
runCmd(r'bp ieframe!CDownloadWindowItem::_SetState')
runCmd(r'bp ieframe!CNotificationBar2::SetFormattedText')
runCmd(r'bp wininet!CommitUrlCacheEntryW')
runCmd(r'bp wininet!CCacheServerContainer::AddUrl')
runCmd(r'bp wininet!CCacheClientContainer::AddUrl')

#runCmd(r'bp rpcrt4!LRPC_BASE_CCALL::SendReceive') # Detail * 0.5
#runCmd(r'bp ntdll!ZwAlpcSendWaitReceivePort')     # Detail * 0.5

#runCmd(r'bp rpcrt4!NdrClientCall3')        # Detail
#runCmd(r'bp rpcrt4!NdrpClientCall3')       # Detail
#runCmd(r'bp rpcrt4!Ndr64pClientUnMarshal') # Detail
#runCmd(r'bp ntdll!memcpy')                 # Detail *2

runCmd(r'bd *;g-;be *')

runCmdLog(r'bl', False)

while True:
    ret = runCmd(r'g')
    if ttt_test2end(ret):
        pyLog('='*10 + ' End ' + '='*10)
        break
    runCmd(r'.time')
    runCmdLog(r'kL3', False)
    
    #if test2Time('54C4AC0000046'): # Abnormal: Out of wininet!CommitUrlCacheEntryW
    #if test2Time('CC79C000003A'): # Normal: Out of wininet!CommitUrlCacheEntryW
    #    break
    ret = runCmd(r'kP')

    for line in ret.split('\n'):
        if 'eState = DLState' in line \
            or 'wchar_t * pwzOriginDownloadUrl = ' in line \
            or 'wchar_t * pwzDestinationFilePath = ' in line \
            or 'wchar_t * psz' in line:
            pyLog(line)
    #if 'ieframe!CDownloadSecurity::_SendSecurityErrorMessage' in ret:
    #    break

    ret = runCmd(r'!mex.t')
    for line in ret.split('\n'):
        if 'webcache_' in line:
            pyLog(line)
    
    LOG_FILE.flush()

LOG_FILE.close()
