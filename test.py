# In main.py beim "add" Command
if cmd[0] == "add":
    n = input("Name: ")
    t = input("Typ (good/bad): ")
    f = input("Wie oft pro Woche? (z.B. 3): ")
    
    # Wir speichern "3W" als internes Kürzel für "3x pro Woche"
    freq_code = f"{f}W" 
    
    # In deiner Engine.add() Methode
    # 'p' (period) nutzen wir hier als Platzhalter oder setzen es auf 0
    d = maine.add(n, t, 0, freq_code)
    print(f"Habit erstellt mit ID: {d}")