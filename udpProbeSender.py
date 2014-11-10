__author__ = 'xyang'
from udpProbeTool import *

class udpProbeSender(udpProbe):
    def __init__(self, host):
        udpProbe.__init__(self, host)
        self.PORT = 4096
        self.probInterval = 5
        self.udpSocket = None
        self.initUdpSocket(host)
        self.lastProbeTime = None
        self.waitRspEvt = threading.Event()
        pass

    def initUdpSocket(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1)
        self.udpSocket = s

    def udpProbeSend(self, address):
        while True:
            buff = self.getCurrentTimeMsg()
            print "send:", buff, self.utc2TimeStr(buff)
            self.udpSend(buff, address)
            self.waitRspEvt.set()
            time.sleep(self.probInterval)

    def updReceiveResponse(self):
        while True:
            if self.waitRspEvt.wait():
                print "begin recieve resp"
                msg, address = self.udpReceive()
                print "receive:", msg, self.utc2TimeStr(buff), address
                self.waitRspEvt.clear()

    def udpProbeTask(self, address):
        self.runTask(self.udpProbeSend, (address,))
        self.runTask(self.updReceiveResponse, ())


if __name__ == "__main__":
    host = "10.103.12.150"
    tt =  time.time()
    print tt
    delay = 10 - tt%10 + 0.1

    print time.time()
    probe = udpProbeSender(host)

    probe.udpProbeTask(("10.103.12.21", 4096))
