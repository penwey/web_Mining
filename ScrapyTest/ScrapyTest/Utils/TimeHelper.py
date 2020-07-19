import time


class TimeHelper:
    def getTime(self):
        currentTime = time.strftime('%Y-%m-%d', time.localtime())
        return currentTime
