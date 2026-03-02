import logging

from engine import Engine


logger = logging.getLogger("HabitApp")


def main():
    logging.basicConfig(filename='main.log', level=logging.INFO)
    logger.info("Started")
    
    maine = Engine(logger)
    
    while True:
        # User Input
        raw = input("--> ").strip()
        # Prüfen ob input leer dann continue
        if not raw:
            logger.info("No Valid Input")
            continue
    
        cmd = raw.split()
        
        if cmd[0] == "add":
            n = input("Name: ")
            t = input("good or bad")
            f = input("'D' = Täglich, 'W' = Wöchentlich, 'MS' = Monatsanfang: ")
            p = input("period nur nr.: ")
            try:
                p = int(p)
            except ValueError:
            # Wenn frequency keine ganze Zahl ist:
                print(f"Fehler: {p} ist keine gültige Zahl für die Frequenz!")
                continue
                
            d = maine.add(n, t, p ,f)
            print(d)
        
        if cmd[0] == "p":
            print(maine.habits.keys())
        
        if cmd[0] == "list":
            maine.list_habits(cmd[1])
        if cmd[0] == "check-in":
            print(maine.check_in(cmd[1]))

            
        if cmd[0] == "exit":
            logger.info("Exit App")
            break
        
    


if __name__ == "__main__":
    main()