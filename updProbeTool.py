__author__ = 'xyang'
import time, os, socket, threading

class udpProbe():
    def __init__(self, host):
        self.PORT = 4096
        self.udpSocket = None
        self.initUdpSocket(host)
        pass

    def initUdpSocket(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, self.PORT))
        self.udpSock = s

    def __runTask(self, func, arg):
        tsk = threading.Thread(target=func, args=arg)
        tsk.start()

    def udoProbeSend(self, address):
        buff = self.getTimestamp()
        self.udpSend(buff, address)
        pass

    def udpSend(self, buff, address):
        self.udpSock.sendto(buff, address)

    def udpReceive(self):
        msg, address = self.udpSock.recvfrom(1024)
        print address
        print msg

    def getTimestamp(self):
        localTime =  time.localtime()
        H = localTime.tm_hour
        M =  localTime.tm_min
        S = localTime.tm_sec
        tt =  time.time()
        MS = (tt - int(tt))*100

        tmStr = "%02d:%02d:%02d.%02d"%(H, M, S, MS)
        print tmStr
        return tmStr

if __name__ == "__main__":
    host = "10.103.12.150"

    tt =  time.time()
    print tt
    delay = 10 - tt%10

    time.sleep(delay)
    #print 10 - tt%10
    print time.time()




    probe = udpProbe(host)
    probe.getTimestamp()

    probe.udoProbeSend(("10.103.12.150", 4096))

    probe.udpReceive()