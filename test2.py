import sqlite3, time

try:
    db = sqlite3.connect('demo1.db')
    cursor = db.cursor()
    time.sleep(0.3)
    print('Курсор подготовлен.', cursor)
    time.sleep(0.5)
    print('База создана и подключена. Создание таблиц...')
    time.sleep(0.8)

    try:
        cursor.execute("""CREATE TABLE trainers (
        id integer not null primary key autoincrement,
        name text not null,
        tgname text not null,
        spec integer not null,
        gender boolean not null,
        cost integer, 
        mail varchar(40),
        tel integer unique);
        """)
        db.commit()
        print("Таблица Trainers создана")
        time.sleep(0.5)
    except sqlite3.OperationalError:
        print("Таблица Trainers уже имеется")
        time.sleep(0.5)

    try:
        cursor.execute("""CREATE TABLE students (
        id integer not null primary key autoincrement,
        name text not null,
        tgname text not null,
        lookfor integer not null,
        mail varchar(40),
        tel integer unique);
        """)
        db.commit()
        print("Таблица Students создана")
        time.sleep(0.7)
    except sqlite3.OperationalError:
        print("Таблица Students уже имеется")
        time.sleep(0.7)

    try:
        cursor.execute("""CREATE TABLE specialities (
        id integer not null primary key autoincrement,
        name text varchar(40) not null);
        """)
        db.commit()
        print("Таблица Specialities создана")
        time.sleep(1.3)
    except sqlite3.OperationalError:
        print("Таблица Specialities уже имеется")
        time.sleep(1.3)

    print('База готова к работе...')

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

