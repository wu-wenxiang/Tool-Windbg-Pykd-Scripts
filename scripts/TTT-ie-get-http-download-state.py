import pykd
import re

LOG_FILE = open(r'C:\local\tmp\ttt-ie-http-request.txt', 'w')

def pykdLog2File(logObj, fileObj):
    for line in str(logObj).split('\n'):
        fileObj.write(line+'\n')

def pykdLog(log):
    print(log)
    pykdLog2File(log, LOG_FILE)

pykd.dbgCommand(r'bc *;g-;bp ieframe!CDownloadWindowItem::_SetState;bp ieframe!CNotificationBar2::SetFormattedText')
ret = pykd.dbgCommand(r'bl')
pykdLog(ret)

while True:
    ret = pykd.dbgCommand(r'g')
    if 'TTT Replay: End of trace reached.' in ret:
        pykdLog(ret)
        break
    ret = pykd.dbgCommand(r'kP')
    pykdLog2File(ret, LOG_FILE)
    for line in ret.split('\n'):
        if 'eState = DLState' in line \
            or 'wchar_t * pwzOriginDownloadUrl = ' in line \
            or 'wchar_t * pwzDestinationFilePath = ' in line \
            or 'wchar_t * psz' in line:
            print(line)
    LOG_FILE.flush()

LOG_FILE.close()
