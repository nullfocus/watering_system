from datetime import datetime as date
from math import floor

class Clock:
    def __init__(self, log):
        self.log = log
    
    def get_time(self):
        today = date.today()

        #0=sunday -> 6=saturday
        day_of_week = (today.weekday() + 1) % 7

        #96 total 15min blocks
        time_of_day = (today.hour * 4) + int(floor(today.minute / 15))

        #self.log(f"{day_of_week} {time_of_day} => {['sun', 'mon', 'tues', 'wed', 'thurs', 'fri', 'sat'][day_of_week]} {floor(time_of_day/4)}:{(time_of_day%4) * 15}")

        return day_of_week, time_of_day