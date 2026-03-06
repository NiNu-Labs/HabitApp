import uuid
import os
import pandas as pd
import json
from datetime import datetime

class Habit:
    """ """
    def __init__(self, name, type, duration, start_date, interval = None,  habit_id = None, active = True):
        self.habit_id = habit_id or str(uuid.uuid4())
        self.name = name
        self.type = type 
        self.duration = duration #z.B. 3W = 3 Wochen 
        self.interval = interval #häufigkeit in der woche 
        self.start_date = pd.to_datetime(start_date).date() 
        self.end_date = self.calc_end().date()
        self.active = active
    def calc_end(self):
        #zerlegen von period
        p_num = int("".join(filter(str.isdigit, self.duration)))
        p_unit = "".join(filter(str.isalpha, self.duration)).upper()

        #Mapping Pandas DateOffset (echter Kalender)
        offset_map = {"D": "days", "W": "weeks"}
        unit_key = offset_map.get(p_unit, "days")
        #Berechnung genaues Ende im Kalender
        start = pd.to_datetime(self.start_date).date()
        return start + pd.DateOffset(**{unit_key: p_num})
    
    def calc_dates(self):
        #zerlegen von frequency
        f_num = int("".join(filter(str.isdigit, self.duration)))
        f_unit = "".join(filter(str.isalpha, self.duration)).upper()
        _liste = []
        if f_unit == 'D':
            _liste(pd.date_range(start=self.start_date, periods=f_num, freq='56h'))
        elif f_unit == 'W':
            actual= f"{round(30.4/f_num, 1)}D"
            for i in pd.date_range(start=self.start_date, periods=f_num, freq='W'):
                _liste.extend(pd.date_range(start=self.start_date, periods=self.interval, freq=actual))
        
        return list(_liste)
       


            
    # "3x pro Woche" bilden wir als '3 mal pro Woche' ab (z.B. Mo, Mi, Fr)
    # Hier nutzen wir eine wöchentliche Frequenz mit Anzahl
    # Einfacher Workaround für '3x pro Woche': Alle 2.3 Tage oder manuell:

        

        

class Engine:
    def __init__(self, logger):
        self.habits = {}
        self.logger = logger
        self.file_habits= "test.json"
        self.load()
        
    def save(self):
        print()
           
        data = {
            
            "habits": [
                { "habit_id": str(h.habit_id),
                 "name": h.name,
                 "type": h.type,
                 "duration": h.duration,
                 "interval": h.interval,
                 "start_date": str(h.start_date),
                 "end_date": str(h.end_date),
                 "active": h.active}
                for h in self.habits.values()
            ]
        }
        
        try:
            
            with open(self.file_habits, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Erfolg: {len(data['habits'])} Habits wurden in  gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
        
    def load(self):
        
        if not os.path.exists(self.file_habits):
            print("Keine Speicherdatei gefunden. Starte mit leerer Liste.")
            self.habits = {} # Sicherstellen, dass das Dict existiert
            return
        try:
            with open(self.file_habits, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for h in data.get("habits", []):
    #(self, name, type, duration, start_date, interval = None,  habit_id = None, active = True)
                ha= Habit(h["name"], h["type"], h["duration"], h["start_date"], interval=h["interval"], habit_id=h["habit_id"], active= h["active"] )
                self.habits[ha.habit_id] = ha
                
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
        
        
    def add(self, name, type, duration, start_date, _interval=None ):
        habit = Habit(name, type, duration, start_date, interval=_interval )
        self.habits[habit.habit_id] = habit
        self.save()
        #save_csv
        return  habit


    def print_habit(self, id):
        print(dir(self.habits[id]))
        

    def get_due_habits(self, check_date):
        due_habits = []
        check_date = pd.to_datetime(check_date).date()

        for habit in self.habits.values():
            if not habit.active:
                continue
            if check_date in habit:
                due_habits.append(habit)
                
        due_habits_list = [(i+1, h) for i, h in enumerate(due_habits)]
        return due_habits_list
        

    def check_in(self, habit_id, check_date=datetime.now().date().isoformat()):
        """Eintragen und abhaken der Habits
Gelogt wird dann in main.py"""
# errechnen welche habits an diesem tag dran sind
# start_date *
        if habit_id in self.habits.keys():
            h = self.habits[habit_id]

            print(f"\nHabit: {h.name}")
            print(f"Typ: {h.type}")
            print(f"Datum: {check_date}")
            print(f"Erfolg? (Y/N): ")

            user_input = input("--> ").strip().lower()

            if user_input == "y":
                print(f"✅ {h.name} erledigt.")
            elif user_input == "n":
                print(f"❌ {h.name} nicht erledigt.")
            else:
                print("Ungültige Eingabe.")
                return False
            
            timestamp = datetime.now().date().isoformat()
            print(f"Check-in für {timestamp}")
            
            return True
        return False
    
    
    def check_main(self, check_date):
         #fällige Habits einholen
        due_habits = self.get_due_habits(check_date)

        if not due_habits:
            print(f"keine Habits fällig am {check_date}")
            return
                
            #Anzeige Habits
        print(f"\nFällige Habits am {check_date}")
        for nr, habit in due_habits:
            print(f"{nr}) {habit.name}")

            #Auswahl Habits
        try:
            nr = int(input("--> "))
            for num, habit in due_habits:
                if num == nr:
                    self.check_in(habit.habit_id, check_date)
                    break

        except:
            print("Bitte eine gültige Nummer eingeben!")
        

    def list_habits(self, sort_by=None):
        """Alle Habits in einer Tabelle anzeigen"""

        habits = list(self.habits.values())

        # Sortierung
        if sort_by is not None:
            sort_by = sort_by.lower()

            if sort_by in ["id", "ID", "Id"]:
                habits.sort(key=lambda h: h.habit_id)

            elif sort_by in ["titel", "title", "name"]:
                habits.sort(key=lambda h: h.name.lower())

            elif sort_by in ["type", "type"]:
                habits.sort(key=lambda h: h.type)

            elif sort_by == "start":
                habits.sort(key=lambda h: h.start_date)
        
            elif sort_by in ["end", "ende"]:
                habits.sort(key=lambda h: h.end_date)

            elif sort_by in ["aktive", "aktiv"]:
                habits.sort(key=lambda h: h.active, reverse=True)

        # NEXT STATUS STREAK sobald log.csv stehen hier einfügen
        
        # Tabellenkopf
        print(
            f"\n{'Titel':<15} | {'Typ':<5} | "
            f"{'Start':<10} | {'Ende':<10} | {'Aktiv':<5} | {'ID':<5} "
            )
        print("-" * 120)

        # Tabelleninhalt
        for h in habits:
            
            print(
                
                f"{h.name: <15} | "
                f"{h.type: <5} | "
                f"{str(h.start_date): <5} | "
                f"{str(h.end_date): <5} | "
                f"{str(h.active): <5} | "
                f"{h.habit_id: <5} | "
            )
            




    def active_change(self):
        """Ändern des Status active eines Habits """
        
        pass
    
    
    
    
        
    
    