import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\memory-dump-fragment%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

fragmentDict = {line.split()[0]:line.split() for line in open(r'C:\Users\wenw\Desktop\dump&TTT\fragment-diff-2.txt') if line}
for i in sorted(fragmentDict, key=lambda x:int(x, 16)):
    util.runCmdLog(r'dc %s;dc %s;dc %s' % (fragmentDict[i][-2], i, fragmentDict[i][1]))

pyLog.close()
