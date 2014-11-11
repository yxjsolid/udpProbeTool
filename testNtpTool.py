__author__ = 'xyang'
import time, os, socket, threading
import ntplib.ntplib as ntplib
from time import ctime


def getTimeFromNtpServer(server):
    start = time.time()

    try :
        c = ntplib.NTPClient()
        response = c.request(server, timeout = 1)
        tm1 = response.tx_time
        clock = time.clock()
        delay = time.time() - start
        print "offset:", response.offset, "clock:%.03f"%clock
        return tm1, delay
    except Exception, e:
        print "timeout"
        return None, None
    # print
    # print "time:", tm1
    # print "spend:", time.time() - start
    # print "delay:", response.delay






if __name__ == "__main__":
    tm2 = 0
    delay2 = 0

    interval = 10
    print "interval:", interval

    while True:
        server1 = "ntp1.aliyun.com"
        tm1, delay1 = getTimeFromNtpServer(server1)

        time.sleep(interval)
        tm2, delay2= getTimeFromNtpServer(server1)

        time.sleep(interval)
