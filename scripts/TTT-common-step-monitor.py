import pykd
import re

LOG_FILE = open(r'C:\local\tmp\ttt-common-step-monitor.txt', 'w')

def pykdLog2File(logObj, fileObj):
    for line in str(logObj).split('\n'):
        fileObj.write(line+'\n')

def pykdLog(log):
    print(log)
    pykdLog2File(log, LOG_FILE)

pykd.dbgCommand(r'bd *')
# 54C1D40000025
# 54C49C0000051 - Issue
pykd.dbgCommand(r'!idna.tt 54C2FC0000033')
pykd.dbgCommand(r'be *')

while True:
    ret = pykd.dbgCommand(r'g;dd 0038294b')
    if 'TTT Replay: End of trace reached.' in ret:
        pykdLog(ret)
        break
    for line in ret.split('\n'):
        if '0038294b' in line:
            pykdLog(line)
    if '0038294b  00000080' in ret:
        pykdLog(ret)
        ret = pykd.dbgCommand(r'.time')
        pykdLog(ret)
        break
    #LOG_FILE.flush()

LOG_FILE.close()
