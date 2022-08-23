import sqlite3

try:
    db = sqlite3.connect('demo1.db')
    cursor = db.cursor()
    print('База создана и подключена')
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
#finally:
#    if (sqlite_connection):
#       sqlite_connection.close()
#        print("Соединение с SQLite закрыто")


cursor.execute("""CREATE TABLE IF NOT EXISTS trainers (
id integer not null primary key autoincrement,
name text not null,
tgname text not null,
spec integer not null,
gender boolean not null,
cost integer, 
mail varchar(40),
tel integer unique);
""")
print("Таблица Trainers создана")

cursor.execute("""CREATE TABLE IF NOT EXISTS students (
id integer not null primary key autoincrement,
name text not null,
tgname text not null,
lookfor integer not null,
mail varchar(40),
tel integer unique);
""")
print("Таблица Students создана")

cursor.execute("""CREATE TABLE IF NOT EXISTS specialities (
id integer not null primary key autoincrement,
name text varchar(40) not null);
""")
print("Таблица Specialities создана")

db.commit()

