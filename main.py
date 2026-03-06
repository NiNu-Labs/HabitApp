import logging
from datetime import datetime
from engine import Engine
import pandas as pd
import warnings
logger = logging.getLogger("HabitApp")

SORT_MAP = {"id":"id","titel":"name","title":"name","name":"name","typ":"type","type":"type","start":"start","ende":"end","end":"end","aktiv":"active","active":"active"}



def get_input(prompt, cast_type=str, valid_options=None, allow_empty=False, ):
    while True:
        val = input(prompt).strip()

        # Falls die Eingabe leer ist und das erlaubt ist -> Sofort None zurückgeben
        if val == "" and allow_empty:
            return None
        
        # Falls die Eingabe leer ist, aber NICHT erlaubt -> Fehlermeldung und Loop von vorn
        if val == "" and not allow_empty:
            print("Fehler: Dieses Feld darf nicht leer sein.")
            continue

        # Falls Eingabe nicht leer ist aber ein falscher Wert eingegeben wurde bei vordefinierten Werten
        if valid_options and val.upper() not in [o.upper() for o in valid_options]:
            print(f"Fehler: Bitte wähle eine der Optionen: {', '.join(valid_options)}")
            continue

        try:
            if cast_type in [pd.Timestamp, "datetime"]:
                # Abfangen von Warnungen (wie MM.DD statt DD.MM)
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    
                    dt = pd.to_datetime(val, dayfirst=True, errors='raise')
                    
                    # Manuelle Korrektur: Wenn Tag/Monat vertauscht wurden, Fehler werfen
                    if len(w) > 0 and any("dayfirst" in str(warn.message) for warn in w):
                        raise ValueError("Zahlenformat unklar (Tag/Monat vertauscht?)")
                
                return dt.isoformat()
#            if inter:
#                if int(prompt) >= 7:
#                    raise ValueError("Es kann max 7 eingeben werden.")
            
            return cast_type(val)

        except (ValueError, TypeError, pd.errors.ParserError):
            type_name = "Datum (TT.MM.JJJJ)" if cast_type in [pd.Timestamp, "datetime"] else cast_type.__name__
            print(f"Fehler: Ungültige Eingabe. Erwartet wird: {type_name}")


                
def main():
    logging.basicConfig(filename='main.log', level=logging.INFO)
    logger.info("Started")
    
    maine = Engine(logger)
    
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
        
        if cmd[0] == "exit":
            logger.info("Exit App")
            break
        
    


if __name__ == "__main__":
    main()