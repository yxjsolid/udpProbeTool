__author__ = 'xyang'
import ntplib.ntplib as ntplib
import time, threading

class LOCAL_TIME():
    def __init__(self):
        print "begin init local time"
        self.initTimeStamp, self.initClock = self.initLocalTime()
        tmstr = self.utc2TimeStr(self.initTimeStamp)
        print "time:", tmstr
        pass

    def initLocalTime(self):
        tm, offset = self.getNtpTime()
        return tm, time.clock()

    def getNtpTime(self):
        while True:
            server = "ntp1.aliyun.com"
            try:
                c = ntplib.NTPClient()
                response = c.request(server, timeout = 1)
                tm1 = response.tx_time
                offset = response.offset
                return tm1, offset
            except Exception, e:
                print "timeout"

    def getLocalTimeUTC(self):
        diff = time.clock() - self.initClock
        return self.initTimeStamp + diff

    def getLocalTimeStr(self):
        utc = self.getLocalTimeUTC()
        utcstr = self.utc2TimeStr(utc)
        print "time:", utcstr

    def utc2TimeStr(self, utc):
        tmStruct = time.localtime(utc)
        H = tmStruct.tm_hour
        M =  tmStruct.tm_min
        S = tmStruct.tm_sec
        MS = (utc - int(utc))*100
        tmStr = "%02d:%02d:%02d.%02d"%(H, M, S, MS)
        return tmStr

    def checkLoclTime(self):
        self.__runTask(self.__checkLocalTime, ())

    def __checkLocalTime(self):
        while True:
            ntpTime, offset = self.getNtpTime()
            localTime = self.getLocalTimeUTC()
            print "diff:%.3f"%(ntpTime - localTime), "offset:%.4f"%offset
            time.sleep(10)

        pass

    def __runTask(self, func, arg):
        tsk = threading.Thread(target=func, args=arg)
        tsk.start()


if __name__ == "__main__":

    localtime = LOCAL_TIME()
    time.sleep(10)
    localtime.getLocalTimeStr()

    localtime.checkLoclTime()