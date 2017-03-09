import pykd
import re

aFile = open(r'C:\local\heap-strings.txt', 'w')

ret = pykd.dbgCommand('!heap 0000000000bf0000')
reSegmentAt = re.compile(r'^\s*Segment at')
aList = [line for line in ret.split('\n') if reSegmentAt.search(line)]
for line in aList:
    tmpList = line.split()
    cmd = r'!mex.strings %s %s' % (tmpList[2], tmpList[4])
    print(cmd)
    aFile.write(cmd+'\n')
    tmpRet = pykd.dbgCommand(cmd)
    for i in tmpRet.split('\n'):
        aFile.write(i+'\n')
    aFile.flush()

aFile.close()
