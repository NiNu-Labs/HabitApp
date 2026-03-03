import uuid
from datetime import datetime
import pandas as pd


class Habit:
    """ """
    def __init__(self, name, type, period, frequency, interval, start_date = None, start_date = None, habit_id = None, active = True):
        self.habit_id = habit_id or str(uuid.uuid4())
        self.name = name
        self.type = type 
        self.period = period #z.B. 3M = Dauer 3 Monate
        self.frequency = frequency #z.B. 3W = 3x pro Woche
        self.interval = interval #häufigkeit bei "D"
        self.start_date = start_date or datetime.now().date().isoformat() 
        self.end_date = end_date
        self.active = active

    def calc_dates(self):
        
        #zerlegen von period
        p_num = int("".join(filter(str.isdigit, self.period)))
        p_unit = "".join(filter(str.isalpha, self.period)).upper()

        #Mapping Pandas DateOffset (echter Kalender)
        offset_map = {"D": "days", "W": "weeks"}
        unit_key = offset_map.get(p_unit, "days")

        #Berechnung genaues Ende im Kalender
        end_date = self.start_date + pd.DateOffset(**{unit_key: p_num})

        #zerlegen von frequency
        f_num = int("".join(filter(str.isdigit, self.period)))
        f_unit = "".join(filter(str.isalpha, self.period)).upper()

        if f_unit == 'W':
            # "3x pro Woche" -> Intervall alle 2.3 Tage
            actual_freq = f"{round(7/f_num, 1)}D"
        elif f_unit == 'M':
            # "X mal pro Monat" -> Intervall basierend auf ø 30.4 Tagen
            actual_freq = f"{round(30.4/f_num, 1)}D"
        else:
            # Standard: Täglich
            actual_freq = 'D'

        if self.period == "D":
            pass
        elif self.period == "W":
            liste = []
            for i in pd.date_range(start='2026-03-02', periods=3, freq='W'):
                liste.extend(pd.date_range(start=i, periods=3, freq='56h'))

            s = sorted(list(set(liste)))
            out = [[datum, False] for datum in [d.strftime('%Y-%m-%d') for d in s]]
            return out
            
    # "3x pro Woche" bilden wir als '3 mal pro Woche' ab (z.B. Mo, Mi, Fr)
    # Hier nutzen wir eine wöchentliche Frequenz mit Anzahl
    # Einfacher Workaround für '3x pro Woche': Alle 2.3 Tage oder manuell:

        

        

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
    
    
    
    
        
    
    