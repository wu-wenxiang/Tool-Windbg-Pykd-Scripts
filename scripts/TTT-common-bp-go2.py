import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\TTT-common-bp-go-2%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

util.runCmd(r'bc *;g')
#util.runCmd(r'bp wininet!CWxSocket::Connect')
#util.runCmd(r'bp mswsock!MSAFD_ConnectEx')
#util.runCmd(r'bp mswsock!SockDoConnectEx')
#util.runCmd(r'bp wininet!CFsm_HttpSendRequest::RunSM')
#util.runCmd(r'bp wininet!CFsm::Run')
#util.runCmd(r'bp wininet!HTTP_REQUEST_HANDLE_OBJECT::HttpSendRequest_Start')
util.runCmd(r'bp wininet!CFsm_HttpSendRequest::RunSM')
    
ret = util.runCmd(r'bl')
for i in ret.split('\n'):
    pyLog.log(i)

while True:
    ret = util.runCmd(r'g-;.time;kL;kP;')
    if Util.ttt_test2end(ret):
        pyLog.log2Scr('='*10 + ' End ' + '='*10)
        break    
    pyLog.log(ret)
    
    pyLog.flush()


pyLog.close()
