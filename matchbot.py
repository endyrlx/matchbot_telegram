import logging, credentials, sqlite3, usersdb
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(filename='matchbot.log', level=logging.INFO)

bot = Updater(credentials.apikey)
dp = bot.dispatcher
NAME, GENDER, ROLE, SPECS, TEL = range(5)

def main():
    logging.info("Бот стартовал")
    dp.add_handler(CommandHandler("start", welcome))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('adduser', adduser)],
        states={NAME: [MessageHandler(Filters.text, username),
                         CommandHandler('skipname', skipname)],
                GENDER: [MessageHandler(Filters.regex('^(Male|Female)$'), usergender),
                           CommandHandler('skipspecs', skipgender)],
                ROLE: [MessageHandler(Filters.text, userrole),
                         CommandHandler('skiprole', skiprole)],
                SPECS: [MessageHandler(Filters.regex('^(Fitness|Running|Athletics|Heavy athletics|Crossfit)$'), userspecs),
                         CommandHandler('skipspecs', skipspecs)],
                TEL: [MessageHandler(Filters.text, usertel),
                         CommandHandler('skipusertel', skiptel)]
                },
        fallbacks=[CommandHandler('usercancel', usercancel)]
    ))

    bot.start_polling()
    bot.idle()

def welcome(update, context):
    print('Вызван welcome')
    checkuser(update, context)

def checkuser(update, context): #Проверяем, есть ли пользователь в БД
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    usertg = update.message.from_user.first_name
    print('вызван checkuser')
    info = cursor.execute('SELECT * FROM users WHERE tgname=?', (usertg, ))
    if info.fetchone() is None: #Если пользователя нет в БД (ни одной записи)
        print('Пользователь отсутствует в бд')
        update.message.reply_text('Привет! Тебя нет в базе данных. Заполни анкету!')
        adduser(update, context)
    else: #Если пользователь есть в БД, переходим к проверке полноты записи
        print('Пользователь из базы')
        update.message.reply_text('Привет! Мы уже знакомы! Что хочешь сделать?')
        checkfull(update, context)

def checkfull(update, context):
    print('Вызван checkfull')
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    usertg = update.message.from_user.first_name
    if not None in cursor.execute('SELECT * FROM users WHERE tgname=?', (usertg, )).fetchone():
        print(f'Пользователь {usertg} с полной анкетой')
        update.message.reply_text('Найти напарника /findmate или /deleteuser для удаления своей записи')
    else:
        print(f'Пользователь {usertg} с неполной анкетой')
        update.message.reply_text('Твоя анкета не заполнена полностью. /reenter для повторного заполнения или /deleteuser для удаления')

def adduser(update, _):
    print('Вызван adduser')
    usertg = update.message.from_user.first_name
    logging.info("Пользователь %s перешел в заполнению анкеты", usertg)
    update.message.reply_text('Для начала, представься. Как тебя зовут? ')

    return NAME

def username(update, _):
    print('Вызван username')
    username = update.message.from_user
    usertg = update.message.from_user.first_name
    db = sqlite3.connect('users.db')  # Подключаемся к БД и создаем курсор
    cursor = db.cursor()
    # Далее передаем в подготовленную команду на создание студента необходимых параметров
    cursor.execute(
        f"""INSERT INTO users ('name') VALUES ('{username}') WHERE tgname='{usertg}';""")
    db.commit()
    print(f'Добавлен ученик:{username}, {usertg}')
    update.message.reply_text('Запись внесена!')
    cursor.execute(f"""SELECT * FROM users WHERE tgname = '{usertg}'""")
    userbio = cursor.fetchall()
    i = 0
    for row in userbio:
        print('id: ', row[0])
        print('TgName: ', row[1])
        print('Name: ', row[2])
        print('Gender: ', row[3])
        print('Role: ', row[4])
        print('Spec: ', row[5])
        print('Tel: ', row[6])

        update.message.reply_text(f'Ваша запись: {userbio}')

def skipname():
    pass

def usergender():
    pass

def skipgender():
    pass

def userrole():
    pass

def skiprole():
    pass

def userspecs():
    pass

def skipspecs():
    pass

def usertel():
    pass

def skiptel():
    pass

def usercancel():
    pass




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


if __name__ == "__main__":
    main()
    usersdb.usersdb()
