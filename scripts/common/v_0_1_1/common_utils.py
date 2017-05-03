'''
Version: 0.1.1
'''

import pykd
import re

LOG_FILE_PATH = r'C:\local\tmp\debugLog.txt'

class PyLog:
    def __init__(self, logFilePath=LOG_FILE_PATH):
        self.logFilePath = logFilePath
        self._logFile = open(logFilePath, 'w')
        
    def log2File(self, logObj):
        for line in str(logObj).split('\n'):
            self._logFile.write(line+'\n')

    def log2Scr(self, logObj):
        print(logObj)

    def log(self, logObj):
        self.log2Scr(logObj)
        self.log2File(logObj)

    def flush(self):
        self._logFile.flush()

    def close(self):
        self._logFile.close()

class Util:
    def __init__(self, pyLog):
        self.pyLog = pyLog

    def runCmd(self, cmd):
        return self.runCmdLog(cmd, False, False)

    def runCmdLog(self, cmd, cmdVerbose=True, retVerbose=True):
        cmdStr = '\n> %s\n%s' % (cmd, '-'*20)
        if cmdVerbose:
            self.pyLog.log2Scr(cmdStr)
        self.pyLog.log2File(cmdStr)
        
        ret = pykd.dbgCommand(cmd)
        if retVerbose:
            self.pyLog.log2Scr(ret)
        self.pyLog.log2File(ret)
        
        return ret

    def runCmdGetArgs(self, cmd, reObj):
        ret = self.runCmd(cmd)
        return [reObj.search(line)for line in ret.split('\n') if reObj.search(line)]

    @staticmethod
    def getDumpName():
        ret = pykd.dbgCommand(r'||')
        return ret.split('\\')[-1].strip()

    @staticmethod
    def ttt_test2end(content):
        if 'TTT Replay: End of trace reached.' in content \
           or 'TTT Replay: Start of trace reached.' in content:
            return True
        return False

    @staticmethod
    def ttt_test2Time(targetTime):
        ret = pykd.dbgCommand(r'.time')
        for line in ret.split('\n'):
            if 'Time Travel Position:' in line:
                currentTime = line.split()[-1].strip('.')
                break
        if int(targetTime, 16) < int(currentTime, 16):
            return True
        return False

if __name__ == '__main__':
    del LOG_FILE_PATH
    ret = Util.getDumpName()
    logPath = r'C:\local\tmp\debugLog-%s.txt' % ret
    pyLog = PyLog(logPath)
    util = Util(pyLog)
    ret = util.runCmd(r'||')
    pyLog.log(ret)
