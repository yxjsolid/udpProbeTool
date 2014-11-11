__author__ = 'xyang'
from ctypes import *
import time






def testInterval():
    tTime = time.time()
    tClock = time.clock()

    while True:
        windll.Kernel32.Sleep(10*1000)
        tTimeDiff = time.time() - tTime
        tClockDiff = time.clock() - tClock
        print "time:%.2f, clock:%.2f"%(tTimeDiff, tClockDiff)



if __name__ == "__main__":
    testInterval()
