import uuid
import os
import pandas as pd
import json
from datetime import datetime
from utils import get_input

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
        self.status = self.init_status()
        self.current_streak = 0
        self.active = active
    
    log_id = 1
    
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
        """Erstellt eine Liste aller fälligen Daten als Python-date Objekte."""
        try:
            f_num = int("".join(filter(str.isdigit, self.duration)))
            f_unit = "".join(filter(str.isalpha, self.duration)).upper()
        except ValueError:
            return []

        _liste = []
        if f_unit == 'D':
            # Täglich: Erzeuge Datumsliste für die Dauer von f_num Tagen
            _liste = pd.date_range(start=self.start_date, periods=f_num, freq='D').date.tolist()
            
        elif f_unit == 'W':
            # Wöchentlich: Intervall gibt an, wie oft pro Woche
            if self.interval:
                actual_freq = f"{round(7/self.interval, 1)}D"
                # Loop über die Anzahl der Wochen (f_num)
                for i in pd.date_range(start=self.start_date, periods=f_num, freq='W'):
                    dates = pd.date_range(start=i, periods=self.interval, freq=actual_freq).date.tolist()
                    _liste.extend(dates)
        
        # Dubletten entfernen (falls durch Rundung Daten doppelt sind)
        
        return sorted(list(set(_liste)))
        
    def calc_streak(self):
        
        current_date = datetime.now().date().isoformat()
        current_streak = 0
        best_streak = 0

        for status in self.status:
            if status[1] is None or status[1] == "skip":
                continue
            
            if status[1] == "success":
                current_streak += 1
                #streak überschreiben wenn current_streak > best_streak
                if current_streak > best_streak:
                    best_streak = current_streak
                if status[0] == current_date:
                    break
            else: #status == "fail"
                current_streak = 0    
        return {"current":current_streak, "best":best_streak}

    def next_due(self):
        """Gibt das nächste fällige Datum zurück"""
        today = datetime.now().date()
        if self.active:
            for date, status in self.status:
                if date >= today and status is None:
                    return date
        return None

    def log(self, _file, status, date ):
        try:
            with open(_file, "a", encoding="utf-8") as f:
                f.write(f"{self.log_id}:{self.habit_id}:{date}:{status}:\n")
            print(f"Status gespeichert. {status}.")
            Habit.log_id += 1
            
        except Exception as e:
            print(f"Fehler beim logSpeichern: {e}")
    
    
    def init_status(self):
        return [[datum, None] for datum in self.calc_dates()]
    
    def status_statistik(self):
        count = len(self.status)
        success = [item for item in self.status if item[1] == "success"]
        fail = [item for item in self.status if item[1] == "fail"]
        skip = [item for item in self.status if item[1] == "skip"]

        #check ob current streak die beste ist
        streaks = self.calc_streak()
        
        if streaks["current"] < streaks["best"]:
            streak_text = f"{streaks['current']} (Best: {streaks['best']})"
        else:
            streak_text = f"{streaks['current']}"

        return {
            "count":count, 
            "success":[len(success), (len(success) / count) * 100 ], 
            "fail":[len(fail), (len(fail) / count * 100)],
            "skip":len(skip),            
            "streak_display": streak_text
            }
       



        

        

class Engine:
    def __init__(self):
        self.habits = {}
        self.file_habits= "habits.json"
        self.file_log = "habit.log"
        self.load()
        self.load_log()
        
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
    
    def load_log(self):
        if not os.path.exists(self.file_log):
            print("Keine Log-Datei gefunden.")
            return
        try:
            with open(self.file_log, "r", encoding="utf-8") as f:
                lines = f.readlines()

        except Exception as e:
            print(f"Fehler beim Lesen des Logs: {e}")
            
        for line in lines:
            arg = line.split(":")
            id = arg[1]
            date = pd.to_datetime(arg[2]).date()
            status = arg[3]
            
            for i,s in enumerate(self.habits[id].status):
                
                if s[0] == date:
                    s[1] = status
                
        Habit.log_id = int(lines[-1][0]) +1
          
    def add(self, name, type, duration, start_date, _interval=None ):
        habit = Habit(name, type, duration, start_date, interval=_interval )
        self.habits[habit.habit_id] = habit
        self.save()
        #save_csv
        return  habit


    def print_habit(self, id):
        print(dir(self.habits[id].status_statistik()))
        

    def get_due_habits(self, check_date):
        """Gibt eine nummerierte Liste von Habit-Objekten zurück, die am check_date fällig sind."""
        due_habits = []
        
        # Wir wandeln das Zieldatum in einen reinen String um: "2026-03-10"
        target_date_str = pd.to_datetime(check_date).strftime('%Y-%m-%d')
        
        print(f"Suche nach: {target_date_str}") # Debug

        for habit in self.habits.values():
            if not habit.active:
                continue
            
            # Wir holen die Liste und wandeln jedes Element darin in einen String um
            # Das eliminiert alle Probleme mit datetime.date vs pandas.Timestamp
            scheduled_dates = habit.calc_dates()
            scheduled_strings = [d.strftime('%Y-%m-%d') for d in scheduled_dates]
            
            # Debug: Nur wenn nötig aktivieren, sonst wird die Konsole geflutet
            #print(f"Habit {habit.name} Termine: {scheduled_strings}") 
            
            if target_date_str in scheduled_strings:
                due_habits.append(habit)
        
        return [(i + 1, h) for i, h in enumerate(due_habits)]
        

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
            print("Status: (Y = Success, N = Fail, S = Skip): ")

            user_input = get_input("---> ", cast_type=str, valid_options=["Y","N","S"]).strip().upper()
            
            #check_date in date-Objekt umwandeln
            
            check_date = pd.to_datetime(check_date)
            
            if user_input == "Y":
                h.log(self.file_log, "success", check_date)
                print(f"✅ {h.name} am {check_date.strftime("%d-%m-%Y")} erledigt.")
            elif user_input == "N":
                h.log(self.file_log, "fail", check_date)
                print(f"❌ {h.name} am {check_date.strftime("%d-%m-%Y")} nicht erledigt.")
            elif user_input == "S":
                h.log(self.file_log, "skip", check_date)
                print(f"⏩ {h.name} am {check_date.strftime("%d-%m-%Y")} übersprungen.")
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
        
        nr = get_input("---> ", cast_type=int)
        for num, habit in due_habits:
            if num == nr:
                self.check_in(habit.habit_id, check_date)
                break
        return True

        

    def list_habits(self, sort_by=None):
        """Alle Habits in einer Tabelle anzeigen"""

        habits = list(self.habits.values())

        # Sortierung
        if sort_by is not None:
            sort_by = sort_by.lower()

            if sort_by in ["titel", "title", "name"]:
                habits.sort(key=lambda h: h.name.lower())

            elif sort_by in ["type", "type"]:
                habits.sort(key=lambda h: h.type)

            elif sort_by == "start":
                habits.sort(key=lambda h: h.start_date)

            elif sort_by == "next":
                habits.sort(key=lambda h: str(h.next_due()) or datetime.max.date())
        
            elif sort_by in ["end", "ende"]:
                habits.sort(key=lambda h: h.end_date)

            elif sort_by in ["aktive", "aktiv"]:
                habits.sort(key=lambda h: h.active, reverse=True)

        # Maximale Namenslänge finden
        max_name_len = max([len(h.name) for h in habits])
        # Tabellenkopf
        print(
            f"\n{'Titel':<{max_name_len}} | {'Aktiv':^6} | {'Typ':^6}  | "
            f"{'Start':^10} | {'Next':^10} | {'Ende':^10} | {'✅ /❌ /⏩':^6}  | {'🔥 Streak':<3}"
            )
        print("-" * (max_name_len + 60))

        # Tabelleninhalt
        for h in habits:
            active_emoji = "🟢" if h.active else "🔴"
            type_emoji = "😇" if h.type == "good" else "👿"
            stat = h.status_statistik()
            
            next_date = h.next_due()
            if next_date:
                next_str = next_date.strftime('%d-%m-%Y')
            else:
                next_str = "----------"
                
            print(
                
                f"{h.name: <{max_name_len}} | "
                f"{active_emoji: ^5} | "
                f"{type_emoji: ^6} | "
                f"{h.start_date.strftime('%d-%m-%Y'): ^10} | " 
                f"{next_str: ^10} | "                 
                f"{h.end_date.strftime('%d-%m-%Y'): ^10} | "
                f" {stat['success'][0]:^2}/ {stat['fail'][0]:^2}/ {stat['skip']:^2} | "
                f" {stat['streak_display']:<3}"
            )
        return True

                
            

    def active_change(self, mode):
        """Ändern des Status active eines Habits """
        if mode == "activate":
            #nur inaktive habits anzeigen
            habits = [ h for i, h in enumerate(self.habits.values()) if not h.active]
            if not habits:
                print("Keine inaktiven Habits vorhanden.")
                return
        elif mode == "deactivate":
            #nur aktive habits anzeigen
            habits = [h for i, h in enumerate(self.habits.values()) if h.active]
            if not habits:
                print("Keine aktiven Habits vorhanden.")
                return
        elif mode == "delete":
            habits = [h for i, h in enumerate(self.habits.values())]

        #Habits anzeigen
        

        # Alle Habits für die maximale Nummer (nicht gefiltert)
        
        max_nr_global = len(habits) 
        breite = len(str(max_nr_global))  # dynamische breite der Auswahlnummern bei 10 = xx / bei 100 = xxx
        print("\nHabits: ")
        for nr, habit in enumerate(habits):
            
            modeprint = "🟢" if habit.active else "🔴"
            print(f"{nr+1:{breite}}) {modeprint} {habit.name}")
    
        #Auswählen und Ändern
        nr = get_input("---> ", cast_type=int)
        if type(nr) is int:
            nr -= 1
        for num, habit in enumerate(habits):
            if num == nr:
                if mode == "delete":
                    confirm = get_input(f"Soll \"{habit.name}\" wirklich gelöscht werden? (Y/N): ", valid_options=["Y", "N"])
                    if confirm == "y":
                        del self.habits[habit.habit_id]
                        print(f"Habit \"{habit.name}\" wurde erfolgreich entfernt.")
                else:
                    #active/inactive umschalten
                    habit.active = not habit.active
                    print(f"Habit \"{habit.name}\" ist jetzt {"aktiv" if habit.active else "inaktiv"}.")
                self.save()
            if nr == "exit":
                pass
            else:
                print(f"Fehler: Wähle eine Nummer von 1 bis {max_nr_global}.")    
            return
        return True
