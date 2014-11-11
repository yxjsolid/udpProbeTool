__author__ = 'xyang'
from udpProbeTool import *

class udpProbeReceiver(udpProbe):
    def __init__(self, host):
        udpProbe.__init__(self, host)
        self.PORT = 4096
        self.probInterval = 5
        self.udpSocket = None
        self.initLogFile()
        self.initUdpSocket(host)
        self.lastProbeTime = None
        self.isFirst = True
        self.initClock = 0
        self.initTime = 0
        self.revCnt = 0
        self.waitRspEvt = threading.Event()
        pass

    def initLogFile(self):
        if not os.path.exists(self.logDir):
            os.mkdir(self.logDir)
        logFileName = os.path.join(self.logDir, "probe.log")
        self.logFd = open(logFileName, "a")

    def initUdpSocket(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, self.PORT))
        self.udpSocket = s

    def udpProbeResponse(self, receive, address):
        current = self.getCurrentTimeMsg()
        resp = receive + " " + current
        self.udpSend(resp, address)

    def udpReceiveProbe(self):
        cc = 0
        while True:
            msg, address = self.udpReceive()

            self.doLog(msg)
            self.lastProbeTime = time.time()
            self.udpProbeResponse(msg, address)

    def doLog(self, msg):
        if self.isFirst is True:
            self.initClock = time.clock()
            self.initTime = time.time()
            self.revCnt = 0
            self.isFirst = False
        else:
            self.revCnt += 1



        if self.lastProbeTime:
            interval = time.time() - self.lastProbeTime
        else:
            interval = 0

        receiveTm = self.utc2TimeStr(msg)
        localTm = self.utc2TimeStr(self.getCurrentTimeMsg())

        receiveUtc = float(msg)
        localUtc = time.time()

        if localUtc > receiveUtc:
            diff = "+%.2f"%(localUtc - receiveUtc)
        else:
            diff = "-%.2f"%(receiveUtc - localUtc)

        spendClock = time.clock() - self.initClock
        spendtime = time.time() - self.initTime
        real = self.revCnt * 5

        log = "receive:%s, local:%s, diff:%s interval:%.2f, spendClock:%.2f, spendtime:%.2f, real:%d"%(receiveTm, localTm, diff, interval, spendClock, spendtime, real)
        print log

        self.writeLog(log)


if __name__ == "__main__":
    host = "0.0.0.0"
    print time.time()
    probe = udpProbeReceiver(host)
    probe.udpReceiveProbe()
