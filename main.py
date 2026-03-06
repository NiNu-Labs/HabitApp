from datetime import datetime
from engine import Engine
import pandas as pd
from utils import get_input


SORT_MAP = {"id":"id","titel":"name","title":"name","name":"name","typ":"type","type":"type","start":"start","ende":"end","end":"end","aktiv":"active","active":"active"}





                
def main():
    
    maine = Engine()
    
    while True:
        # User Input
        raw = input("--> ").strip()
        # Prüfen ob input leer dann continue
        if not raw:
            continue
        cmd = raw.split()
        
        if cmd[0] == "add":
            inter = None
            n = get_input("Name: ")
            t = get_input("Typ (good/bad): ", valid_options=["good", "bad"])
            s_date = get_input("Startdatum eingeben (DD-MM-YYYY): ", cast_type=pd.Timestamp, allow_empty=True) or None
            if s_date is None:
                s_date = datetime.now().date().isoformat()
                print(f"-> Setze heute: {s_date}")

            dur_unit = get_input("Einheit Dauer (D = Tage, W = Wochen): ", valid_options=["D", "W"]).upper()
            dur_val = get_input("Dauer (Zahl): ", cast_type=int)

            if dur_unit == "W":
                
                while True:
                    inter = get_input("Wie oft in der Woche? (Zahl): ", cast_type=int)
                    if inter <= 7:
                        break
                    else:
                        print(f"-> Fehler: Eine Woche hat nur 7 Tage. Du kannst nicht {inter} mal wählen.")

            duration = f"{dur_val}{dur_unit}"
            ha = maine.add(n,t,duration,s_date, inter)
            print(f"Habit: {ha.name}; Art: {ha.type}; Start-Datum: {ha.start_date}; End-Datum: {ha.end_date}; Dauer: {ha.duration}" + (f"; {ha.interval}x die Woche."if ha.interval else""))

            

            
        
        if cmd[0] == "list":
            sort_choice = get_input("Sortieren? (Y/N):", valid_options=["Y", "N"])
            sort_by = None

            if sort_choice.upper() == "Y":
                sort_input = get_input("Sortieren nach (id/titel/typ/start/ende/aktiv): ").lower()

                if sort_input not in SORT_MAP:
                    print("Fehler: Bitte wähle eine der Optionen: id, titel, typ , start, ende, aktiv")
                    continue
                sort_by = SORT_MAP[sort_input]
            
            else:
                sort_by = None
            
            maine.list_habits(sort_by)

        if cmd[0] == "p":
            pass
            
            
        if cmd[0] == "check-in":
            #Datum Bestimmen
            if len(cmd) == 1:
                check_date = datetime.now().date().isoformat()
            else:
                check_date = pd.to_datetime(cmd[1]).date()
            maine.check_main(check_date)
        

        if cmd[0] in ["deactivate", "deac"]:
            maine.active_change("deactivate")

        if cmd[0] in ["activate", "ac"]:
            maine.active_change("activate")

        if cmd[0] in ["delete", "del"]:
            maine.active_change("delete")


        if cmd[0] == "exit":
            break
        
    


if __name__ == "__main__":
    main()