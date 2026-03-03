if cmd[0] == "add":
    n = input("Name: ")
    t = input("Typ (good/bad): ")
    
    #Startdatum
    s_date = input("Startdatum (YYYY-MM-DD) [Leer lassen für heute]: ").strip() or None
    
    #Dauer (Enddatum berechnen)
    dur_val = input("Dauer (Zahl): ")
    dur_unit = input("Einheit Dauer (D = Tage, W = Wochen, M = Monate): ").upper()
    duration = f"{dur_val}{dur_unit}"

    #Frequenz (x mal pro Intervall)
    count = input("Wie oft? (z.B. 3): ")
    unit = input("Pro was? (D = Tag, W = Woche, M = Monat): ").upper() #nur bei MS
    freq_str = f"{count}{unit}" 
    print("""Gebe die Wochentage ein mithilfe der zahlen an
1. Montag
2. Dienstag
3. Mittwoch
4. Donnerstag
5. Freitag
6. Samstag
7. Sonntag
zb 1 3 5 
          """)
    #Übergabe an Engine
    d = maine.add(n, t, freq_str, duration, s_date)
    
    
    
User input
n = input("Name: ")
    t = input("Typ (good/bad): ")
    
    #Startdatum
    #Dauer
    if d
    
    if w

    #auschlussregel
    
    