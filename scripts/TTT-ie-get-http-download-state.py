import pykd
import re

LOG_FILE = open(r'C:\local\tmp\ttt-ie-http-request-fail.txt', 'w')

def pykdLog2File(logObj, fileObj=LOG_FILE):
    for line in str(logObj).split('\n'):
        fileObj.write(line+'\n')

def pykdLog(log):
    print(log)
    pykdLog2File(log, LOG_FILE)

def test2end(retContent):
    if 'TTT Replay: End of trace reached.' in ret:
        return True
    return False

def test2Time(targetTime):
    ret = pykd.dbgCommand(r'.time')
    for line in ret.split('\n'):
        if 'Time Travel Position:' in line:
            currentTime = line.split()[-1].strip('.')
            break
    if int(targetTime, 16) < int(currentTime, 16):
        return True
    return False

pykd.dbgCommand(r'bc *;g-')
pykd.dbgCommand(r'!idna.tt 4159E80000018') # Abnormal:ieframe!CDownloadWindowItem::_SetState
#pykd.dbgCommand(r'!idna.tt 54BF700000644') # Abnormal:wininet!CommitUrlCacheEntryW
#pykd.dbgCommand(r'!idna.tt CC66400005FC') # Normal: wininet!CommitUrlCacheEntryW
pykd.dbgCommand(r'bp ieframe!CDownloadSecurity::_SendSecurityErrorMessage')
pykd.dbgCommand(r'bp ieframe!CDownloadWindowItem::_SetState')
pykd.dbgCommand(r'bp ieframe!CNotificationBar2::SetFormattedText')
pykd.dbgCommand(r'bp wininet!CommitUrlCacheEntryW')
pykd.dbgCommand(r'bp wininet!CommitUrlCacheEntryW+0x759') # Return Point
pykd.dbgCommand(r'bp wininet!CCacheServerContainer::AddUrl')
pykd.dbgCommand(r'bp wininet!CCacheClientContainer::AddUrl')
#pykd.dbgCommand(r'bp rpcrt4!NdrClientCall3')        # Detail
#pykd.dbgCommand(r'bp rpcrt4!NdrpClientCall3')       # Detail
#pykd.dbgCommand(r'bp rpcrt4!Ndr64pClientUnMarshal') # Detail
#pykd.dbgCommand(r'bp ntdll!memcpy')                 # Detail *2

ret = pykd.dbgCommand(r'bl')
pykdLog(ret)

while True:
    ret = pykd.dbgCommand(r'g')
    if test2end(ret):
        pykdLog('='*10 + ' End ' + '='*10)
        break
    ret = pykd.dbgCommand(r'.time')
    pykdLog2File(ret)
    ret = pykd.dbgCommand(r'kL3')
    pykdLog(ret)
    #if test2Time('54C4AC0000046'): # Abnormal: Out of wininet!CommitUrlCacheEntryW
    #if test2Time('CC79C000003A'): # Normal: Out of wininet!CommitUrlCacheEntryW
    #    break
    ret = pykd.dbgCommand(r'kP')
    pykdLog2File(ret)
    for line in ret.split('\n'):
        if 'eState = DLState' in line \
            or 'wchar_t * pwzOriginDownloadUrl = ' in line \
            or 'wchar_t * pwzDestinationFilePath = ' in line \
            or 'wchar_t * psz' in line:
            print(line)
    #if 'ieframe!CDownloadSecurity::_SendSecurityErrorMessage' in ret:
    #    break
    LOG_FILE.flush()

LOG_FILE.close()
