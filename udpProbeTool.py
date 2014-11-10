__author__ = 'xyang'
import time, os, socket, threading

class udpProbe():
    def __init__(self, host):
        self.PORT = 4096
        self.probInterval = 5
        self.udpSocket = None
        self.initUdpSocket(host)
        self.lastProbeTime = None
        pass

    def initUdpSocket(self, host):
        pass

    def runTask(self, func, arg):
        tsk = threading.Thread(target=func, args=arg)
        tsk.start()

    def udpSend(self, buff, address):
        self.udpSocket.sendto(buff, address)

    def udpReceive(self):
        try:
            msg, address = self.udpSocket.recvfrom(1024)
            return msg, address
        except Exception, e:
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
