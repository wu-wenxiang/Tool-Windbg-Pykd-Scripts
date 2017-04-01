'''
Utils: 0.0.3
'''

import pykd
import re
from common_utils import runCmd, pyLog, LOG_FILE, runCmdGetArgs

reAspxpages = re.compile(r'^(SL)?\s+([0-9a-fA-F]+)\s+')
reHttpRequest = re.compile(r'\s_request\s+:\s+([0-9a-fA-F]+)\s+')
reWorkerRequest = re.compile(r'\s_wr\s+:\s+([0-9a-fA-F]+)\s+')
reUnknownRequestHeaders = re.compile(r'\s_unknownRequestHeaders\s+:\s+([0-9a-fA-F]+)\s+')
reHeader = re.compile(r'^\[[0-9a-fA-F]+\]\s+([0-9a-fA-F]+)\s+')
reIpAddr = re.compile(r'\[1\]\s+[0-9a-fA-F]+\s+"([^"]+)"')

ret = runCmdGetArgs(r'!mex.grep pdnqnykrvmsdcqmdzhzsxhz3 !mex.aspxpagesext -n -ip -s', reAspxpages)
for item in ret:
    httpContextID = item.groups()[1]
    # pyLog(httpContextID)
    ret = runCmdGetArgs(r'!mex.DisplayObj %s' % httpContextID, reHttpRequest)
    if not ret:
        continue
    httpRequestID = ret[0].groups()[0]
    # pyLog(httpRequestID)
    ret = runCmdGetArgs(r'!mex.DisplayObj %s' % httpRequestID, reWorkerRequest)
    if not ret:
        continue
    workerRequestID = ret[0].groups()[0]
    #pyLog(workerRequestID)
    ret = runCmdGetArgs(r'!mex.DisplayObj %s' % workerRequestID, reUnknownRequestHeaders)
    if not ret:
        continue
    unknownRequestID = ret[0].groups()[0]
    #pyLog(unknownRequestID)
    ret = runCmdGetArgs(r'!mex.DisplayObj %s' % unknownRequestID, reHeader)
    if not ret:
        continue
    for header in ret:
        headerID = header.groups()[0]
        tmpRet = runCmd(r'!mex.DisplayObj %s' % headerID)
        if "NS-Client-IP" in tmpRet:
            for line in tmpRet.split('\n'):
                if reIpAddr.search(line):
                    pyLog(reIpAddr.search(line).groups()[0])
            break

    LOG_FILE.flush()

LOG_FILE.close()

    
    
        
        
        

