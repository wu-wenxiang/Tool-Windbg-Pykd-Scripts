import pykd
import re

aFile = open(r'C:\local\modules-info.txt', 'w')

ret = pykd.dbgCommand('lm')
reAddress = re.compile(r'^\d+')
aList = [line for line in ret.split('\n') if reAddress.search(line)]
for line in aList:
    tmpList = line.split()
    cmd = r'lmvm %s' % (tmpList[2])
    print(cmd)
    aFile.write(cmd+'\n')
    tmpRet = pykd.dbgCommand(cmd)
    for i in tmpRet.split('\n'):
        #if 'CompanyName:' in i or 'Timestamp:' in i:
        #    print(i)
        aFile.write(i+'\n')
    aFile.flush()

aFile.close()
