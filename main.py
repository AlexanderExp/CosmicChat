import telebot
from telebot import types
import datetime
import re
import db_functions

TOKEN = '5717083963:AAHflxPNEMzSklg_hc5Snbs24MQv4aaUyNU'
db_functions.create_database()


bot = telebot.TeleBot(TOKEN, parse_mode=None)

def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Гороскоп на сегодня')
    itembtn2 = types.KeyboardButton('Гороскоп на завтра')
    markup.add(itembtn1, itembtn2)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    state = db_functions.check_user(message.from_user.id)
    if state is None or state[0] == 'false':
        db_functions.register_user(message.from_user.id, state)
        bot.reply_to(message, "Добро пожаловать в бота-гороскоп! Пожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ.")
    else:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=create_main_menu_markup())

@bot.message_handler(func=lambda message: True)
def check_message(message):
    state = db_functions.check_user(message.from_user.id)
    if state is None:
        db_functions.register_user(message.from_user.id, state)
        bot.reply_to(message, "Добро пожаловать в бота-гороскоп! Пожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ.")
    elif state[0] == 'false':
        date_text = message.text
        if re.match(r'\d{2}\.\d{2}\.\d{4}', date_text):
            try:
                birth_date = datetime.datetime.strptime(date_text, '%d.%m.%Y')
                db_functions.set_birthday(birth_date, message.from_user.id)
                bot.reply_to(message, "Вы успешно зарегистрированы!")
            except:
                bot.reply_to(message, "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
        else:
            bot.reply_to(message, "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
    else:
        bot.send_message(message.chat.id, 'Класс')

bot.infinity_polling()