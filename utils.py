import warnings
import pandas as pd

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
