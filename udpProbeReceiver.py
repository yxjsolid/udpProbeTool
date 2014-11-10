__author__ = 'xyang'
from udpProbeTool import *

class udpProbeReceiver(udpProbe):
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
        s.bind((host, self.PORT))
        self.udpSocket = s


    def udpProbeResponse(self, receive, address):
        current = self.getCurrentTimeMsg()
        resp = receive + " " + current
        self.udpSend(resp, address)

    def udpReceiveProbe(self):
        while True:
            msg, address = self.udpReceive()
            self.doLog(msg)
            self.lastProbeTime = time.time()
            self.udpProbeResponse(msg, address)

    def doLog(self, msg):
        if self.lastProbeTime:
            interval = time.time() - self.lastProbeTime
        else:
            interval = 0

        log = "receive:%s, local:%s, interval:%.2f"%(msg, self.getCurrentTimeMsg(), interval)
        print log


if __name__ == "__main__":
    host = "0.0.0.0"
    print time.time()
    probe = udpProbeReceiver(host)
    probe.udpReceiveProbe()
