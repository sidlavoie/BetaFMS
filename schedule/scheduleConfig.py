from datetime import datetime


class ScheduleConfiguration:
    def __init__(self):
        self.day = datetime.now()
        self.starttime = datetime(self.day.year, self.day.month, self.day.day, 10, 30)
        self.ambreaktime = datetime(self.day.year, self.day.month, self.day.day, 11, 11, 2)
        self.lunchtime = datetime(self.day.year, self.day.month, self.day.day, 12, 0)
        self.pmbreaktime = datetime(self.day.year, self.day.month, self.day.day, 16, 0)
        self.cycletime = 10
        self.amduration = 14
        self.lunchduration = 50
        self.pmduration = 0
