__author__ = 'xyang'
import time, os, socket, threading

class udpProbe():
    def __init__(self, host):
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
        #s.bind((host, self.PORT))
        self.udpSock = s

    def __runTask(self, func, arg):
        tsk = threading.Thread(target=func, args=arg)
        tsk.start()

    def udpProbeSend(self, address):
        while True:
            buff = self.getCurrentTimeMsg()
            print "send:", buff
            self.udpSend(buff, address)
            self.waitRspEvt.set()
            time.sleep(self.probInterval)
        pass


    def udpProbeTask(self, address):
        self.__runTask(self.udpProbeSend, (address,))
        self.__runTask(self.updReceiveResponse, ())

    def udpSend(self, buff, address):
        self.udpSock.sendto(buff, address)

    def udpProbeResponse(self, receive, address):
        current = self.getCurrentTimeMsg()
        resp = receive + " " + current
        self.udpSend(resp, address)

    def updReceiveResponse(self):
        while True:
            if self.waitRspEvt.wait():
                print "begin recieve resp"
                msg, address = self.udpReceive()
                print "receive:", msg, address
                self.waitRspEvt.clear()


    def udpReceiveProbe(self):
        while True:
            msg, address = self.udpReceive()
            if self.lastProbeTime:
                print "interval:", time.time() - self.lastProbeTime
            self.lastProbeTime = time.time()
            self.udpProbeResponse(msg, address)

    def udpReceive(self):
        try:
            msg, address = self.udpSock.recvfrom(1024)
            return msg, address
        except Exception, e:
            print "timeout"
            return None, None

    def getCurrentTimeMsg(self):
        localTime =  time.localtime()
        H = localTime.tm_hour
        M =  localTime.tm_min
        S = localTime.tm_sec
        tt =  time.time()
        MS = (tt - int(tt))*100
        tmStr = "%02d:%02d:%02d.%02d"%(H, M, S, MS)
        return tmStr

if __name__ == "__main__":
    host = "10.103.12.150"

    tt =  time.time()
    print tt
    delay = 10 - tt%10 + 0.1

    #time.sleep(delay)
    print time.time()

    probe = udpProbe(host)
    probe.udpProbeTask(("10.103.12.21", 4096))

    #probe.udpReceive()