print(f"Habit: {ha.name}; Art: {ha.type}; Start-Datum: {ha.start_date}; Start-Datum: {ha.end_date}; Dauer: {ha.duration}" + (f"; {ha.interval} mal die Woche."if ha.interval else""))



                print(f"\n{'ID':<5} | {'Titel':<20} | {'Status':<12}")
                print("-" * 45)
                for t in tickets:
                    print(f"{t.id:<5} | {t.title:<20} | {t.status:<12}")