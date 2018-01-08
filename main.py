#python 2.7
# Val Chapple
#
# Nov 2018
# Updated Jan 8, 2018
# MIT License

from config import database
import sys

#
# MAIN:
#
def main():
    print("USAGE: python2 " + sys.argv[0] + " username host password database")
    try:
        user = sys.argv[1]
    except:
        user = 'price_watcher'

    try:
        host = sys.argv[2]
    except:
        host = 'localhost'

    try:
        password = sys.argv[3]
    except:
        password = 'password'

    try:
        db = sys.argv[4]
    except:
        db = 'price_watcher'

    db = database(user, password, host, db)

    # MAIN MENU
    selection = 0
    numOptions = 2
    while selection < 1 or selection > numOptions:
        prompt  = " MENU\n"
        prompt += "======\n"
        prompt += "1 - Run Price Check (you must implement in config.py first)\n"
        prompt += "2 - Graph Prices (example data provided in \'sql\' folder)\n"
        prompt += ">> "

        selection = raw_input(prompt)
        try:
            selection = int(selection)
        except:
            selection = -1


    if selection == 1:
        db.runPriceChecks() # Must write your own code in config.py
    elif selection == 2:
        db.graphJobs()  # Uses database schema in folder "sql"
    else:
        print("ERROR")
        sys.exit()


if __name__ == "__main__":
    main()
