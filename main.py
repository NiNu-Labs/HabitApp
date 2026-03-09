from datetime import datetime
from engine import Engine
import pandas as pd
from utils import get_input, validate_value

SORT_MAP = {"titel":"name","title":"name","name":"name","typ":"type","type":"type","start":"start","next":"next","ende":"end","end":"end","aktiv":"active","active":"active"}
ACTIONS = ["add", "list", "check-in", "exit", "help", "deactivate", "deac", "activate", "ac", "delete", "del"]   

def phelp():
    help_text = """
    ========================== 📝 HABIT-APP HILFE ==========================

    SCHNELLÜBERSICHT DER BEFEHLE:
    -----------------------------------------------------------------------
    add          : Neuen Habit erstellen (Interaktiver Assistent).
    list         - Alle Habits anzeigen (Optional mit Sortierung).
    check-in     - Fortschritt loggen (Heute oder spezifisches Datum).
    activate     - (Alias: ac) Einen inaktiven Habit reaktivieren.
    deactivate   - (Alias: deac) Habit pausieren (bleibt in der Liste).
    delete       - (Alias: del) Habit unwiderruflich löschen.
    exit         - Programm sicher beenden.

    DETAIILLIERTE ANLEITUNG:
    -----------------------------------------------------------------------

    1. DER 'add' BEFEHL (Erstellung)
       - Name: Wähle einen aussagekräftigen Titel.
       - Typ: 'good' (😇) für Gewohnheiten, die du aufbauen willst.
              'bad' (👿) für Laster, die du loswerden willst.
       - Dauer: Gib eine Zahl + Einheit an (z.B. '30D' für 30 Tage oder '12W').
       - Intervall: Bei Wochen (W) legst du fest, wie oft pro Woche (1-7) 
         du den Habit ausführen musst. Die App errechnet daraus die Termine.

    2. DER 'list' BEFEHL (Übersicht & Statistik)
       - Zeigt eine Tabelle mit deinem aktuellen Status.
       - ✅/❌/⏩ : Zeigt die absolute Anzahl (Erfolg/Fehlschlag/Übersprungen).
       - 🔥 Streak: Berechnet deine aktuelle Erfolgsserie. Wenn du einen Tag
         auf 'fail' (❌) setzt, bricht der Streak ab und startet bei 0.
       - Sortierung: Du kannst die Liste nach Name, Startdatum oder Status 
         sortieren lassen, um den Überblick zu behalten.

    3. DER 'check-in' BEFEHL (Logging)
       - 'check-in' ohne Zusatz prüft nur Habits, die heute fällig sind.
       - 'check-in YYYY-MM-DD' erlaubt das Nachholen für vergangene Tage.
       - Auswahl: Wähle die Nummer des Habits aus der angezeigten Liste.
       - Status: 
         [Y] = Success (Erfolg, zählt für den Streak)
         [N] = Fail (Fehlgeschlagen, bricht den Streak)
         [S] = Skip (Neutral, der Streak bleibt bestehen)

    HINWEIS ZUR DATENSICHERHEIT:
    -----------------------------------------------------------------------
    Deine Habits werden in 'habits.json' gespeichert. Alle täglichen 
    Fortschritte landen in 'habit.log'. Lösche diese Dateien nicht, 
    da sonst dein Fortschritt verloren geht!
    ========================================================================
    """
    return help_text


       


def welcome_msg():
    print("=" * 50)
    print("✨ WILLKOMMEN ZUR HABIT-APP ✨")
    print("=" * 50)
    print("Dein Werkzeug für bessere Gewohnheiten.")
    print("\nSchnellstart:")
    print("  -> Tippe 'add' um eine neue Gewohnheit zu starten.")
    print("  -> Tippe 'list' für deine Übersicht.")
    print("  -> Tippe 'help' für alle Details.")
    print("-" * 50)

def main():
    
    maine = Engine()
    welcome_msg()
    while True:
        # User Input
        raw = get_input("--> ", cast_type=str).strip()
        # Prüfen ob input leer dann continue
        if not raw:
            continue
        cmd = raw.split()
        
        if cmd[0] == "help":
            print(phelp())
        
        elif cmd[0] == "add":
            inter = None
            n = get_input("Name: ")
            t = get_input("Typ (good/bad): ", valid_options=["good", "bad"])
            s_date = get_input("Startdatum eingeben oder Leer lassen für heute.(DD-MM-YYYY): ", cast_type=pd.Timestamp, allow_empty=True) or None
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

            

            
        
        elif cmd[0] == "list":
            sort_choice = get_input("Sortieren? (Y/N):", valid_options=["Y", "N"])
            sort_by = None

            if sort_choice.upper() == "Y":
                sort_input = get_input("Sortieren nach (titel/typ/start/next/ende/aktiv): ").lower()

                if sort_input not in SORT_MAP:
                    print("Fehler: Bitte wähle eine der Optionen: id, titel, typ , start, ende, aktiv")
                    continue
                sort_by = SORT_MAP[sort_input]
            
            else:
                sort_by = None
            
            maine.list_habits(sort_by)

            
            
        elif cmd[0] in ["check-in", "check"]:
            #Datum Bestimmen
            if len(cmd) == 1:
                check_date = datetime.now().date().isoformat()
            else:
                try:
                    valid = validate_value(cmd[1], cast_type=pd.Timestamp)
                    check_date = pd.to_datetime(valid).date()
                except ValueError:
                    print(f"Falsches Datumsformat angegeben (DD-MM-YYYY): {cmd[1]}")
                    continue
            maine.check_main(check_date)
        

        elif cmd[0] in ["deactivate", "deac"]:
            maine.active_change("deactivate")

        elif cmd[0] in ["activate", "ac"]:
            maine.active_change("activate")

        elif cmd[0] in ["delete", "del"]:
            maine.active_change("delete")


        elif cmd[0] == "exit":
            break
        
        else:
            print(f"\n❌ '{raw}' ist kein bekannter Befehl.")
            print(f"💡 Versuche es mit: {', '.join(ACTIONS)}")
            print("❓ Tippe 'help' für eine detaillierte Anleitung.\n") 
            
    


if __name__ == "__main__":
    main()