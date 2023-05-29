import sqlite3


def meal():
    connection = sqlite3.connect('campuscare365.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()
    print("finished")