'''
Version: 0.0.2
'''

import pykd
import re

LOG_FILE = open(r'C:\local\tmp\debugLog.txt', 'w')

def pyLog2File(logObj, fileObj=LOG_FILE):
    for line in str(logObj).split('\n'):
        fileObj.write(line+'\n')

def pyLog(log):
    print(log)
    pyLog2File(log, LOG_FILE)

def runCmd(cmd, cmdVerbose=True, retVerbose=True):
    cmdLog = pyLog if cmdVerbose else pyLog2File
    retLog = pyLog if retVerbose else pyLog2File
    cmdLog('\n> %s\n%s' % (cmd, '-'*20))
    ret = pykd.dbgCommand(cmd)
    retLog(ret)
    return ret

def runCmdGetArgs(cmdStr, reObj):
    ret = runCmd(cmdStr, False, False)
    return [reObj.search(line)for line in ret.split('\n') if reObj.search(line)]

def ttt_test2end(content):
    if 'TTT Replay: End of trace reached.' in content \
       or 'TTT Replay: Start of trace reached.' in content:
        return True
    return False

def ttt_test2Time(targetTime):
    ret = pykd.dbgCommand(r'.time')
    for line in ret.split('\n'):
        if 'Time Travel Position:' in line:
            currentTime = line.split()[-1].strip('.')
            break
    if int(targetTime, 16) < int(currentTime, 16):
        return True
    return False

