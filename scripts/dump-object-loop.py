import sys
import pykd
import re
from common.v_0_1_1.common_utils import *

postfix = ""
if len(sys.argv) > 1:
    postfix = "-%s" % sys.argv[1]
pyLog = PyLog(r'C:\local\tmp\dump-object-loop%s.txt' % postfix)
util = Util(pyLog)
pyLog.log2Scr('='*10 + ' Start ' + '='*10)

aStr = r'!mex.do2 67640cc158 -c 1 -offset %s -comment 67640cc0b0(Ebf.Core.BusinessComposer.DataModel.IndexedCollection).children.m_dict'
for i in range(0,378320,10000):
    cmdStr = aStr % i
    pyLog.log2Scr(cmdStr)
    util.runCmd(cmdStr)
    pyLog.flush()

pyLog.close()
