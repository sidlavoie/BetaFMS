from datetime import datetime


class ScheduleConfiguration:
    def __init__(self):
        self.day = datetime.now()
        self.starttime = datetime(self.day.year, self.day.month, self.day.day, 10, 0)
        self.ambreaktime = datetime(self.day.year, self.day.month, self.day.day, 11, 0)
        self.lunchtime = datetime(self.day.year, self.day.month, self.day.day, 12, 0)
        self.pmbreaktime = datetime(self.day.year, self.day.month, self.day.day, 15, 0)
        self.cycletime = 10
        self.amduration = 10
        self.lunchduration = 60
        self.pmduration = 10
