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

while True:
    ret = pykd.dbgCommand(r'g;dd 0038294b')
    if '0038294b  00000080' in ret:
        pykdLog(ret)
        ret = pykd.dbgCommand(r'.time')
        pykdLog(ret)
        break
    #LOG_FILE.flush()

LOG_FILE.close()
