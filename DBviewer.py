import sqlite3

def users():
    #Prints all the users in the database
    conn = sqlite3.connect("/home/pi/NoFlimsyCardsDB.db")
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    print("                     User Table                        ")
    print("+-----------------------------------------------------+")
    print("|ID  |UserID         |User Level  |Name               |")
    print("+-----------------------------------------------------+")
    for x in data:
        print repr(str(x[0])).ljust(4), repr(str(x[1])).ljust(15), repr(str(x[2])).ljust(12), repr(str(x[3])).ljust(1)
    print("")

    c.close()
    conn.commit()
    conn.close()

def logs():
    #Prints all the logs in the database
    conn = sqlite3.connect("/home/pi/NoFlimsyCardsDB.db")
    c = conn.cursor()
    c.execute('SELECT * FROM logs')
    data = c.fetchall()
    print("                     Logs Table                        ")
    print("+-----------------------------------------------------+")
    print("|ID  |UserID         |Date & Time           |Direction|")
    print("+-----------------------------------------------------+")
    for x in data:
        print repr(str(x[0])).ljust(4), repr(str(x[1])).ljust(15), repr(str(x[2])).ljust(22), repr(str(x[3])).ljust(1)
    print("")

    c.close()
    conn.commit()
    conn.close()
