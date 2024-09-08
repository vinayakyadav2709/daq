from datetime import datetime
import sqlite3

def database_connect():
    global database, cursor, table
    try:
        database = sqlite3.connect('daq.db')
        print("Connected to database 'daq' successfully")
        cursor = database.cursor()

        table = """ CREATE TABLE PINDATA (
            TIMESTAMP TEXT,
            PIN1 INTEGER,
            PIN2 INTEGER,
            PIN3 INTEGER,
            PIN4 INTEGER,
            PIN5 INTEGER,
            PIN6 INTEGER,
            PIN7 INTEGER,
            PIN8 INTEGER,
            PIN9 INTEGER
        ); """

        cursor.execute(table)
        print("Created table 'PINDATA' successfully")
    
    except:
        print("Connected to table 'PINDATA' successfully")

def database_store(decoded_line):
    result_list = []

    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    result_list.append(formatted_time)

    result_list.extend(decoded_line.strip())  # Assuming decoded_line is a string of bits

    cursor.execute('''INSERT INTO PINDATA VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(result_list))
    
    database.commit()
    return result_list

def database_disconnect():
    if database:
        database.commit() # test if redundant
        database.close()
        print('SQLite Connection closed')