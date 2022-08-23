from telegram.ext import CommandHandler, ConversationHandler, Updater, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import logging, sqlite3, time

#def connect()
#logging.info("Обращение к модулю trainer")

def choose_role(update, _):
    reply_keyboard = [['/trainer', '/student', '/cancelrole']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Bot>Main>Trainings\nВыбрана ветка роли. Выбери, кто ты. \nЕсли хочешь выйти из анкеты, выбери /tcancel', reply_markup=markup_key,)
    logging.info("Пользователь %s в ветке выбора роли", update.message.from_user.first_name)
    return "ROLE"

def trener(update, context):
    update.message.reply_text('Bot>Main>Trainings>Trainer\nВыбрана ветка тренера\nДля возврата в главное меню, выбери /tcancel')
    update.message.reply_text('Введи свое имя: ')
    logging.info("Пользователь %s в ветке тренера", update.message.from_user.first_name)


def student(update, context):
    update.message.reply_text('Bot>Main>Trainings>Student\nВыбрана ветка ученика\nДля возврата в главное меню, выбери /tcancel')
    logging.info("Пользователь %s в ветке студента", update.message.from_user.first_name)

def cancelrole(update, context):
    update.message.reply_text('Bot>Main\nВыход из выбора роли')
    logging.info("Пользователь %s отменил выбор роли", update.message.from_user.first_name)
    CommandHandler('demo1', choose_role)

def trainercancel(update, context):
    # Определяем пользователя
    # Запись в лог об окончании диалога
    logging.info("Пользователь %s вышел из анкеты.", update.message.from_user.first_name)
    # Сообщение пользователю в чат
    update.message.reply_text(
        'Bot>Main\nВы вышли из анкеты' ,
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END