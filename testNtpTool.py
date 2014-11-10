__author__ = 'xyang'
import time, os, socket, threading
import ntplib.ntplib as ntplib
from time import ctime


def getTimeFromNtpServer(server):
    start = time.time()
    c = ntplib.NTPClient()
    response = c.request(server, timeout = 1)
    tm1 = response.tx_time
    delay = time.time() - start

    # print
    # print "time:", tm1
    # print "spend:", time.time() - start
    # print "delay:", response.delay

    return tm1, delay




if __name__ == "__main__":
    tm2 = 0
    delay2 = 0

    while True:
        server1 = "ntp1.aliyun.com"
        tm1, delay1 = getTimeFromNtpServer(server1)

        time.sleep(1000)
        tm2, delay2= getTimeFromNtpServer(server1)

        print tm2 - tm1 - delay2