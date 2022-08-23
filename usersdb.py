import sqlite3
import time

def usersdb():
    try:
        db = sqlite3.connect('users.db')
        cursor = db.cursor()
        print('База создана и подключена')
        time.sleep(0.3)
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id integer not null primary key autoincrement,
        tgname varchar(40),
        name varchar(40),
        gender boolean,
        role boolean,
        spec varchar(40),
        tel integer,
        bio text,
        photo text);
        """)
        print("Таблица users создана")
        time.sleep(0.6)

        db.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (db):
           db.close()
           print("Соединение с SQLite закрыто")
           time.sleep(0.6)

