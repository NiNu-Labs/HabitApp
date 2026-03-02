import uuid
from datetime import datetime
import pandas as pd


class Habit:
    """ """
    def __init__(self, name, type, period, frequency, start_date = None, habit_id = None, active = True):
        self.habit_id = habit_id or str(uuid.uuid4())
        self.name = name
        self.type = type 
        self.period = period # 'D' = Täglich, 'W' = Wöchentlich, 'MS' = Monatsanfang
        self.frequency = frequency
        self.start_date = start_date or datetime.now().date().isoformat() 
        self.active = active
    def calc_dates(self):
        start = pd.to_datetime(self.start_date)
        end = start + pd.DateOffset(end_date)
    
    # "3x pro Woche" bilden wir als '3 mal pro Woche' ab (z.B. Mo, Mi, Fr)
    # Hier nutzen wir eine wöchentliche Frequenz mit Anzahl
    # Einfacher Workaround für '3x pro Woche': Alle 2.3 Tage oder manuell:
    
        if self.frequency == "3W":
        # Erzeugt Termine mit Abstand von 2 Tagen (ca. 3x pro Woche)
            return pd.date_range(start=self.start_date, end=end, freq='2D')

        return pd.date_range(start=self.start_date, periods=self.period, freq=self.frequency)
        

        

class Engine:
    def __init__(self, logger):
        self.habits = {}
        self.logger = logger
        
        
        
    
    def add(self, name, type, period, frequency, start_date = None):
        habit = Habit(name, type, period, frequency, start_date)
        self.habits[habit.habit_id] = habit

        #save_csv
        return  habit.habit_id


    def print_habit(self, id):
        print(dir(self.habits[id]))
        

    def check_in(self, habit_id):
        """Eintragen und abhaken der Habits
Gelogt wird dann in main.py"""
# errechnen welche habits an diesem tag dran sind
# start_date *
        if habit_id in self.habits.keys():
            h = self.habits[habit_id]
            print(h)
            l = h.calc_dates()
            print(l)
            timestamp = datetime.now().date().isoformat()
            print(timestamp)
            return True
        return False

    def list_habits(self, habit_id):
        """Eintragen und abhaken der Habits
Gelogt wird dann in main.py"""
# errechnen welche habits an diesem tag dran sind
# start_date *
        if habit_id in self.habits.keys():
            h = self.habits[habit_id]
            print(h)
            l = h.calc_dates()
            print(l)
            timestamp = datetime.now().date().isoformat()
            print(timestamp)
            return True
        return False


    def active_change(self):
        """Ändern des Status active eines Habits """
        
        pass
    
    
    
    
        
    
    