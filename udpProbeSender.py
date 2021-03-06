__author__ = 'xyang'
from udpProbeTool import *

class udpProbeSender(udpProbe):
    def __init__(self, host, targetInfo):
        udpProbe.__init__(self, host)
        self.target, self.targetName = targetInfo
        self.PORT = 4096
        self.probInterval = 5
        self.udpSocket = None
        self.initLogFile()
        self.initUdpSocket(self.host)
        self.lastProbeTime = None
        self.waitRspEvt = threading.Event()
        pass

    def initLogFile(self):
        if not os.path.exists(self.logDir):
            os.mkdir(self.logDir)
        logFileName = os.path.join(self.logDir, "%s.log"%self.targetName)
        self.logFd = open(logFileName, "a")

    def initUdpSocket(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1)
        self.udpSocket = s

    def udpProbeSend(self, address):
        self.waitDelay()
        while True:
            buff = self.getCurrentTimeMsg()
            #print "send:", buff, self.utc2TimeStr(buff)
            self.udpSend(buff, address)
            self.waitRspEvt.set()
            time.sleep(self.probInterval)

    def updReceiveResponse(self):
        while True:
            if self.waitRspEvt.wait():
                msg, address = self.udpReceive()
                if msg:
                    self.logResponse(msg)
               # print "receive:", msg, self.utc2TimeStr(probeTm), self.utc2TimeStr(respTm), address
                self.waitRspEvt.clear()

    def udpProbeTask(self):
        address = (self.target, self.PORT)
        self.runTask(self.udpProbeSend, (address,))
        self.runTask(self.updReceiveResponse, ())

    def waitDelay(self):
        tt =  time.time()
        delay = 10 - tt%10 + 0.1
        time.sleep(delay)

    def logResponse(self, msg):
        probeTm, respTm = msg.split()
        probeUtc = float(probeTm)
        respUtc = float(respTm)

        if probeUtc > respUtc:
            diff = "-%.2f"%(probeUtc - respUtc)
        else:
            diff = "+%.2f"%(respUtc - probeUtc)

        log =  "probe:%s, resp:%s, diff:%s"%(self.utc2TimeStr(probeTm), self.utc2TimeStr(respTm), diff)
        print log

        self.writeLog(log)


if __name__ == "__main__":
    host = "10.103.12.21"

    serverList = [
        ("182.254.210.23",  "qcloud"),
        ("115.29.210.164",  "Server_2"),
        ("121.40.213.94",   "Server_3"),
        ("121.40.213.66",   "server_4"),
        ("121.41.24.35",    "server_5"),
        ("121.40.214.109",  "server_6"),
        ("121.40.213.68",   "server_7"),
        ("121.40.213.133",  "server_8"),
        ("121.41.24.56",    "server_9"),

        ]
    for target in serverList:
        probe = udpProbeSender(host, target)
        probe.udpProbeTask()
