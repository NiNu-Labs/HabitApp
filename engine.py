from datetime import datetime
import uuid


class Habit:
    """ """
    def __init__(self, name, type, period, frequency, start_date = None, habit_id = None, active = True):
        self.habit_id = habit_id or uuid.uuid4()
        self.name = name
        self.type = type 
        self.period = period
        self.frequency = frequency
        self.start_date = start_date or datetime.now().date() 
        self.active = active
        

class Engine:
    def __init__(self,logger):
        self.habits = {}
        self.logger = logger
        


