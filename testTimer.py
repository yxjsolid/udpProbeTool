__author__ = 'xyang'
import time


if __name__ == "__main__":
    i = 0
    interval = 10
    cc = time.clock()
    while True:
        i +=1

        time.sleep(interval)
        c1 = time.clock() - cc

        print "interval:%d, clock:%.2f"%(i*interval, c1)