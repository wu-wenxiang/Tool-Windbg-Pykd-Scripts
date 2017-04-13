'''
Utils: 0.1.0
'''

import pykd
import re
from common_utils import *

dumpName = Util.getDumpName()
logPath = r'C:\local\tmp\memory-dotnet-string-%s.txt' % dumpName
pyLog = PyLog(logPath)
util = Util(pyLog)
#ret = util.runCmd(r'!DumpHeap /d -mt 00007ffe972f0e08')
ret = util.runCmd(r'||')
pyLog.log(ret)

pyLog.close()

