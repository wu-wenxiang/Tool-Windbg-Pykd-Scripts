import pykd
import re

LOG_FILE = open(r'C:\local\tmp\ttt-common-bp-go-2.txt', 'w')

def pykdLog2File(logObj, fileObj):
    for line in str(logObj).split('\n'):
        fileObj.write(line+'\n')

def pykdLog(log):
    print(log)
    pykdLog2File(log, LOG_FILE)

pykd.dbgCommand(r'bc *')
pykd.dbgCommand(r'bp 08bca3d8')
pykd.dbgCommand(r'bp 2c6d2310')
#pykd.dbgCommand(r'bp 72debcf8')

ret = pykd.dbgCommand(r'bl')
pykdLog(ret)

pykd.dbgCommand(r'bd *')
pykd.dbgCommand(r'g-')
pykd.dbgCommand(r'be *')

while True:
    ret = pykd.dbgCommand(r'g;.time;kL;')
    pykdLog(ret)
    if 'TTT Replay: End of trace reached.' in ret:
        break
    #for line in ret.split('\n'):
    #    if '0038294b' in line:
    #        pykdLog(line)
    #if '0038294b  00000080' in ret:
    #    pykdLog(ret)
    #    ret = pykd.dbgCommand(r'.time')
    #    pykdLog(ret)
    #    break
    LOG_FILE.flush()


pykd.dbgCommand(r'bd *')
pykd.dbgCommand(r'g')
pykd.dbgCommand(r'be *')

while True:
    ret = pykd.dbgCommand(r'g-;.time;kL;')
    pykdLog(ret)
    if 'TTT Replay: Start of trace reached.' in ret:
        break
    LOG_FILE.flush()

LOG_FILE.close()
