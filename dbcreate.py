import sqlite3, time

def dbcreate():
    print('вызван dbcreate')
    try:
        db = sqlite3.connect('demo1.db')
        cursor = db.cursor()
        time.sleep(0.1)
        print('Курсор подготовлен.', cursor)
        time.sleep(0.1)
        print('База создана и подключена. Создание таблиц...')
        time.sleep(0.1)

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
            time.sleep(0.1)
        except sqlite3.OperationalError:
            print("Таблица Trainers уже имеется")
            time.sleep(0.1)

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
            time.sleep(0.1)
        except sqlite3.OperationalError:
            print("Таблица Students уже имеется")
            time.sleep(0.1)

        try:
            cursor.execute("""CREATE TABLE specialities (
            id integer not null primary key autoincrement,
            name text varchar(40) not null);
            """)
            db.commit()
            print("Таблица Specialities создана")
            time.sleep(0.1)
        except sqlite3.OperationalError:
            print("Таблица Specialities уже имеется")
            time.sleep(0.1)

        print('База готова к работе...')

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

def createstudent():
    print('вызван createstudent')
    answer = 'y' #Задаем начальный параметр переключателя для повторения цикла добавления студента
    while answer == 'y':
        name = input('Name: ')
        tgname = input("tgname: ")
        lookfor = input("lookfor: ")
        mail=input('mail: ')
        tel = input('tel: ')
        try:
            db = sqlite3.connect('demo1.db') #Подключаемся к БД и создаем курсор
            cursor = db.cursor()
            time.sleep(0.1)
            print('Курсор подготовлен.', cursor)
            time.sleep(0.1)
            print('База подключена.')
            time.sleep(0.1)
            #Далее передаем в подготовленную команду на создание студента необходимых параметров
            cursor.execute(f"""INSERT INTO students ('name', 'tgname', 'lookfor', 'mail', 'tel') VALUES ('{name}','{tgname}','{lookfor}','{mail}','{tel}');""")
            db.commit()
            print(f'Добавлен ученик:{name}, {lookfor}')
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        answer=input('Добавить ещё запись (y) или выйти (любой ответ)?: ') #Запрос пользователю ответа на повторение цикла добавления студента
    print('Добавление студентов завершено!')
def dbconsole(): #Инструмент прямого взаимодействия с sql через интерфейс бота
    print('Вызвана dbconsole')
    try:
        db = sqlite3.connect('demo1.db')
        cursor = db.cursor()
        time.sleep(0.1)
        print('Курсор подготовлен.', cursor)
        #           telluser('Курсор подготовлен.')
        time.sleep(0.1)
        print('База подключена.')
        #           telluser('База подключена.')
        time.sleep(0.1)
        while True:
           usertext = input('sql>>> ')
#            dp.add_handler(MessageHandler(Filters.text)) #Возможно, эта строка тут неуместна. Так же, здесь отсутствует вызов функции
            #telluser = update.message.reply_text
            #usertext = update.message.text
            #update.message.reply_text('Bot>Main>sql\nВыбрана sql консоль.', reply_markup=markup_key)
            #logging.info("Пользователь %s в sql консоли", update.message.from_user.first_name)

                #Подключаемся к БД для прямого взаимодействия с ней

           cursor.execute(f"""{usertext}""")
           db.commit()
           rows = cursor.fetchall()
           for row in rows:
               print(row)
           update.message.reply_text(cursor.fetchone())
    except:
        print('Ошибка')

def main():
    print('вызван main')
    dbcreate()




main()
#dbconsole()
#createstudent()
print('Конец')