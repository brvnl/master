from datetime import datetime
from dateutil.relativedelta import relativedelta

class Calendar:

    def __init__(self, filePath):
        self.file = filePath
        self.nBusDaysDict = {}
        self.readData()

    def readData(self):
        with open(self.file) as f:
            lines = f.readlines()

        self.nBusDaysDict = {l.rstrip():1 for l in lines if (l[:2] != "//")}
    
    def printCalendar(self):
        print(self.nBusDaysDict.keys())

    def isBusinessDay(self, aDate):
        if aDate.replace("-", "").replace("/", "") in self.nBusDaysDict:
            return False
        else:
            return True

    def previousBusinessDay(self, aDate):
        dt_obj = datetime.strptime(aDate.replace("-", "").replace("/", ""), '%Y%m%d')
        dt_obj = dt_obj + relativedelta(days=-1)

        while(not self.isBusinessDay(dt_obj.strftime("%Y%m%d"))):
            dt_obj = dt_obj + relativedelta(days=-1)

        return dt_obj.strftime("%Y-%m-%d")


    def nextBusinessDay(self, aDate):
        dt_obj = datetime.strptime(aDate.replace("-", "").replace("/", ""), '%Y%m%d')
        dt_obj = dt_obj + relativedelta(days=+1)

        while(not self.isBusinessDay(dt_obj.strftime("%Y%m%d"))):
            dt_obj = dt_obj + relativedelta(days=+1)

        return dt_obj.strftime("%Y-%m-%d")