import sqlite3, nfc, datetime, time, RPi.GPIO as GPIO

def write_logs(userid):
    #Writes logs of the specified user to the db
    date = datetime.datetime.now()    
    current_date = date.strftime('%d/%m/%y %H:%M:%S')
    conn = sqlite3.connect("/home/pi/NoFlimsyCardsDB.db")
    c = conn.cursor()
    
    #Gets the next available ID in the table
    maxid = c.execute('SELECT max(id) FROM logs')
    maxidtuple = maxid.fetchone()
    newid = maxidtuple[0]+1

    #Switches the users direction
    if get_direction(userid) == "OUT":
        direction = "IN"
    else:
        direction = "OUT"
        
    #Creates the log in the table
    c.execute("INSERT INTO logs (id, userid, date_time, direction) VALUES (?,?,?,?);", (newid, userid, current_date, direction,))  
    conn.commit()
    c.execute("SELECT * FROM logs;")
    data = c.fetchall()
    c.close()
    conn.commit()
    conn.close()

def get_direction(userid):
    #Gets the last direction that a user went (in or out)
    conn = sqlite3.connect("/home/pi/NoFlimsyCardsDB.db")
    c = conn.cursor()
    last_entry = c.execute('SELECT max(id) FROM logs WHERE `userid` = ?;', (userid,))
    last_entry_tuple = last_entry.fetchone()
    last_direction = c.execute('SELECT `direction` FROM logs WHERE `id` = ?;', (last_entry_tuple[0],))
    last_direction_tuple = last_direction.fetchone()
    c.close()
    conn.commit()
    conn.close()
    return last_direction_tuple[0]


def loop():
    #The main loop that searches for NFC tags
    oldUser = ""
    while 1 < 2:
        t = nfcConnect()
        tagId = str(t[0])
        tagType = str(t[1])
        userId = str(t[2])
        if userId != None:
            if compareDate(userId) == True:
                if checkUser(userId) == True:
                    write_logs(userId)
                    print("User %s's activity has been logged." %(userId))
                    print("The TagType %s used was: %s." %(userId, tagType))
                    print("The ID of %s's tag is: %s." %(userId, tagId))
                    print("")
                    servoUp()
                    time.sleep(5)
                    servoDown()
                    
                else:
                    print("User is not registered in the database")
                
        else:
            pass
        continue

def compareDate(userId):
    #Compares the date between now and the user's last log
    try:
        date = datetime.datetime.now()
        
        conn = sqlite3.connect("/home/pi/NoFlimsyCardsDB.db")
        c = conn.cursor()
        lastLog = c.execute('SELECT max(date_time) FROM logs WHERE `userid` = ?;', (userId,))
        data = lastLog.fetchone()
        lastDateTime = datetime.datetime.strptime(data[0], '%d/%m/%y %H:%M:%S')
        c.close()
        conn.commit()
        conn.close()
        if lastDateTime < date-datetime.timedelta(seconds=10):
            return True
    except TypeError:
        return False

def checkUser(userId):
    #Checks if the user is in the database
    conn = sqlite3.connect("/home/pi/NoFlimsyCardsDB.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM users"):
        if str(row[1]) == str(userId):
            c.close()
            conn.commit()
            conn.close()
            return True

def nfcConnect():
    #Searches for a response from a specific App
    try:
        clf = nfc.ContactlessFrontend("tty:AMA0")
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})

        cla = 0x00
        ins = 0xA4
        p1 = 0x04
        p2 = 0x00
        data = bytearray.fromhex("F0010203040506")

        response = tag.send_apdu(cla, ins, p1, p2, data, check_status=False)
        
        tag_id = str(tag._nfcid).encode("hex")
        tag_type = tag.type
        returnData = [tag_id, tag_type, response]
        clf.close()
        return returnData
    
    except nfc.tag.TIMEOUT_ERROR:
        clf.close()
        returnData = [None, None, None]
        return returnData
    
    except nfc.tag.RECEIVE_ERROR:
        clf.close()
        returnData = [None, None, None]
        return returnData

    except nfc.tag.PROTOCOL_ERROR:
        clf.close()
        returnData = [None, None, None]
        return returnData

    except nfc.tag.TagCommandError:
        clf.close()
        returnData = [None, None, None]
        return returnData

    except nfc.clf.TransmissionError:
        clf.close()
        returnData = [None, None, None]
        return returnData

    except nfc.clf.TimeoutError:
        clf.close()
        returnData = [None, None, None]
        return returnData

def servoUp():
    #Moves the servo to the upright position
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    pwm = GPIO.PWM(11, 50)
    pwm.start(7)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()

def servoDown():
    #Moves the servo to the closed position
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    pwm = GPIO.PWM(11, 50)
    pwm.start(2.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(7)
    time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    loop()
