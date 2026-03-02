import logging


logger = logging.getLogger("HabitApp")

def main():
    logging.basicConfig(filename='main.log', level=logging.INFO)
    logger.info("Started")
    
    
    while True:
        raw = input("--> ").strip()
        
        if not raw:
            logger.info("No Valid Input")
            continue
        cmd = raw.split()
        
        
        if cmd[0] == "exit":
            logger.info("Exit App")
            break
        
    


if __name__ == "__main__":
    main()