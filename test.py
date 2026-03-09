from datetime import datetime
def get_input(prompt, cast_type=str, valid_options=None):
    while True:
        try:
            val = input(prompt).strip()
            # Falls eine Liste an erlaubten Werten mitgegeben wurde (z.B. ["D", "W"])
            if valid_options and val.upper() not in [o.upper() for o in valid_options]:
                print(f"Fehler: Bitte wähle eine der Optionen: {', '.join(valid_options)}")
                continue
            
            # Versuche den Datentyp umzuwandeln (z.B. zu int)
            return cast_type(val)
        except ValueError:
            print(f"Fehler: Ungültige Eingabe. Erwartet wird: {cast_type.__name__}")

# Anwendung in deinem Code:
inter = None
n = get_input("Name: ")
t = get_input("Typ (good/bad): ", valid_options=["good", "bad"])
s_date = input("Startdatum (YYYY-MM-DD) [Leer lassen für heute]: ").strip() or None
if s_date is None:
    print(f"-> Setze heute: {datetime.now().date().isoformat()}")    

dur_unit = get_input("Einheit Dauer (D = Tage, W = Wochen): ", valid_options=["D", "W"]).upper()
dur_val = get_input("Dauer (Zahl): ", cast_type=int)

if dur_unit == "W":
    inter = get_input("Wie oft in der Woche? (Zahl): ", cast_type=int)

duration = f"{dur_val}{dur_unit}"

print(f"{n}  {t} {s_date} {dur_unit} {dur_val} {duration} {inter }")

def get_input(prompt, cast_type=str, valid_options=None, allow_empty=False):
    while True:
        val = input(prompt).strip()

        if val == "" and allow_empty:
            return None
        
        if val == "" and not allow_empty:
            print("Fehler: Dieses Feld darf nicht leer sein.")
            continue
        
        try:
                # Falls eine Liste an erlaubten Werten mitgegeben wurde (z.B. ["D", "W"])
            if valid_options and val.upper() not in [o.upper() for o in valid_options]:
                print(f"Fehler: Bitte wähle eine der Optionen: {', '.join(valid_options)}")
                continue
            
                # Versuche den Datentyp umzuwandeln (z.B. zu int)
            return cast_type(val)
        except ValueError:
            name = cast_type.__name__ 
            if 
            print(f"Fehler: Ungültige Eingabe. Erwartet wird: {cast_type.__name__}")

def validate_date(date_str):
    """Prüft, ob der String dem Format YYYY-MM-DD entspricht."""
    # datetime.strptime wirft einen ValueError, wenn das Format nicht stimmt
    datetime.strptime(date_str, "%Y-%m-%d")
    return date_str


def get_input(prompt, cast_type=str, valid_options=None, allow_empty=False):
    while True:
        val = input(prompt).strip()

        if val == "" and allow_empty:
            return None
        
        if valid_options and val.upper() not in [o.upper() for o in valid_options]:
            print(f"Fehler: Bitte wähle eine der Optionen: {', '.join(valid_options)}")
            continue

        try:
            # Spezialfall: Datum (wird immer als ISO-String zurückgegeben)
            if cast_type in [pd.Timestamp, "datetime"]:
                # Erkennt fast alles: 05.03.2024, 2024-03-05, 05/03/24 etc.
                dt = pd.to_datetime(val, dayfirst=True, errors='raise')
                
                # Rückgabe als ISO-Format (z.B. "2024-03-05T00:00:00")
                return dt.isoformat()
            
            # Standard-Typumwandlung
            return cast_type(val)

        except (ValueError, TypeError, pd.errors.ParserError):
            type_name = "Datum (z.B. 05.03.2024)" if cast_type in [pd.Timestamp, "datetime"] else cast_type.__name__
            print(f"Fehler: Ungültige Eingabe. Erwartet wird: {type_name}")
