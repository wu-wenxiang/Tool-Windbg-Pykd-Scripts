import pykd
import re

LOG_FILE = open(r'C:\local\tmp\ttt-ie-http-request.txt', 'w')

def pykdLog2File(logObj, fileObj):
    for line in str(logObj).split('\n'):
        fileObj.write(line+'\n')

def pykdLog(log):
    print(log)
    pykdLog2File(log, LOG_FILE)

pykd.dbgCommand(r'bc *;g-')
pykd.dbgCommand(r'!idna.tt 54C1D40000025')
pykd.dbgCommand(r'bp ieframe!CDownloadSecurity::_SendSecurityErrorMessage')
pykd.dbgCommand(r'bp wininet!CommitUrlCacheEntryW')
pykd.dbgCommand(r'bp ieframe!CDownloadWindowItem::_SetState')
pykd.dbgCommand(r'bp ieframe!CNotificationBar2::SetFormattedText')
pykd.dbgCommand(r'bp wininet!CCacheServerContainer::AddUrl')
pykd.dbgCommand(r'bp wininet!CCacheClientContainer::AddUrl')
pykd.dbgCommand(r'bp rpcrt4!NdrClientCall3')
pykd.dbgCommand(r'bp rpcrt4!NdrpClientCall3')


ret = pykd.dbgCommand(r'bl')
pykdLog(ret)

while True:
    ret = pykd.dbgCommand(r'g')
    if 'TTT Replay: End of trace reached.' in ret:
        pykdLog(ret)
        break
    ret = pykd.dbgCommand(r'kP')
    pykdLog2File(ret, LOG_FILE)
    if 'ieframe!CDownloadSecurity::_SendSecurityErrorMessage' in ret:
        break
    for line in ret.split('\n'):
        if 'eState = DLState' in line \
            or 'wchar_t * pwzOriginDownloadUrl = ' in line \
            or 'wchar_t * pwzDestinationFilePath = ' in line \
            or 'wchar_t * psz' in line:
            print(line)
    LOG_FILE.flush()

LOG_FILE.close()
