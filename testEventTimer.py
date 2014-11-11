__author__ = 'xyang'
import threading, time

if __name__ == "__main__":
    i = 0
    evt = threading.Event()
    interval = 10
    cc = time.clock()
    while True:
        i +=1

        evt.wait(timeout=interval)
        c1 = time.clock() - cc

        print "interval:%d, clock:%.2f"%(i*interval, c1)