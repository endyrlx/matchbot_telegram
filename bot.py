import logging, credentials
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import dbcreate, sqlite3
import trainer
from random import randint

logging.basicConfig(filename='bot.log', level=logging.INFO)

bot = Updater(credentials.apikey)
dp = bot.dispatcher

def main():
    logging.info("Бот стартовал")
    dp.add_handler(CommandHandler("start", main_branch))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("addtest", addtest))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('adduser', adduser)],
        states={'NAME': [MessageHandler(Filters.text, username),
                         CommandHandler('skipname', skipname)],
                'GENDER': [MessageHandler(Filters.regex('^(Male|Female)$'), usergender),
                           CommandHandler('skipspecs', skipgender)],
                'ROLE': [MessageHandler(Filters.regex), userrole,
                         CommandHandler('skiprole', skiprole)],
                'SPECS': [MessageHandler(Filters.regex('^(Fitness|Running|Athletics|Heavy athletics|Crossfit)$'), userspecs),
                         CommandHandler('skipspecs', skipspecs)],
                'TEL': [MessageHandler(Filters.text, usertel),
                         CommandHandler('skipusertel', skiptel)]
                },
        fallbacks=[CommandHandler('usercancel', usercancel)]
    ))
#    dp.add_handler(MessageHandler(Filters.text, text))
#    dp.add_handler(MessageHandler(Filters.text, addtest))
    bot.start_polling()
    bot.idle()

def cancel(update, context):
    # Запись в лог об окончании диалога
    logging.info("Пользователь %s вышел из основного меню", update.message.from_user.first_name)
    # Сообщение пользователю в чат
    update.message.reply_text(
        'Режим эхо-бота. Для возвращения в главное меню выбери /start',
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END

def main_branch(update, context):
    reply_keyboard = [['/demo1', '/demo2']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Bot>Main \nТы находишься в главном меню. \nВыбери демо или /cancel для выхода в эхо-режим', reply_markup=markup_key,)
    logging.info("Пользователь %s в главном меню", update.message.from_user.first_name)
    return "main_state"

def text(update, context):
    usertext = update.message.text
    print(usertext)
    logging.info('{}: {}'.format(update.message.from_user.first_name, usertext))
    update.message.reply_text('Ты написал: {}'.format(usertext))

def addtest(update, context): #Добавляет запись в students с перечисленными ниже параметрами
    usertg = update.message.from_user.first_name
    logging.info("Пользователь %s присоединился к БД", update.message.from_user.first_name)
    update.message.reply_text('Bot>Main>addtest\nТестовое внесение записи\nв таблицу students')
    update.message.reply_text('Введи свое имя: ')
    username = update.message.text
    try:
        db = sqlite3.connect('demo1.db')  # Подключаемся к БД и создаем курсор
        cursor = db.cursor()
        # Далее передаем в подготовленную команду на создание студента необходимых параметров
        cursor.execute(
            f"""INSERT INTO students ('name', 'tgname', 'lookfor', 'mail', 'tel') VALUES ('{username}','{usertg}','test','test','{randint(1, 9999)}');""")
        db.commit()
        print(f'Добавлен ученик:{username}, {usertg}')
        update.message.reply_text('Запись внесена!')
        cursor.execute(f"""SELECT * FROM students WHERE tgname = '{usertg}'""")
        userbio = cursor.fetchall()
        i = 0
        for row in userbio:
            print('id: ', row[0])
            print('Name: ', row[1])
            print('TgName: ', row[2])
            print('Looking for: ', row[3])
            print('Mail: ', row[4])
            print('Tel: ', row[5])
            print('Telephone: ', row[6])

        update.message.reply_text(f'Ваша запись: {userbio}')
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        update.message.reply_text('Ошибка БД')

def connect(update, context):
    usertg = update.message.from_user.first_name
    logging.info("Пользователь %s добавляет запись в students", update.message.from_user.first_name)
    update.message.reply_text('Bot>Main>addtest\nТестовое внесение записи\nв таблицу students')
    update.message.reply_text('Введи свое имя: ')
    username = update.message.text
    try:
        db = sqlite3.connect('demo1.db')  # Подключаемся к БД и создаем курсор
        cursor = db.cursor()
        # Далее передаем в подготовленную команду на создание студента необходимых параметров
        cursor.execute(
            f"""INSERT INTO students ('name', 'tgname', 'lookfor', 'mail', 'tel') VALUES ('{username}','{usertg}','test','test','{username}');""")
        db.commit()
        print(f'Добавлен ученик:{username}, {usertg}')
        update.message.reply_text('Запись внесена!')
        cursor.execute(f"""SELECT * FROM students WHERE tgname = '{usertg}'""")
        userbio = cursor.fetchall()
        for row in userbio:
            print(row)
        update.message.reply_text(f'Ваша запись: {userbio}')
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        update.message.reply_text('Ошибка БД')


"""+++++++++++++++++START POINT ADD USER CONVERSATION++++++++++++++++"""

def adduser (update, context):
    usertg = update.message.from_user.first_name
    logging.info("Пользователь %s присоединился к БД через", update.message.from_user.first_name)
    update.message.reply_text('Bot>USER CONVERS\nДобавление нового пользователя\nв таблицу users')
    update.message.reply_text('Тебя нет в БД. Как тебя зовут?')
    username = update.message.text
    try:
        db = sqlite3.connect('demo1.db')  # Подключаемся к БД и создаем курсор
        cursor = db.cursor()
        # Далее передаем в подготовленную команду на создание студента необходимых параметров
        cursor.execute(
            f"""INSERT INTO students ('name', 'tgname', 'lookfor', 'mail', 'tel') VALUES ('{username}','{usertg}','test','test','{randint(1, 9999)}');""")
        db.commit()
        print(f'Добавлен ученик:{username}, {usertg}')
        update.message.reply_text('Запись внесена!')
        cursor.execute(f"""SELECT * FROM students WHERE tgname = '{usertg}'""")
        userbio = cursor.fetchall()
        i = 0
        for row in userbio:
            print('id: ', row[0])
            print('Name: ', row[1])
            print('TgName: ', row[2])
            print('Looking for: ', row[3])
            print('Mail: ', row[4])
            print('Tel: ', row[5])
            print('Telephone: ', row[6])

        update.message.reply_text(f'Ваша запись: {userbio}')
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        update.message.reply_text('Ошибка БД')



"""+++++++++++++++++END OF ADD USER CONVERSATION+++++++++++++++++++"""

if __name__ == "__main__":
    main()
#    dbconsole()
